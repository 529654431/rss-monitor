#!/bin/bash

# RSS监控执行脚本
# 功能：直接执行RSS监控任务（可被Cron调用）

set -e

# 配置
WORK_DIR="${COZE_WORKSPACE_PATH:-$(dirname $(dirname $0))}"
LOG_DIR="${WORK_DIR}/logs"
RSS_URL="https://cn.investing.com/rss/news_285.rss"
RECIPIENT_EMAIL="529654431@qq.com"
EXEC_LOG="${LOG_DIR}/rss_exec_$(date +%Y%m%d_%H%M%S).log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 创建日志目录
mkdir -p "${LOG_DIR}"

echo "========================================" | tee -a "${EXEC_LOG}"
echo "RSS监控执行时间: ${TIMESTAMP}" | tee -a "${EXEC_LOG}"
echo "========================================" | tee -a "${EXEC_LOG}"

# 执行工作流
cd "${WORK_DIR}"
python src/main.py -m flow -i "{\"rss_url\": \"${RSS_URL}\", \"recipient_email\": \"${RECIPIENT_EMAIL}\"}" 2>&1 | tee -a "${EXEC_LOG}"

echo "" | tee -a "${EXEC_LOG}"
echo "执行完成" | tee -a "${EXEC_LOG}"
echo "========================================" | tee -a "${EXEC_LOG}"
