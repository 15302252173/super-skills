# 超级skills 🦸

牛二办公室 (FeiControl) 使用的全套 AI Agent Skills 和上下文持久化方案。

## 目录结构

```
super-skills/
├── context/          # Agent 上下文文件
│   ├── AGENTS.md     # 行为准则和工作区规则
│   ├── SOUL.md       # Agent 人格定义
│   ├── IDENTITY.md   # Agent 身份信息
│   ├── MEMORY.md     # 长期记忆
│   ├── TOOLS.md      # 本地工具配置
│   ├── USER.md       # 用户偏好
│   └── HEARTBEAT.md  # 心跳检查任务
├── user-skills/      # 用户自定义 Skill
├── dbs-skills/       # dontbesilent 商业诊断工具箱 (17个)
├── docs/             # 学习手册与实践模板
├── memory/           # 每日记忆示例
└── README.md
```

## 核心方案

### 上下文持久化 — 解决 AI Agent "失忆" 问题

每次会话重启，Agent 都会"失忆"。这套文件是 Agent 的长期记忆系统：

| 文件 | 作用 |
|------|------|
| AGENTS.md | 定义 Agent 行为：何时说话、何时沉默、如何组织工作 |
| SOUL.md | Agent 人格：语气、边界、价值观 |
| IDENTITY.md | 身份：名字、emoji、人设 |
| MEMORY.md | 长期记忆：重要决策、偏好、经验教训 |
| USER.md | 用户信息：称呼、时区、偏好 |
| TOOLS.md | 本地配置：SSH、摄像头、TTS 等设备信息 |
| HEARTBEAT.md | 心跳任务清单：定期检查邮件、日历等 |
| memory/YYYY-MM-DD.md | 每日工作日志 |

### 关键 Skill

| Skill | 功能 |
|-------|------|
| **niu-er** | 一键启动 FeiControl 开发服务器 |
| **dispatch** | Agent 调度模式 |
| **dbs-diagnosis** | 商业模式诊断 |
| **dbs-benchmark** | 对标分析（五重过滤法） |
| **dbs-content** | 内容创作诊断 |
| **dbs-hook** | 短视频开头优化 |
| **dbs-xhs-title** | 小红书标题公式 |
| **dbs-ai-check** | AI 写作特征检测 |
| **dbs-action** | 执行力诊断（阿德勒心理学） |
| **dbs-slowisfast** | 慢就是快方法论 |
| **dbs-goal** | 目标清晰化（维特根斯坦） |
| **dbs-deconstruct** | 概念拆解 |
| **dbs-chatroom** | 定向聊天室（多角色对话） |
| **dbs-save/restore/report** | 状态管理三件套 |
| **dbs-agent-migration** | Agent 工作台迁移 |

## 学习手册

- [抖音运营学习手册](docs/douyin-operations/README.md)：从选题、脚本、字幕和发布检查，到数据复盘与小步实验；区分官方公开依据、方法建议与待验证假设。

## 安装到新设备

```bash
# 1. 复制上下文文件到 OpenClaw workspace
cp context/*/*.md ~/.openclaw/workspace/

# 2. 安装 skills
cp -r user-skills/* ~/.openclaw/workspace/skills/
cp -r dbs-skills/* ~/.openclaw/workspace/.agents/skills/

# 3. 创建 memory 目录
mkdir -p ~/.openclaw/workspace/memory/

# 4. 重启 OpenClaw
```

## 使用说明

新设备上部署后，Agent 会自动读取这些文件获取：
- ✅ 知道自己的名字和性格
- ✅ 知道用户是谁、偏好什么
- ✅ 记住历史决策和重要信息
- ✅ 拥有全部商业诊断工具
- ✅ 理解工作区规则和行为边界
