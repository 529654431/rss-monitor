#!/bin/bash

# RSS监控服务启动脚本
# 功能：启动工作流HTTP服务

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

# 检查服务是否已运行
if [ -f "${PID_FILE}" ]; then
    PID=$(cat "${PID_FILE}")
    if ps -p ${PID} > /dev/null 2>&1; then
        print_warn "服务已在运行 (PID: ${PID})"
        print_info "如需重启，请先运行: bash scripts/stop_rss_service.sh"
        exit 1
    else
        print_warn "发现残留的PID文件，正在清理..."
        rm -f "${PID_FILE}"
    fi
fi

# 检查端口是否被占用
if lsof -Pi :${PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_error "端口 ${PORT} 已被占用"
    print_info "请检查是否有其他服务正在使用该端口"
    exit 1
fi

print_info "正在启动RSS监控HTTP服务..."
print_info "工作目录: ${WORK_DIR}"
print_info "监听端口: ${PORT}"
print_info "日志目录: ${LOG_DIR}"

# 启动服务（后台运行）
nohup python ${WORK_DIR}/src/main.py -m http -p ${PORT} \
    > "${LOG_DIR}/rss_service.log" 2>&1 &

# 获取进程ID
PID=$!
echo ${PID} > "${PID_FILE}"

# 等待服务启动
sleep 3

# 检查服务是否成功启动
if ps -p ${PID} > /dev/null 2>&1; then
    print_info "✓ 服务启动成功!"
    print_info "PID: ${PID}"
    print_info "访问地址: http://localhost:${PORT}"
    print_info "API文档: http://localhost:${PORT}/docs"
    print_info ""
    print_info "查看日志: tail -f ${LOG_DIR}/rss_service.log"
    print_info "停止服务: bash scripts/stop_rss_service.sh"
else
    print_error "服务启动失败"
    print_info "查看日志: cat ${LOG_DIR}/rss_service.log"
    rm -f "${PID_FILE}"
    exit 1
fi
