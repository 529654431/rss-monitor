from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class GlobalState(BaseModel):
    """全局状态定义"""
    rss_url: str = Field(..., description="RSS订阅源URL")
    recipient_email: str = Field(..., description="收件人邮箱")
    fetched_articles: List[Dict] = Field(default_factory=list, description="从RSS获取的文章列表")
    processed_articles: List[str] = Field(default_factory=list, description="已处理的文章ID列表")
    new_articles: List[Dict] = Field(default_factory=list, description="新发现的文章列表")
    email_sent: bool = Field(default=False, description="邮件是否已发送")
    send_result: Dict = Field(default_factory=dict, description="邮件发送结果")
    total_fetched: int = Field(default=0, description="获取的文章总数")
    new_count: int = Field(default=0, description="新文章数量")
    email_status: str = Field(default="未发送", description="邮件发送状态")

class GraphInput(BaseModel):
    """工作流的输入"""
    rss_url: str = Field(..., description="RSS订阅源URL")
    recipient_email: str = Field(..., description="收件人邮箱")

class GraphOutput(BaseModel):
    """工作流的输出"""
    total_fetched: int = Field(..., description="获取的文章总数")
    new_count: int = Field(..., description="新文章数量")
    email_status: str = Field(..., description="邮件发送状态")

# RSS获取节点
class FetchRSSInput(BaseModel):
    """RSS获取节点的输入"""
    rss_url: str = Field(..., description="RSS订阅源URL")

class FetchRSSOutput(BaseModel):
    """RSS获取节点的输出"""
    fetched_articles: List[Dict] = Field(..., description="从RSS获取的文章列表")
    total_fetched: int = Field(..., description="获取的文章总数")

# 新内容判断节点
class CheckNewContentInput(BaseModel):
    """新内容判断节点的输入"""
    fetched_articles: List[Dict] = Field(..., description="从RSS获取的文章列表")
    processed_articles: Optional[List[str]] = Field(default_factory=list, description="已处理的文章ID列表")

class CheckNewContentOutput(BaseModel):
    """新内容判断节点的输出"""
    new_articles: List[Dict] = Field(..., description="新发现的文章列表")
    updated_processed_articles: List[str] = Field(..., description="更新后的已处理文章ID列表")
    new_count: int = Field(..., description="新文章数量")
    email_status: str = Field(default="未发送", description="邮件发送状态")

# 邮件发送节点
class SendEmailInput(BaseModel):
    """邮件发送节点的输入"""
    new_articles: List[Dict] = Field(..., description="新发现的文章列表")
    recipient_email: str = Field(..., description="收件人邮箱")

class SendEmailOutput(BaseModel):
    """邮件发送节点的输出"""
    send_result: Dict = Field(..., description="邮件发送结果")
    email_sent: bool = Field(..., description="邮件是否已发送")
    email_status: str = Field(..., description="邮件发送状态")
