#!/bin/bash

# Cron定时任务配置脚本
# 功能：设置每小时运行一次RSS监控任务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
WORK_DIR="${COZE_WORKSPACE_PATH:-$(dirname $(dirname $0))}"
LOG_DIR="${WORK_DIR}/logs"
RSS_URL="https://cn.investing.com/rss/news_285.rss"
RECIPIENT_EMAIL="529654431@qq.com"
CRON_LOG="${LOG_DIR}/cron_rss_monitor.log"
PORT=8000

# 打印信息函数
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 创建日志目录
mkdir -p "${LOG_DIR}"

print_info "========================================="
print_info "  RSS监控Cron定时任务配置工具"
print_info "========================================="
print_info ""
print_info "配置信息："
print_info "  RSS源: ${RSS_URL}"
print_info "  收件人: ${RECIPIENT_EMAIL}"
print_info "  执行频率: 每小时一次"
print_info "  服务端口: ${PORT}"
print_info "  日志文件: ${CRON_LOG}"
print_info ""

# 检查服务是否运行
if ! lsof -Pi :${PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_warn "HTTP服务未运行"
    print_info "请先启动服务: bash scripts/start_rss_service.sh"
    read -p "是否现在启动服务? (y/n): " START_SERVICE
    if [ "$START_SERVICE" = "y" ] || [ "$START_SERVICE" = "Y" ]; then
        bash "${WORK_DIR}/scripts/start_rss_service.sh"
    else
        print_error "服务未启动，无法设置Cron任务"
        exit 1
    fi
fi

# 生成Cron任务
CRON_JOB="0 * * * * curl -s -X POST http://localhost:${PORT}/api/v1/workflow/run -H 'Content-Type: application/json' -d '{\"rss_url\": \"${RSS_URL}\", \"recipient_email\": \"${RECIPIENT_EMAIL}\"}' >> ${CRON_LOG} 2>&1"

print_info "生成的Cron任务："
print_info "${CRON_JOB}"
print_info ""

# 备份现有crontab
print_info "备份现有crontab..."
crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null || true

# 检查是否已存在RSS监控任务
if crontab -l 2>/dev/null | grep -q "rss.*monitor\|RSS.*监控"; then
    print_warn "检测到已存在的RSS监控任务"
    read -p "是否删除旧的任务并重新设置? (y/n): " REPLACE_TASK
    if [ "$REPLACE_TASK" = "y" ] || [ "$REPLACE_TASK" = "Y" ]; then
        # 删除旧的任务
        crontab -l 2>/dev/null | grep -v "rss.*monitor\|RSS.*监控" | crontab -
        print_info "已删除旧的任务"
    else
        print_error "操作已取消"
        exit 0
    fi
fi

# 添加新的Cron任务
print_info "正在添加Cron任务..."
(crontab -l 2>/dev/null; echo "${CRON_JOB}") | crontab -

print_info "✓ Cron定时任务已设置!"
print_info ""
print_info "验证Cron任务："
crontab -l | grep -A 1 "rss.*monitor\|RSS.*监控" || true
print_info ""
print_info "查看Cron日志："
print_info "  tail -f ${CRON_LOG}"
print_info ""
print_info "查看所有Cron任务："
print_info "  crontab -l"
print_info ""
print_info "删除Cron任务："
print_info "  crontab -e  # 手动删除或运行: crontab -l | grep -v 'rss' | crontab -"
print_info ""
