const fs = require("fs");
const path = require("path");

const ROOT = path.join(process.cwd(), "src");

// Only replace text that appears in JSX (between tags, as text content)
// Pattern: immediately preceded by > or inside JSX expression
const REPLACEMENTS = {
  // Login page
  "Enter your password": "输入密码",
  ">Sign In<": ">登录<",
  '"Verifying..."': '"验证中..."',
  "Incorrect password": "密码错误",
  "Connection error": "连接失败",

  // TopBar
  "Search... ⌘K": "搜索... ⌘K",

  // StatusBar
  "label=\"处理器\"": "label=\"处理器\"", // already done
  "label=\"内存\"": "label=\"内存\"", // already done
  "label=\"磁盘\"": "label=\"磁盘\"", // already done
  "Uptime: ": "运行时间：", // already done

  // Generic page titles and UI text
  "Settings\n": "设置\n",
  "Quick Actions": "快捷操作",
  "Scheduled Tasks": "定时任务",
  "File Browser": "文件浏览器",
  "Browse agent workspaces and files": "浏览工作区和文件",

  // Buttons
  ">Run<": ">执行<",
  "Running...": "执行中...",
  ">Cancel<": ">取消<",
  "Force Execute": "强制执行",
  "Recent Results": "最近结果",
  ">Refresh<": ">刷新<",
  "Last updated": "上次更新",
  ">View Details<": ">查看详情<",
  ">Save<": ">保存<",
  ">Delete<": ">删除<",
  ">Edit<": ">编辑<",
  ">Create<": ">创建<",
  ">Add<": ">添加<",

  // Status / States
  "Loading...": "加载中...",
  "Unable to fetch": "无法获取",
  "No results found": "未找到结果",
  "No recent results": "暂无最近结果",
  "No cron tasks configured": "未配置定时任务",
  "Recent results will appear here": "最近结果将显示在此处",
  "Search files...": "搜索文件...",
  "Search commands...": "搜索命令...",

  // About page
  "Failed to fetch system data:": "获取系统数据失败：",

  // Error
  "System status, integrations, and configuration": "系统状态、集成与配置",
  "Failed to load files": "加载文件失败",
  "Failed to load file tree": "加载文件树失败",
  "Quick Commands": "快速命令",

  // Footer
  "OpenClaw Agent Dashboard": "OpenClaw 控制面板",

  // Workspace
  ">Workspaces<": ">工作区<",
  "Search...": "搜索...",

  // Generic
  "Close": "关闭",
  "Total": "总计",
  "Active": "活跃",
  "Inactive": "未激活",
  "Enabled": "已启用",
  "Disabled": "已禁用",
};

let count = 0;

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const f of entries) {
    const fp = path.join(dir, f.name);
    if (f.isDirectory() && f.name !== "node_modules") {
      walk(fp);
    } else if (f.name.endsWith(".tsx") || f.name.endsWith(".ts")) {
      let c = fs.readFileSync(fp, "utf-8");
      let changed = false;

      // First pass: only replace patterns that exactly match JSX text
      for (const [from, to] of Object.entries(REPLACEMENTS)) {
        if (c.includes(from)) {
          c = c.replaceAll(from, to);
          changed = true;
        }
      }

      if (changed) {
        fs.writeFileSync(fp, c, "utf-8");
        count++;
        const rel = path.relative(ROOT, fp);
        console.log("✅", rel);
      }
    }
  }
}

walk(ROOT);
console.log(`\nDone! Modified ${count} files.`);
