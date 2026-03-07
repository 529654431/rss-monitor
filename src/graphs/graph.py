from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.fetch_rss_node import fetch_rss_node
from graphs.nodes.check_new_content_node import check_new_content_node
from graphs.nodes.send_email_node import send_email_node


def has_new_content(state: GlobalState) -> str:
    """
    title: 是否有新内容
    desc: 判断是否有新文章需要发送邮件
    """
    if state.new_count > 0:
        return "发送邮件"
    else:
        return "结束"


# 创建状态图，指定工作流的入参和出参
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("fetch_rss", fetch_rss_node)
builder.add_node("check_new_content", check_new_content_node)
builder.add_node("send_email", send_email_node)

# 设置入口点
builder.set_entry_point("fetch_rss")

# 添加边
builder.add_edge("fetch_rss", "check_new_content")

# 添加条件分支
builder.add_conditional_edges(
    source="check_new_content",
    path=has_new_content,
    path_map={
        "发送邮件": "send_email",
        "结束": END
    }
)

builder.add_edge("send_email", END)

# 编译图
main_graph = builder.compile()
