from typing import List, Dict
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import CheckNewContentInput, CheckNewContentOutput


def check_new_content_node(state: CheckNewContentInput, config: RunnableConfig, runtime: Runtime[Context]) -> CheckNewContentOutput:
    """
    title: 检查新内容
    desc: 比较获取的文章和已处理的文章，筛选出新内容
    integrations: 
    """
    ctx = runtime.context
    
    # 筛选出新文章（不在已处理列表中的文章）
    new_articles = [
        article for article in state.fetched_articles
        if article["id"] not in state.processed_articles
    ]
    
    # 更新已处理的文章ID列表
    updated_processed = state.processed_articles.copy()
    for article in state.fetched_articles:
        if article["id"] not in updated_processed:
            updated_processed.append(article["id"])
    
    # 限制已处理列表大小，保留最近1000个
    if len(updated_processed) > 1000:
        updated_processed = updated_processed[-1000:]
    
    # 如果没有新内容，设置email_status为"无新内容"
    email_status = "无新内容" if len(new_articles) == 0 else "待发送"
    
    return CheckNewContentOutput(
        new_articles=new_articles,
        updated_processed_articles=updated_processed,
        new_count=len(new_articles),
        email_status=email_status
    )
