# RSS监控Cron定时任务部署指南

## 概述

本指南介绍如何使用Linux Cron定时任务，每小时自动执行RSS监控并发送邮件通知。

## 文件说明

| 文件 | 功能 |
|------|------|
| `scripts/start_rss_service.sh` | 启动HTTP服务 |
| `scripts/stop_rss_service.sh` | 停止HTTP服务 |
| `scripts/setup_cron.sh` | 配置Cron定时任务 |
| `scripts/cron_rss_monitor.sh` | 直接执行RSS监控（可选） |

## 快速开始

### 步骤1：启动HTTP服务

```bash
# 启动RSS监控服务
bash scripts/start_rss_service.sh
```

输出示例：
```
[INFO] 正在启动RSS监控HTTP服务...
[INFO] 工作目录: /workspace/projects
[INFO] 监听端口: 8000
[INFO] 日志目录: /workspace/projects/logs
[INFO] ✓ 服务启动成功!
[INFO] PID: 12345
[INFO] 访问地址: http://localhost:8000
[INFO] API文档: http://localhost:8000/docs
[INFO] 查看日志: tail -f /workspace/projects/logs/rss_service.log
[INFO] 停止服务: bash scripts/stop_rss_service.sh
```

### 步骤2：配置Cron定时任务

```bash
# 运行Cron配置脚本
bash scripts/setup_cron.sh
```

脚本会自动：
1. 检查HTTP服务是否运行
2. 备份现有crontab
3. 添加每小时执行一次的Cron任务
4. 显示配置结果

### 步骤3：验证配置

```bash
# 查看Cron任务列表
crontab -l
```

应该看到类似这样的任务：
```bash
0 * * * * curl -s -X POST http://localhost:8000/api/v1/workflow/run -H 'Content-Type: application/json' -d '{"rss_url": "https://cn.investing.com/rss/news_285.rss", "recipient_email": "529654431@qq.com"}' >> /workspace/projects/logs/cron_rss_monitor.log 2>&1
```

## 服务管理

### 查看服务状态

```bash
# 查看服务进程
ps aux | grep main.py | grep -v grep

# 查看服务日志
tail -f logs/rss_service.log

# 查看Cron执行日志
tail -f logs/cron_rss_monitor.log
```

### 停止服务

```bash
# 停止HTTP服务
bash scripts/stop_rss_service.sh
```

### 重启服务

```bash
# 重启服务
bash scripts/stop_rss_service.sh
bash scripts/start_rss_service.sh
```

## Cron任务管理

### 查看Cron任务

```bash
# 查看所有Cron任务
crontab -l

# 查看Cron任务执行日志
tail -f logs/cron_rss_monitor.log
```

### 修改Cron任务

```bash
# 编辑Cron任务
crontab -e
```

修改执行频率的示例：
```bash
# 每小时执行（默认）
0 * * * * curl ...

# 每30分钟执行
*/30 * * * * curl ...

# 每2小时执行
0 */2 * * * curl ...

# 每天上午9点执行
0 9 * * * curl ...
```

### 删除Cron任务

```bash
# 方法1：使用配置脚本重新运行，选择删除旧任务
bash scripts/setup_cron.sh

# 方法2：手动编辑
crontab -e
# 删除RSS监控相关的任务行

# 方法3：命令行删除
crontab -l | grep -v 'rss' | crontab -
```

## 日志管理

### 日志位置

| 日志类型 | 路径 |
|----------|------|
| HTTP服务日志 | `logs/rss_service.log` |
| Cron执行日志 | `logs/cron_rss_monitor.log` |
| 工作流执行日志 | `/app/work/logs/bypass/app.log` |

### 查看日志

```bash
# 查看HTTP服务日志（实时）
tail -f logs/rss_service.log

# 查看最近的Cron执行记录
tail -n 50 logs/cron_rss_monitor.log

# 查看工作流日志
tail -f /app/work/logs/bypass/app.log

# 搜索错误信息
grep -i "error\|exception\|failed" logs/rss_service.log
```

### 日志清理

```bash
# 清理7天前的日志
find logs/ -name "*.log" -mtime +7 -delete

# 清理工作流日志（保留最近7天）
find /app/work/logs/bypass/ -name "*.log" -mtime +7 -delete
```

## 测试配置

### 手动触发一次RSS监控

```bash
# 方法1：直接运行flow模式
python src/main.py -m flow -i '{
  "rss_url": "https://cn.investing.com/rss/news_285.rss",
  "recipient_email": "529654431@qq.com"
}'

# 方法2：使用Cron执行脚本
bash scripts/cron_rss_monitor.sh

# 方法3：通过HTTP API
curl -X POST http://localhost:8000/api/v1/workflow/run \
  -H "Content-Type: application/json" \
  -d '{
    "rss_url": "https://cn.investing.com/rss/news_285.rss",
    "recipient_email": "529654431@qq.com"
  }'
```

### 验证邮件发送

检查你的邮箱 `529654431@qq.com`，应该收到主题为"RSS订阅更新"的邮件。

## 故障排查

### 问题1：服务启动失败

**症状**：运行 `start_rss_service.sh` 后提示启动失败

**解决方案**：
```bash
# 查看详细错误日志
cat logs/rss_service.log

# 检查端口是否被占用
lsof -i :8000

# 检查Python依赖
pip list | grep -E 'feedparser|smtplib|email'
```

