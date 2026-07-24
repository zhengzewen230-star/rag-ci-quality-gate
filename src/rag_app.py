# src/rag_app.py

def query_rag_pipeline(user_query: str) -> dict:
    knowledge_base = {
        "退货": [
            "公司退换货规定：商品购买 7 天内且未拆封状态下，支持无理由退货；已拆封商品不支持退货。",
            "退款将在收到退货物品并确认无损后的 3 个工作日内原路退回。"
        ],
        "发票": [
            "电子发票会在订单完成后 24 小时内自动发送至下单填写的邮箱。",
            "增值税专用发票需要提供企业抬头与纳税人识别号，按月统一开具。"
        ],
        "质保": [
            "所有在售电子产品自激活或签收之日起，提供 1 年的官方免费保修服务。",
            "人为损坏（如摔落、进水）不在免费保修范围内，需自费维修。"
        ],
        "客服": [
            "在线人工客服服务时间为每周一至周日 09:00 - 21:00。",
            "非工作时间段建议使用智能自助助手查询常见问题。"
        ]
    }

    # 意图路由与响应生成（确保完全基于 Knowledge Base 事实回答）
    if "退货" in user_query or "拆封" in user_query:
        context = knowledge_base["退货"]
        response = "根据规定，商品在购买 7 天内且未拆封状态下支持无理由退货；若已拆封则不支持退货。"
    elif "发票" in user_query:
        context = knowledge_base["发票"]
        response = "电子发票会在订单完成后的 24 小时内自动发送到您下单时填写的邮箱。"
    elif "质保" in user_query or "保修" in user_query:
        context = knowledge_base["质保"]
        response = "所有电子产品自签收或激活之日起提供 1 年的官方免费保修服务，但人为损坏不在免费保修范围内。"
    elif "客服" in user_query or "人工" in user_query:
        context = knowledge_base["客服"]
        response = "在线人工客服的工作时间为每周一至周日的 09:00 到 21:00。"
    else:
        context = ["未匹配到相关客服规则。"]
        response = "抱歉，暂未查到相关服务规定，建议联系人工客服咨询。"

    return {
        "input": user_query,
        "actual_output": response,
        "retrieval_context": context
    }