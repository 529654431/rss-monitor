# 🚀 GitHub Actions 快速部署指南

## 3分钟快速部署RSS监控到GitHub Actions

### 前提条件
- GitHub账号（免费注册：https://github.com）
- Git工具（已安装）
- 本地项目代码已完成

---

## 步骤1：创建GitHub仓库（1分钟）

1. 访问 [GitHub](https://github.com) 并登录
2. 点击右上角 `+` → `New repository`
3. 填写：
   - **Repository name**: `rss-monitor`
   - **Public**: ✅ 勾选（必须公开才能免费无限使用）
4. 点击 `Create repository`

---

## 步骤2：上传代码（1分钟）

### 方法A：使用命令行（推荐）

```bash
# 进入项目目录
cd /workspace/projects

# 初始化git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: RSS monitor"

# 添加远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/rss-monitor.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 方法B：使用GitHub网页上传

1. 在刚创建的仓库页面，点击 `uploading an existing file`
2. 将项目文件夹拖拽到上传区域
3. 填写：`Initial commit`
4. 点击 `Commit changes`

---

## 步骤3：验证部署（1分钟）

1. 进入仓库页面
2. 点击 `Actions` 标签
3. 看到 `RSS Monitor` 工作流
4. 点击 `Run workflow` 手动触发一次测试

---

## 步骤4：检查邮件

查看你的邮箱 `529654431@qq.com`，应该收到RSS更新邮件。

---

## 🎉 完成！

GitHub Actions会**每小时自动执行**RSS监控任务，无需任何服务器！

---

## 常用操作

### 查看执行日志
1. 进入仓库 → `Actions` 标签
2. 点击 `RSS Monitor` 工作流
3. 选择一次执行记录查看日志

### 手动触发任务
1. 进入仓库 → `Actions` 标签
2. 点击 `RSS Monitor` → `Run workflow`

### 修改执行频率
编辑 `.github/workflows/rss-monitor.yml` 文件：

```yaml
schedule:
  - cron: '0 */2 * * *'  # 改为每2小时执行
```

### 修改RSS源或邮箱
编辑 `.github/workflows/rss-monitor.yml` 文件：

```yaml
env:
  RSS_URL: "https://your-new-rss-source.com/feed"
  RECIPIENT_EMAIL: "new-email@example.com"
```

---

## 重要提示

### ⚠️ 必须使用公开仓库
- **公开仓库**：无限制使用GitHub Actions ✅
- **私有仓库**：每月只有2000分钟免费额度 ⚠️

### ⏰ 时区说明
- GitHub Actions使用UTC时间
- 北京时间 = UTC + 8小时
- 例如：UTC时间 0点 = 北京时间 8点

### 📧 邮件配置
- 邮件配置通过GitHub环境变量自动获取
- 无需手动配置SMTP服务器

---

## 故障排查

### 任务未按时执行？
- 检查Cron表达式是否正确
- 手动触发测试：`Actions → RSS Monitor → Run workflow`

### 邮件未收到？
- 查看Actions日志，定位错误信息
- 检查邮箱垃圾邮件文件夹

### 超过免费额度？
- 将仓库设置为公开（Public）
- 或减少执行频率

---

## 详细文档

完整文档请查看：[GitHub Actions部署指南](GITHUB_ACTIONS_DEPLOY.md)

---

## 💡 小贴士

1. **使用GitHub CLI加速部署**：
   ```bash
   # 安装GitHub CLI
   brew install gh  # macOS
   sudo apt install gh  # Ubuntu

   # 一键创建仓库并推送
   gh repo create rss-monitor --public --source=. --remote=origin --push
   ```

2. **添加多个RSS源**：
   创建多个工作流文件，例如 `.github/workflows/rss-monitor-2.yml`

3. **使用Secrets保护敏感信息**：
   - `Settings` → `Secrets and variables` → `Actions`
   - 添加 `RECIPIENT_EMAIL` 等Secret

---

## 成本

**完全免费！**

- 公开仓库：无限制使用GitHub Actions
- 无需购买服务器
- 无需支付任何费用

---

## 支持与反馈

- **问题反馈**: GitHub Issues
- **文档**: [GitHub Actions文档](https://docs.github.com/en/actions)

---

**🎊 享受免费的24/7 RSS监控服务！**
