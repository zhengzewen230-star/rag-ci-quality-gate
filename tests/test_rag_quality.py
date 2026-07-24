import json
import os
import pytest
from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase
from openai import OpenAI

from src.rag_app import query_rag_pipeline

load_dotenv()


# 1. 使用 OpenAI 兼容 SDK 封装 DeepSeek 裁判模型
class DeepSeekJudgeModel(DeepEvalBaseLLM):

    def __init__(self, model_name="deepseek-chat"):
        self.model_name = model_name
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        )

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,  # 评估类任务建议将随机度设为 0，确保评估稳定
        )
        return response.choices[0].message.content

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return self.model_name


# 初始化 DeepSeek 裁判实例
# 换成硅基流动的 DeepSeek-V3 模型 (或 "Qwen/Qwen2.5-7B-Instruct")
deepseek_judge = DeepSeekJudgeModel(model_name="deepseek-ai/DeepSeek-V3")


# 2. 读取测试数据集
def load_test_cases():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "test_cases.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


# 3. 参数化测试套件
@pytest.mark.parametrize("case_data", load_test_cases())
def test_rag_faithfulness(case_data):
    user_input = case_data["input"]

    # 1. 运行被测业务代码获取回答
    rag_result = query_rag_pipeline(user_input)

    # 2. 构造 DeepEval 测试用例
    test_case = LLMTestCase(
        input=rag_result["input"],
        actual_output=rag_result["actual_output"],
        retrieval_context=rag_result["retrieval_context"],
    )

    # 3. 配置忠实度评估指标 (阈值 0.8)
    faithfulness_metric = FaithfulnessMetric(
        threshold=0.8, model=deepseek_judge, include_reason=True
    )

    # 4. 执行评估断言
    assert_test(test_case, [faithfulness_metric])