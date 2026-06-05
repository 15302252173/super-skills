---
name: niu-er
description: 启动 FeiControl 开发服务器 (端口 3001)。当用户说“牛二启动”时触发，自动启动 Next.js 开发服务。
---

# 牛二 (Niu-Er) - FeiControl 启动器

## 概述
一键启动 `FeiControl` 项目的开发服务器，自动处理端口冲突并绑定到 `http://127.0.0.1:3001`。

## 触发条件
当用户说“牛二启动”或“启动牛二”时执行此技能。

## 工作流程

### 1. 检查项目是否存在
- 确认 `C:\Users\L7384\.openclaw\workspace\FeiControl` 目录存在
- 确认 `package.json` 存在且包含 `dev` 脚本

### 2. 启动开发服务器
执行以下命令（使用 `cmd` 以绕过 PowerShell 执行策略限制）：
```cmd
cmd /c "cd /d C:\Users\L7384\.openclaw\workspace\FeiControl && npm run dev"
```

### 3. 监控启动状态
- 等待服务器就绪（通常 3-5 秒）
- 确认输出包含 `✓ Ready in X.Xs`
- 记录实际绑定的端口（可能是 3000 或 3001）

### 4. 报告结果
向用户报告：
- ✅ 启动成功
- 🌐 访问地址（如 `http://127.0.0.1:3001`）
- ⚠️ 任何警告（如端口切换、弃用提示等）

## 注意事项
- 如果 3000 端口被占用，自动切换到 3001
- 服务器在后台运行，不阻塞当前会话
- 使用 `cmd` 执行以兼容 Windows PowerShell 执行策略
- 记录进程 ID 以便后续管理

## 示例响应
```
✅ 牛二已启动！

🌐 访问地址：http://127.0.0.1:3001
📂 项目路径：C:\Users\L7384\.openclaw\workspace\FeiControl
⚙️ 运行命令：npm run dev
⏱️ 启动时间：3.6 秒

服务器正在后台运行，你可以直接打开浏览器访问。
```

## 后续操作
- 如需停止：告诉用户可以使用 `Ctrl+C` 或在任务管理器中结束 `node` 进程
- 如需重启：再次触发此技能
