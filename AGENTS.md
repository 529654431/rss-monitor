## 项目概述
- **名称**: RSS订阅监控与邮件通知工作流
- **功能**: 定时扫描RSS订阅源，发现新内容时自动发送邮件通知

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| fetch_rss | `nodes/fetch_rss_node.py` | task | 获取RSS内容 | - | - |
| check_new_content | `nodes/check_new_content_node.py` | condition | 检查是否有新内容 | "有新内容"→send_email, "无新内容"→END | - |
| send_email | `nodes/send_email_node.py` | task | 发送邮件通知 | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 子图清单
无

## 技能使用
- 节点`send_email`使用邮件技能

## 定时任务说明
此工作流需要通过外部定时任务调度器（如Cron、Kubernetes CronJob等）定期调用，实现定时扫描功能。建议设置每30分钟或1小时执行一次。

工作流会自动记录已处理的文章ID，避免重复发送邮件。已处理的文章列表会保留最近1000条记录。

## 输入输出说明
**输入参数**:
- `rss_url`: RSS订阅源URL（必填）
- `recipient_email`: 收件人邮箱（必填）

**输出结果**:
- `total_fetched`: 获取的文章总数
- `new_count`: 新文章数量
- `email_status`: 邮件发送状态
