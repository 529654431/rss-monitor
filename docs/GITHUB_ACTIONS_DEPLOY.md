# GitHub Actions RSS监控部署指南

## 概述

GitHub Actions 是GitHub提供的自动化CI/CD服务，可以免费定时执行任务。本方案将RSS监控任务部署到GitHub Actions，实现**24/7自动运行**，无需服务器，完全免费。

## 优势

✅ **完全免费**：公开仓库有免费的GitHub Actions使用额度
✅ **无需服务器**：不需要购买或维护服务器
✅ **24/7运行**：GitHub服务器全天候运行
✅ **易于管理**：网页端管理，查看日志和状态
✅ **自动触发**：支持定时和手动触发
✅ **稳定可靠**：GitHub基础设施，高可用

## 免费额度说明

- **公开仓库**：无限制使用
- **私有仓库**：
  - 每月2000分钟免费额度
  - RSS监控任务约1-2分钟/次
  - 每小时执行一次：约720-1440分钟/月
  - 推荐使用**公开仓库**，避免额度限制

## 快速开始（5分钟部署）

### 步骤1：创建GitHub仓库

1. 访问 [GitHub](https://github.com) 并登录
2. 点击右上角 `+` → `New repository`
3. 填写仓库信息：
   - **Repository name**: `rss-monitor`（或任意名称）
   - **Description**: RSS订阅监控与邮件通知
   - **Public** ✅（**必须选择公开**，才能无限免费使用）
   - ⚠️ 不要勾选 "Add a README file"
   - ⚠️ 不要勾选 "Add .gitignore"
4. 点击 `Create repository`

### 步骤2：上传代码到GitHub

#### 方法A：使用GitHub CLI（推荐，最快速）

```bash
# 安装GitHub CLI（如果没有）
# Ubuntu/Debian: sudo apt install gh
# macOS: brew install gh

# 登录GitHub
gh auth login

# 初始化git仓库
git init
git add .
git commit -m "Initial commit: RSS monitor with GitHub Actions"

# 创建远程仓库并推送（替换YOUR_USERNAME）
gh repo create rss-monitor --public --source=. --remote=origin --push
```

#### 方法B：使用命令行上传

```bash
# 初始化git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: RSS monitor with GitHub Actions"

# 添加远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/rss-monitor.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

#### 方法C：使用GitHub网页上传

1. 在刚创建的仓库页面，点击 `uploading an existing file`
2. 将项目文件拖拽到上传区域
3. 填写提交信息：`Initial commit`
4. 点击 `Commit changes`

### 步骤3：验证GitHub Actions

1. 进入仓库页面
2. 点击 `Actions` 标签页
3. 应该看到名为 `RSS Monitor` 的工作流
4. 点击工作流，查看执行记录

### 步骤4：手动触发一次测试

1. 在 `Actions` 页面，点击 `RSS Monitor` 工作流
2. 点击右侧 `Run workflow` 按钮
3. 选择分支，点击绿色 `Run workflow` 按钮
4. 等待执行完成（约1-2分钟）

### 步骤5：检查邮件

查看你的邮箱 `529654431@qq.com`，应该收到RSS更新邮件。

**🎉 恭喜！部署完成！**

GitHub Actions会在**每小时**自动执行RSS监控任务。

## 定时任务配置

### 当前配置

工作流配置文件：`.github/workflows/rss-monitor.yml`

```yaml
on:
  schedule:
    - cron: '0 * * * *'  # 每小时执行一次（UTC时间）
```

### Cron表达式说明

GitHub Actions使用UTC时间，需要注意时区转换。

**UTC时间 vs 北京时间**：
- 北京时间 = UTC + 8小时
- 例如：UTC时间 0点 = 北京时间 8点

**常用Cron表达式**（UTC时间）：

| 执行频率 | Cron表达式 | 北京时间对应 |
|---------|-----------|------------|
| 每小时一次 | `0 * * * *` | 每小时8分、16分... |
| 每2小时 | `0 */2 * * *` | 每天8点、16点、0点 |
| 每6小时 | `0 */6 * * *` | 每天8点、14点、20点、2点 |
| 每天9点（北京时间） | `1 * * * *` | 每小时1分（UTC） |
| 每天上午9点（北京时间） | `1 1 * * *` | 每天9点（UTC 1点） |
| 每周一上午9点（北京时间） | `1 1 * * 1` | 每周一9点（UTC 1点） |

**时区转换工具**：
- 北京时间 → UTC时间：减去8小时
- 例如：北京时间 9:00 → UTC时间 1:00

### 修改执行频率

编辑 `.github/workflows/rss-monitor.yml` 文件：

```bash
# 1. 克隆仓库到本地（如果没有）
git clone https://github.com/YOUR_USERNAME/rss-monitor.git
cd rss-monitor

# 2. 编辑工作流文件
nano .github/workflows/rss-monitor.yml

# 3. 修改cron表达式
# 例如改为每2小时执行一次：
#   - cron: '0 */2 * * *'

# 4. 提交并推送
git add .github/workflows/rss-monitor.yml
git commit -m "Change cron schedule to every 2 hours"
git push origin main
```

修改后，GitHub Actions会自动使用新的配置。

## 查看执行日志

### 方法1：GitHub网页查看

1. 进入仓库页面
2. 点击 `Actions` 标签
3. 点击 `RSS Monitor` 工作流
4. 选择一次执行记录，查看详细日志

### 方法2：查看运行状态

```bash
# 使用GitHub CLI查看运行状态
gh run list --workflow=rss-monitor.yml

# 查看最近一次运行的日志
gh run view --log

# 查看指定运行的日志
gh run view RUN_ID --log
```

## 手动触发执行

### 方法1：GitHub网页触发

1. 进入仓库 → `Actions` 标签
2. 点击 `RSS Monitor` 工作流
3. 点击右侧 `Run workflow` 按钮
4. 选择分支，点击 `Run workflow`

### 方法2：使用GitHub CLI

```bash
# 手动触发工作流
gh workflow run rss-monitor.yml

# 查看运行状态
gh run list --workflow=rss-monitor.yml
```

## 修改配置

### 修改RSS源

编辑 `.github/workflows/rss-monitor.yml` 文件：

```yaml
env:
  RSS_URL: "https://your-new-rss-source.com/feed"
  RECIPIENT_EMAIL: "your-email@example.com"
```

### 修改收件人邮箱

同样在 `.github/workflows/rss-monitor.yml` 中修改：

```yaml
env:
  RECIPIENT_EMAIL: "new-email@example.com"
```

### 添加多个RSS源

创建新的工作流文件，例如 `.github/workflows/rss-monitor-2.yml`：

```yaml
name: RSS Monitor 2

on:
  schedule:
    - cron: '30 * * * *'  # 每小时30分执行

env:
  RSS_URL: "https://another-rss-source.com/feed"
  RECIPIENT_EMAIL: "your-email@example.com"

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python src/main.py -m flow -i '{"rss_url": "${{ env.RSS_URL }}", "recipient_email": "${{ env.RECIPIENT_EMAIL }}"}'
```

## 配置Secret（敏感信息）

如果不想在配置文件中暴露邮箱地址，可以使用GitHub Secrets。

### 添加Secret

1. 进入仓库 → `Settings` 标签
2. 左侧菜单 → `Secrets and variables` → `Actions`
3. 点击 `New repository secret`
4. 添加Secret：
   - Name: `RECIPIENT_EMAIL`
   - Value: `529654431@qq.com`
5. 点击 `Add secret`

### 在工作流中使用Secret

修改 `.github/workflows/rss-monitor.yml`：

```yaml
jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python src/main.py -m flow -i '{
          "rss_url": "https://cn.investing.com/rss/news_285.rss",
          "recipient_email": "${{ secrets.RECIPIENT_EMAIL }}"
        }'
