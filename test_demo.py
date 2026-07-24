import os
from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric
from deepeval.models.base_model import DeepEvalBaseLLM
from google import genai

# 加载 .env 里的 GOOGLE_API_KEY
load_dotenv()

# 1. 使用 Google 官方原生 Client 封装 DeepEval 裁判类
class GeminiJudgeModel(DeepEvalBaseLLM):
    def __init__(self, model_name="gemini-2.5-flash"):
        # 如果 gemini-2.5-flash 依然报错，可尝试切换为 "gemini-1.5-flash" 或 "gemini-2.0-flash"
        self.model_name = model_name
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response.text

    async def a_generate(self, prompt: str) -> str:
        # 简化版异步调用
        return self.generate(prompt)

    def get_model_name(self):
        return self.model_name


def test_hallucination_demo():
    # 初始化 Gemini 作为裁判模型
    # 注：如果你使用的是 Gemini 2.5 系列，填 "gemini-2.5-flash"，如果是 1.5 系列，填 "gemini-1.5-flash"
    gemini_model = GeminiJudgeModel(model_name="gemini-flash-latest")

    test_case = LLMTestCase(
        input="我买的东西拆封了，还能退货吗？",
        actual_output="可以的，我们支持任意时间的无理由退换货，拆封了也不影响！",
        retrieval_context=[
            "公司退换货规定：商品购买 7 天内且未拆封状态下，支持无理由退货；已拆封商品不支持退货。"
        ]
    )

    # 2. 将裁判模型指定为你的 gemini_model
    faithfulness_metric = FaithfulnessMetric(
        threshold=0.7,
        model=gemini_model,
        include_reason=True
    )

    # 断言测试
    assert_test(test_case, [faithfulness_metric])