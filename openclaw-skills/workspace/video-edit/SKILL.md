# Video Editing Skill

Trigger: 用户说"剪视频""剪辑""编辑视频""做一条视频""video edit"时激活。

## 工作流程

用户只需发送参考视频链接或描述想要的风格，我全自动完成：

1. 分析参考视频风格（节奏、转场、色调、字幕风格）
2. 下载/收集素材
3. 用 ffmpeg 自动剪辑 → 输出最终视频

## 依赖
- ffmpeg.exe 路径: `%APPDATA%/npm/node_modules/@ffmpeg-installer/win32-x64/ffmpeg.exe`
- 纯 ffmpeg 滤镜链，无需 Python/pip/whisper/GPU

## 剪辑能力

| 功能 | ffmpeg 实现 |
|------|-----------|
| 静音检测+自动切 | silencedetect + trim |
| 30ms 音频淡入淡出 | afade |
| 调色（电影风/清新/复古） | eq + colorbalance + curves |
| 字幕叠加 | drawtext (SRT→ASS→硬编码) |
| 转场效果 | xfade (dissolve/fade/pixelize) |
| 变速 | setpts/atempo |
| 画中画 | overlay |
| 缩放裁剪 | scale + crop |

## 角色分工

| 我（AI）做 | ffmpeg 做 |
|-----------|----------|
| 分析参考视频风格 | 实际渲染编码 |
| 决定剪切点、顺序 | 静音检测 |
| 生成字幕文本 | 字幕叠加渲染 |
| 选择调色参数 | 色彩滤镜 |
| 编排转场节奏 | 转场合成 |
| QA 检查输出 | 输出 final.mp4 |
