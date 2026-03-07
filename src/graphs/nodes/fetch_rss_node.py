import feedparser
from typing import List, Dict
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import FetchRSSInput, FetchRSSOutput


def fetch_rss_node(state: FetchRSSInput, config: RunnableConfig, runtime: Runtime[Context]) -> FetchRSSOutput:
    """
    title: 获取RSS内容
    desc: 从指定的RSS订阅源获取文章列表
    integrations: 
    """
    ctx = runtime.context
    
    # 解析RSS源
    feed = feedparser.parse(state.rss_url)
    
    articles = []
    for entry in feed.entries:
        article = {
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "description": entry.get("description", ""),
            "id": entry.get("id", entry.get("link", ""))  # 使用link作为唯一ID
        }
        articles.append(article)
    
    return FetchRSSOutput(
        fetched_articles=articles,
        total_fetched=len(articles)
    )
