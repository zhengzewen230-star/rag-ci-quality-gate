# src/rag_app.py

def query_rag_pipeline(user_query: str) -> dict:
    """
    模拟一个 RAG 知识库系统：
    接收用户提问 -> 检索知识库上下文 -> 返回 AI 的回答
    """
    # 模拟知识库中的预设文档段落
    knowledge_base = {
        "退货": [
            "公司退换货规定：商品购买 7 天内且未拆封状态下，支持无理由退货；已拆封商品不支持退货。",
            "退款将在收到退货物品并确认无损后的 3 个工作日内原路退回。"
        ],
        "发票": [
            "电子发票会在订单完成后 24 小时内自动发送至下单填写的邮箱。",
            "增值税专用发票需要提供企业抬头与纳税人识别号，按月统一开具。"
        ]
    }

    # 模拟业务匹配逻辑与回答（这里故意包含 1 个正确回答和 1 个带幻觉的错误回答，用于测试）
    if "退货" in user_query or "拆封" in user_query:
        # 故意模拟一个包含幻觉的错误回答，测试我们的质量门槛是否能抓住它
        context = knowledge_base["退货"]
        response = "只要买了就能随时退，哪怕拆封使用过也没关系，我们包邮退！"
    elif "发票" in user_query:
        # 模拟一个准确无幻觉的回答
        context = knowledge_base["发票"]
        response = "电子发票会在订单完成后的 24 小时内发送到您的电子邮箱。"
    else:
        context = ["未找到匹配的知识库信息。"]
        response = "抱歉，我暂时无法回答这个问题。"

    return {
        "input": user_query,
        "actual_output": response,
        "retrieval_context": context
    }