import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, formatdate, make_msgid
from typing import List, Dict
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_workload_identity import Client
from cozeloop.decorator import observe
from graphs.state import SendEmailInput, SendEmailOutput


def get_email_config():
    """获取邮件配置信息"""
    client = Client()
    email_credential = client.get_integration_credential("integration-email-imap-smtp")
    return json.loads(email_credential)


@observe
def send_email_with_content(subject: str, content: str, to_addrs: list) -> dict:
    """
    发送HTML格式的邮件
    
    Args:
        subject: 邮件主题
        content: 邮件正文（HTML格式）
        to_addrs: 收件人列表，如["recipient1@xxx.com"]
        
    Returns:
        发送结果字典，包含状态和消息
    """
    try:
        config = get_email_config()
        
        msg = MIMEText(content, "html", "utf-8")
        msg["From"] = formataddr(("RSS订阅通知", config["account"]))
        msg["To"] = ", ".join(to_addrs) if to_addrs else ""
        msg["Subject"] = Header(subject, "utf-8")
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid()
        
        all_recipients = to_addrs.copy()
        if not all_recipients:
            return {"status": "error", "message": "收件人为空"}
        
        ctx = ssl.create_default_context()
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        
        with smtplib.SMTP_SSL(config["smtp_server"], config["smtp_port"], context=ctx, timeout=30) as server:
            server.ehlo()
            server.login(config["account"], config["auth_code"])
            server.sendmail(config["account"], all_recipients, msg.as_string())
            server.quit()
        
        return {
            "status": "success",
            "message": f"邮件成功发送给 {len(to_addrs)} 位收件人",
            "recipient_count": len(to_addrs)
        }
    except smtplib.SMTPAuthenticationError as e:
        return {"status": "error", "message": f"认证失败: {str(e)}"}
    except smtplib.SMTPRecipientsRefused as e:
        return {"status": "error", "message": "收件人被拒绝", "detail": {k: str(v) for k, v in getattr(e, "recipients", {}).items()}}
    except smtplib.SMTPSenderRefused as e:
        return {"status": "error", "message": f"发件人被拒绝: {e.smtp_code} {e.smtp_error}"}
    except smtplib.SMTPDataError as e:
        return {"status": "error", "message": f"数据被拒绝: {e.smtp_code} {e.smtp_error}"}
    except smtplib.SMTPConnectError as e:
        return {"status": "error", "message": f"连接失败: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"发送失败: {str(e)}"}


def send_email_node(state: SendEmailInput, config: RunnableConfig, runtime: Runtime[Context]) -> SendEmailOutput:
    """
    title: 发送邮件
    desc: 将新文章通过邮件发送给指定收件人
    integrations: 邮件
    """
    ctx = runtime.context
    
    # 如果没有新文章，返回成功但不发送
    if not state.new_articles:
        return SendEmailOutput(
            send_result={"status": "skipped", "message": "没有新内容，跳过发送"},
            email_sent=False
        )
    
    # 构建邮件内容
    html_content = "<html><body>"
    html_content += "<h2>RSS订阅更新通知</h2>"
    html_content += f"<p>发现 {len(state.new_articles)} 篇新文章：</p><hr>"
    
    for idx, article in enumerate(state.new_articles):
        html_content += f"<h3>{idx + 1}. {article['title']}</h3>"
        html_content += f"<p><strong>链接：</strong><a href=\"{article['link']}\">{article['link']}</a></p>"
        if article.get('published'):
            html_content += f"<p><strong>发布时间：</strong>{article['published']}</p>"
        if article.get('description'):
            html_content += f"<p><strong>摘要：</strong>{article['description']}</p>"
        html_content += "<hr>"
    
    html_content += "</body></html>"
    
    # 发送邮件
    send_result = send_email_with_content(
        subject=f"RSS订阅更新 - 发现{len(state.new_articles)}篇新文章",
        content=html_content,
        to_addrs=[state.recipient_email]
    )
    
    email_sent = send_result.get("status") == "success"
    
    # 设置email_status
    if send_result.get("status") == "skipped":
        email_status = "跳过发送"
    elif email_sent:
        email_status = "发送成功"
    else:
        email_status = f"发送失败: {send_result.get('message', '未知错误')}"
    
    return SendEmailOutput(
        send_result=send_result,
        email_sent=email_sent,
        email_status=email_status
    )
