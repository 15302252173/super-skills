# 🖥️ RPA Skill — 桌面自动化

让OpenClaw像人一样看到屏幕、操控鼠标键盘。

## 能力

- **👁️ 看屏幕** — 截图并保存为PNG，AI可以读取分析
- **🖱️ 控制鼠标** — 移动、单击、双击、右键、拖拽
- **⌨️ 控制键盘** — 打字、快捷键、组合键
- **🪟 窗口管理** — 查找窗口、激活、获取位置
- **🌐 浏览器控制** — 通过Chrome CDP操控网页

## 文件

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 本文件 |
| `rpa.py` | Python RPA引擎（鼠标/键盘/截图） |
| `bridge.cjs` | Node.js桥接（与CDP联动） |

## 使用方式

### 截图
```bash
python rpa.py screenshot [文件路径]
```
默认保存到 `workspace/screenshots/screen_YYYYMMDD_HHMMSS.png`

### 鼠标
```bash
python rpa.py click [x] [y]          # 单击
python rpa.py dblclick [x] [y]       # 双击
python rpa.py rightclick [x] [y]     # 右键
python rpa.py move [x] [y]           # 移动
python rpa.py drag [x1] [y1] [x2] [y2]  # 拖拽
python rpa.py position               # 获取当前鼠标位置
```

### 键盘
```bash
python rpa.py type "要打的文字"       # 输入文字
python rpa.py press enter             # 按键
python rpa.py hotkey ctrl c           # 组合键
```

### 窗口
```bash
python rpa.py findwindow "窗口标题"   # 查找窗口位置
python rpa.py activewindow            # 获取当前活动窗口
```

## 依赖

```bash
pip install pyautogui pillow
```

## 注意事项

- 截图后用 `read` 工具分析屏幕内容
- 组合键用空格分隔：`ctrl c` = Ctrl+C
- 窗口标题支持模糊匹配
- 坐标是屏幕绝对像素坐标