### 问题2：Cron任务未执行

**症状**：到了时间点，Cron任务没有执行

**解决方案**：
```bash
# 检查Cron服务是否运行
sudo systemctl status cron

# 查看Cron服务日志
sudo tail -f /var/log/cron.log  # Ubuntu/Debian
# 或
sudo tail -f /var/log/syslog | grep CRON  # 部分系统

# 查看Cron任务执行日志
cat logs/cron_rss_monitor.log

# 检查crontab语法
crontab -l | crontab -v  # 如果支持
```

### 问题3：邮件发送失败

**症状**：工作流执行成功，但没有收到邮件

**解决方案**：
```bash
# 查看工作流日志
tail -f /app/work/logs/bypass/app.log | grep -i "email\|smtp"

# 检查邮件配置
# 邮件配置通过环境变量获取，确保已正确配置

# 手动测试邮件发送
python src/main.py -m flow -i '{
  "rss_url": "https://cn.investing.com/rss/news_285.rss",
  "recipient_email": "529654431@qq.com"
}'
```

### 问题4：重复发送邮件

**症状**：收到重复的邮件

**原因**：已处理的文章ID记录丢失

**解决方案**：
```bash
# 检查是否有持久化存储
# 当前实现每次运行都是独立的，processed_articles会重置

# 如果需要避免重复，可以考虑：
# 1. 使用数据库存储已处理的文章ID
# 2. 使用文件存储已处理的文章ID
# 3. 使用Redis等缓存存储
```

## 高级配置

### 修改RSS源

编辑 `scripts/setup_cron.sh` 文件，修改以下变量：

```bash
RSS_URL="https://your-rss-source.com/feed"
RECIPIENT_EMAIL="your-email@example.com"
```

然后重新运行：
```bash
bash scripts/setup_cron.sh
```

### 修改执行时间

编辑Cron任务：
```bash
crontab -e
```

Cron表达式格式：
```
┌───────────── 分钟 (0 - 59)
│ ┌───────────── 小时 (0 - 23)
│ │ ┌───────────── 日期 (1 - 31)
│ │ │ ┌───────────── 月份 (1 - 12)
│ │ │ │ ┌───────────── 星期 (0 - 7, 0和7都代表星期日)
│ │ │ │ │
* * * * * 命令
```

常用示例：
```bash
# 每小时执行
0 * * * * curl ...

# 每30分钟执行
*/30 * * * * curl ...

# 每天上午9点执行
0 9 * * * curl ...

# 每周一上午9点执行
0 9 * * 1 curl ...

# 每月1号上午9点执行
0 9 1 * * curl ...
```

### 添加多个RSS源

编辑 `scripts/setup_cron.sh`，添加多个Cron任务：

```bash
CRON_JOB1="0 * * * * curl -s -X POST http://localhost:8000/api/v1/workflow/run -H 'Content-Type: application/json' -d '{\"rss_url\": \"https://source1.com/feed\", \"recipient_email\": \"user@example.com\"}' >> ${LOG_DIR}/cron_rss_monitor.log 2>&1"

CRON_JOB2="0 * * * * curl -s -X POST http://localhost:8000/api/v1/workflow/run -H 'Content-Type: application/json' -d '{\"rss_url\": \"https://source2.com/feed\", \"recipient_email\": \"user@example.com\"}' >> ${LOG_DIR}/cron_rss_monitor.log 2>&1"
```

然后添加到crontab：
```bash
(crontab -l 2>/dev/null; echo "${CRON_JOB1}"; echo "${CRON_JOB2}") | crontab -
```

## 系统要求

- **操作系统**: Linux (Ubuntu, CentOS, Debian等)
- **Python**: 3.8+
- **服务**: cron 服务
- **依赖**: feedparser, coze-coding-dev-sdk

## 安全建议

1. **限制Cron日志权限**：
   ```bash
   chmod 600 logs/cron_rss_monitor.log
   ```

2. **使用环境变量管理敏感信息**：
   ```bash
   export RECIPIENT_EMAIL="your-email@example.com"
   ```

3. **定期清理日志**：
   ```bash
   # 添加日志清理任务
   0 2 * * * find /workspace/projects/logs/ -name "*.log" -mtime +7 -delete
   ```

## 监控和告警

### 创建健康检查脚本

创建 `scripts/health_check.sh`：

```bash
#!/bin/bash
# 服务健康检查脚本

PORT=8000
if lsof -Pi :${PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✓ 服务正常运行"
    exit 0
else
    echo "✗ 服务未运行"
    # 可以添加邮件告警
    exit 1
fi
```

### 添加健康检查到Cron

```bash
# 每5分钟检查一次服务状态
*/5 * * * * /workspace/projects/scripts/health_check.sh >> /workspace/projects/logs/health_check.log 2>&1
```

## 卸载

### 停止服务并清理

```bash
# 1. 停止HTTP服务
bash scripts/stop_rss_service.sh

# 2. 删除Cron任务
crontab -l | grep -v 'rss' | crontab -

# 3. 清理日志（可选）
rm -rf logs/

# 4. 验证清理
crontab -l
ps aux | grep main.py | grep -v grep
```

## 支持

如遇到问题，请查看：
1. 服务日志：`logs/rss_service.log`
2. Cron日志：`logs/cron_rss_monitor.log`
3. 工作流日志：`/app/work/logs/bypass/app.log`