```

## 故障排查

### 问题1：工作流未按时执行

**原因**：
- Cron表达式配置错误
- 时区转换错误
- GitHub Actions服务延迟（通常<5分钟）

**解决方案**：
1. 检查Cron表达式是否正确
2. 确认使用的是UTC时间
3. 查看 `Actions` 页面是否有执行记录
4. 手动触发测试：点击 `Run workflow`

### 问题2：邮件发送失败

**原因**：
- 邮件配置未正确设置
- 网络问题
- 邮箱服务限制

**解决方案**：
1. 查看工作流日志，定位错误信息
2. 在Actions页面点击执行记录，查看详细日志
3. 手动触发一次，查看实时日志
4. 检查邮箱是否在GitHub的邮件服务白名单中

### 问题3：任务执行超时

**原因**：
- RSS源响应慢
- 网络问题
- 超时限制（默认6小时）

**解决方案**：
```yaml
jobs:
  monitor:
    timeout-minutes: 10  # 设置超时时间为10分钟
    runs-on: ubuntu-latest
    steps:
      # ... 其他步骤
```

### 问题4：超过免费额度

**原因**：私有仓库使用免费额度有限

**解决方案**：
1. 将仓库设置为公开（Public）
2. 或升级GitHub付费计划
3. 或减少执行频率

## 高级功能

### 添加执行通知（可选）

使用GitHub Actions的通知功能，在执行成功/失败时发送通知。

#### 使用Slack通知

1. 在 `.github/workflows/rss-monitor.yml` 中添加：

```yaml
- name: Slack通知
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'RSS监控任务完成'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

