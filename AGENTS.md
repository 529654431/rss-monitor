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

## 定时任务部署方案

本项目支持多种定时任务部署方案，可根据实际需求选择：

### 方案一：GitHub Actions（推荐）⭐
- **适用场景**: 无需服务器、完全免费、24/7运行
- **成本**: 完全免费（公开仓库）
- **部署难度**: ⭐⭐ 简单
- **文档**: [GitHub Actions快速部署指南](docs/QUICK_START_GITHUB_ACTIONS.md)
- **详细文档**: [GitHub Actions完整部署指南](docs/GITHUB_ACTIONS_DEPLOY.md)

### 方案二：Linux Cron + HTTP服务
- **适用场景**: 本地服务器或云服务器
- **成本**: 免费（服务器成本除外）
- **部署难度**: ⭐⭐⭐ 中等
- **文档**: [Cron定时任务部署指南](docs/RSS_CRON_SETUP.md)

### 方案三：Kubernetes CronJob
- **适用场景**: K8s集群环境
- **成本**: 取决于K8s集群成本
- **部署难度**: ⭐⭐⭐⭐ 较难

### 方案四：Docker + Crontab
- **适用场景**: 容器化部署
- **成本**: 取决于容器平台成本
- **部署难度**: ⭐⭐⭐ 中等

### 推荐选择
- **个人使用**: GitHub Actions（免费、无需维护）
- **企业使用**: Kubernetes CronJob（稳定、可扩展）
- **本地测试**: Linux Cron（快速、方便）

## 定时频率建议
- **高频监控**: 每30分钟（`*/30 * * * *`）
- **标准监控**: 每1小时（`0 * * * *`）
- **低频监控**: 每2-4小时（`0 */2 * * *`）
- **每日摘要**: 每天9点（`0 1 * * *` UTC时间）

## 工作流特性
- 自动记录已处理的文章ID，避免重复发送邮件
- 已处理的文章列表保留最近1000条记录
- 支持手动触发和定时触发
- 提供详细的执行日志

## 输入输出说明
**输入参数**:
- `rss_url`: RSS订阅源URL（必填）
- `recipient_email`: 收件人邮箱（必填）

**输出结果**:
- `total_fetched`: 获取的文章总数
- `new_count`: 新文章数量
- `email_status`: 邮件发送状态
