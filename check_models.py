import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("=== 你的 API Key 支持的可用模型列表 ===")
try:
    for model in client.models.list():
        # 筛选出支持 generateContent 的模型
        if "generateContent" in model.supported_actions:
            print(model.name)
except Exception as e:
    print(f"查询失败，请检查 API Key: {e}")