2. 在 `Settings → Secrets` 添加Slack Webhook URL

#### 使用邮件通知

GitHub Actions原生支持邮件通知：

1. 进入 `Settings` → `Notifications`
2. 勾选 `Actions` → `Workflow run status changes`
3. 设置邮箱地址

### 添加条件执行

只在特定条件下执行任务：

```yaml
on:
  schedule:
    - cron: '0 * * * *'
  workflow_dispatch:

jobs:
  monitor:
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    steps:
      # ... 步骤
```

### 使用矩阵策略并行执行多个任务

```yaml
jobs:
  monitor:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        rss:
          - url: "https://source1.com/feed"
            email: "user1@example.com"
          - url: "https://source2.com/feed"
            email: "user2@example.com"
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python src/main.py -m flow -i '{
          "rss_url": "${{ matrix.rss.url }}",
          "recipient_email": "${{ matrix.rss.email }}"
        }'
```

## 监控和维护

### 查看执行统计

```bash
# 使用GitHub CLI查看统计信息
gh run list --workflow=rss-monitor.yml --json databaseId,conclusion,createdAt,displayTitle --jq '.[]'

# 统计成功/失败次数
gh run list --workflow=rss-monitor.yml --json conclusion --jq 'group_by(.conclusion) | map({key: .[0], count: length})'
```

### 设置执行历史保留

在工作流中添加：

```yaml
jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      # ... 步骤

      # 保留最近30天的日志
      - name: 清理旧日志
        if: always()
        uses: Mattraks/delete-workflow-runs@v2
        with:
          token: ${{ github.token }}
          repository: ${{ github.repository }}
          retain_days: 30
```

## 最佳实践

### 1. 使用公开仓库
- 无限制使用GitHub Actions
- 免费额度充足
- 代码可公开分享

### 2. 使用Secrets管理敏感信息
- 不要在代码中硬编码邮箱地址
- 使用GitHub Secrets存储敏感信息

### 3. 添加手动触发
- 保留 `workflow_dispatch` 触发方式
- 方便调试和测试

### 4. 监控执行状态
- 定期查看Actions页面
- 检查任务是否正常执行
- 及时处理错误

### 5. 优化执行时间
- 减少不必要的依赖安装
- 使用缓存加速构建
- 合理设置超时时间

## 成本估算

### 免费额度

| 类型 | 仓库类型 | 免费额度 |
|------|---------|---------|
| GitHub Actions | 公开仓库 | 无限制 |
| GitHub Actions | 私有仓库 | 2000分钟/月 |

### 实际使用量

**RSS监控任务**：
- 每次执行时间：约1-2分钟
- 每小时执行一次：24次/天
- 每月使用量：720-1440分钟

**结论**：
- 使用公开仓库：完全免费 ✅
- 使用私有仓库：接近免费额度限制 ⚠️

## 限制和注意事项

### 1. 时区问题
- GitHub Actions使用UTC时间
- 需要手动转换时区

### 2. 执行频率限制
- 最小间隔：1分钟
- 建议间隔：≥5分钟

### 3. 执行时长限制
- 公开仓库：6小时
- 私有仓库：6小时

### 4. 网络访问限制
- 部分地区可能无法访问GitHub
- RSS源需要可以被GitHub服务器访问

### 5. 邮件发送限制
- 某些邮箱服务可能限制发送频率
- 建议使用企业邮箱或专用邮件服务

## 卸载

如果需要停止GitHub Actions任务：

1. 进入仓库 → `Actions` 标签
2. 点击 `RSS Monitor` 工作流
3. 点击 `...` → `Disable workflow`
4. 确认禁用

或者删除工作流文件：

```bash
# 删除工作流文件
rm .github/workflows/rss-monitor.yml

# 提交更改
git add .github/workflows/rss-monitor.yml
git commit -m "Disable GitHub Actions workflow"
git push origin main
```

## 支持

- **GitHub Actions文档**: https://docs.github.com/en/actions
- **工作流语法**: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- **本仓库**: 查看Issues和Discussions

---

**🎉 现在你已经成功部署了RSS监控到GitHub Actions！**

任务会每小时自动执行，无需任何服务器，完全免费！
