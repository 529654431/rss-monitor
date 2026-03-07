#!/bin/bash

# RSS监控服务停止脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
WORK_DIR="${COZE_WORKSPACE_PATH:-$(dirname $(dirname $0))}"
LOG_DIR="${WORK_DIR}/logs"
PID_FILE="${LOG_DIR}/rss_service.pid"

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

# 检查PID文件是否存在
if [ ! -f "${PID_FILE}" ]; then
    print_warn "服务未运行 (PID文件不存在)"
    exit 0
fi

# 读取PID
PID=$(cat "${PID_FILE}")

# 检查进程是否存在
if ! ps -p ${PID} > /dev/null 2>&1; then
    print_warn "进程不存在 (PID: ${PID})"
    rm -f "${PID_FILE}"
    exit 0
fi

print_info "正在停止服务 (PID: ${PID})..."

# 优雅停止进程
kill ${PID}

# 等待进程结束
for i in {1..10}; do
    if ! ps -p ${PID} > /dev/null 2>&1; then
        print_info "✓ 服务已停止"
        rm -f "${PID_FILE}"
        exit 0
    fi
    sleep 1
done

# 强制杀死进程
print_warn "进程未响应，强制终止..."
kill -9 ${PID}
rm -f "${PID_FILE}"

print_info "✓ 服务已强制停止"
