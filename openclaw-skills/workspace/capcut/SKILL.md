# 剪映自动化 Skill

触发：用户说"剪映""剪视频""CapCut""做视频"时激活

## 前提
- 剪映专业版已安装：https://www.capcut.cn/
- 未安装时提示用户安装

## 我负责
1. 找素材 → 下载到桌面
2. 写文案 → INFJ/指定风格
3. 生成配音 → Edge TTS / Windows TTS
4. 生成 SRT 字幕 → 可直接导入剪映
5. 遥控剪映 → 导入素材、加字幕、导出

## 剪映快捷键映射

| 操作 | 快捷键 |
|------|--------|
| 新建项目 | Ctrl+N |
| 导入素材 | Ctrl+I |
| 文本→智能字幕 | Ctrl+Shift+C |
| 导入字幕 | 拖拽 SRT 文件 |
| 导出 | Ctrl+M |
| 分割 | Ctrl+B |
| 删除 | Del |

## 工作流程

1. 用户给出参考视频链接或风格描述
2. 我分析风格/写文案
3. 我下载素材（或用户提供本地文件）
4. 我生成配音 WAV + SRT 字幕
5. 我打开剪映 → 导入素材 → 添加配音 → 导入字幕 → 导出

## 桌面操控实现

使用 PowerShell SendKeys 模拟键盘操作剪映。
关键函数：
- 打开剪映：`Start-Process jianyingpro`
- 等待窗口就绪
- 模拟快捷键：`[System.Windows.Forms.SendKeys]::SendWait("^n")`
