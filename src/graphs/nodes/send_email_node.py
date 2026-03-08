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
    desc: 将新文章逐篇通过邮件发送给指定收件人（每篇文章单独发送）
    integrations: 邮件
    """
    import time
    ctx = runtime.context
    
    # 如果没有新文章，返回成功但不发送
    if not state.new_articles:
        return SendEmailOutput(
            send_result={"status": "skipped", "message": "没有新内容，跳过发送"},
            email_sent=False
        )
    
    # 统计发送结果
    total_count = len(state.new_articles)
    success_count = 0
    failed_count = 0
    send_details = []
    
    # 逐篇发送邮件
    for idx, article in enumerate(state.new_articles):
        # 构建单篇文章的邮件内容
        html_content = "<html><body>"
        html_content += "<h2>📰 新文章通知</h2>"
        html_content += f"<h1>{article['title']}</h1>"
        html_content += "<hr>"
        html_content += f"<p><strong>🔗 文章链接：</strong><a href=\"{article['link']}\">{article['link']}</a></p>"
        if article.get('published'):
            html_content += f"<p><strong>📅 发布时间：</strong>{article['published']}</p>"
        if article.get('description'):
            html_content += f"<p><strong>📝 内容摘要：</strong></p>"
            html_content += f"<p>{article['description']}</p>"
        html_content += "<hr>"
        html_content += f"<p><small>RSS订阅源：{state.recipient_email}</small></p>"
        html_content += "</body></html>"
        
        # 构建邮件主题（包含文章标题）
        subject = f"📰 新文章：{article['title']}"
        
        # 发送邮件
        send_result = send_email_with_content(
            subject=subject,
            content=html_content,
            to_addrs=[state.recipient_email]
        )
        
        # 记录发送结果
        if send_result.get("status") == "success":
            success_count += 1
            send_details.append({
                "title": article['title'],
                "status": "success",
                "message": "发送成功"
            })
        else:
            failed_count += 1
            send_details.append({
                "title": article['title'],
                "status": "failed",
                "message": send_result.get('message', '发送失败')
            })
        
        # 延迟2秒，避免被邮件服务器限制（短时间内发送大量邮件可能被判定为垃圾邮件）
        if idx < total_count - 1:  # 最后一次不需要延迟
            time.sleep(2)
    
    # 构建总体发送结果
    result_summary = {
        "total": total_count,
        "success": success_count,
        "failed": failed_count,
        "details": send_details
    }
    
    # 设置email_status
    if failed_count == 0:
        email_status = f"全部成功：{success_count}/{total_count} 篇文章"
    elif success_count == 0:
        email_status = f"全部失败：{failed_count}/{total_count} 篇文章"
    else:
        email_status = f"部分成功：成功 {success_count} 篇，失败 {failed_count} 篇"
    
    return SendEmailOutput(
        send_result=result_summary,
        email_sent=success_count > 0,
        email_status=email_status
    )
