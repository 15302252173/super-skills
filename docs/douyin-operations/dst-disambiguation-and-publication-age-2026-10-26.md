# 排期的重复时刻与发布龄：两项离线验收

核验日期：2026-10-26（北京时间；UTC 2026-10-25）。

本轮补充[制作复盘手册](video-production-operations-review-public.md)中的时区与发布龄检查。增量不是再写一遍“记住时区”，而是拦截不存在／有两个解释的本地时刻，并区分“次日同一钟点”与“经过 24 小时”。适用于跨时区制作、发布和复盘台账，不是抖音或小红书的新功能说明。

状态：已执行六个纯离线历史日期用例；没有实际排期、平台提交、账号数据或传播效果测量。现有完整视听、同版双审核、版本去重与发布授权要求不变。

## 一 排期先验证这个本地时刻是否存在且唯一

### 官方依据

Python 官方 `zoneinfo` 支持 IANA 时区规则与 `fold`；重复时刻的前后两次对应不同 UTC 偏移。模块优先读取系统时区数据，必要时使用独立 tzdata 包，因此软件版本与时区数据版本不是一回事。[Python zoneinfo](https://docs.python.org/3/library/zoneinfo.html)

PEP 495 将时钟回拨造成的重复区间称为 fold，前拨造成的缺失区间称为 gap；构造 datetime 或调用 replace 并不会自动拒绝所有无效本地时刻。能创建带时区对象，不等于排期有效。[PEP 495](https://peps.python.org/pep-0495/)

IANA 说明数据库会随时区边界、UTC 偏移及夏令时规则变更而更新。本轮官网列出的版本为 2026e；这不保证任何执行环境或平台已使用相同版本。[IANA Time Zones](https://www.iana.org/time-zones)

### 建议方法

在已有“日期、本地时间、IANA 时区、UTC 偏移、UTC 时间、平台时区依据”之外，增加三项：

- **候选 UTC 数量：** 本地时间转换到 UTC 再转回原时区。没有有效候选，标 `nonexistent`；两个不同候选，标 `ambiguous`；唯一候选才可进入后续核对。缺少时区数据或键名无效时标待核，不当作零候选。
- **歧义处理依据：** 重复时刻应明确选择较早或较晚那一次及其偏移；若平台不显示足够信息，保持待核，不默认选择第一次。不存在时刻不要静默顺延；选择替代时间仍需对应授权。
- **规则版本／核验日：** 保留转换所用数据版本。未来日期按该日期重新计算，不复用今天的偏移；规则更新后比对未执行计划，不能未经授权自动改已保存排期。

这是工程防错建议，不证明平台使用哪套时间库。即使本地转换唯一，也必须核平台页面与已保存条目；数学检查不能替代回读。

### 实验 A 四个合成排期输入

使用公开历史时区日期，避免把未来规则预测当作当前平台实测。预先期待的候选数依次为 2、0、1、1。

| 输入本地时间 | IANA 时区 | 本轮实际 UTC 候选 | 判定 |
| --- | --- | --- | --- |
| 2020-11-01 01:30 | America/Los_Angeles | 08:30Z、09:30Z（同日） | 重复，需明确选择 |
| 2020-03-08 02:30 | America/Los_Angeles | 无 | 不存在，拦截 |
| 2020-11-01 12:00 | America/Los_Angeles | 20:00Z（同日） | 唯一 |
| 2020-11-01 12:00 | Asia/Shanghai | 04:00Z（同日） | 唯一 |

“唯一”只表示本用例时间换算通过，不表示作品通过审核或平台已接受排期。洛杉矶仅为测试时区，不是建议更改运营时区。

## 二 用 UTC 经过时长算发布龄 不用本地日期差冒充

### 官方依据与方法推导

Python datetime 文档说明：带相同 tzinfo 的时间相减会忽略时区调整；加 timedelta 也不自动按 UTC 经过时长重算。直接在本地对象上加“一天”可能保留钟点，却不等于现实中经过 24 小时。[Python datetime 运算说明](https://docs.python.org/3.12/library/datetime.html#datetime-objects)

由此区分两种运营意图：

1. **固定本地钟点排期：** 按每个本地日期构建时刻，再做实验 A 的有效性检查；UTC 钟点可能随日期变化。
2. **固定发布龄采样：** 从已确认的实际公开时刻转换为 UTC，再加 24／72 小时；显示时可转回本地时区。若只知道大致公开时间，应保留精度限制，不填造精确发布龄。

建议记录 `actual_public_utc`、`sample_target_utc`、`sample_observed_utc`、实际经过小时与延迟。排期保存时刻、上传结束时刻不能替代实际公开时刻。自然日数据保留平台统计日边界，不与经过 24 小时窗口混算。

### 实验 B 两个跨切换日的采样输入

以下仍是历史日期合成用例，不是真实作品：

| 起点（America/Los_Angeles） | 次日同一钟点 | 实际经过 | 真正经过 24 小时的当地时间 |
| --- | --- | --- | --- |
| 2020-03-07 12:00 -08:00 | 03-08 12:00 -07:00 | 23 小时 | 03-08 13:00 -07:00 |
| 2020-10-31 12:00 -07:00 | 11-01 12:00 -08:00 | 25 小时 | 11-01 11:00 -08:00 |

本轮两个结果均符合预期。它们只证明“次日同钟点”与“24 小时后”在这两个用例中不相同，不证明所有地区都调整一小时，也不评价哪种发布钟点更有流量。

## 可复现检查

以下 Python 仅使用标准库和已存在的时区数据，无网络、无账号操作。缺数据时应停止并记录，不因本实验自行安装软件。

```python
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

UTC = timezone.utc

def candidates(s, key):
    wall = datetime.fromisoformat(s)  # 本实验输入不含偏移
    if wall.tzinfo is not None:
        raise ValueError("expected local wall time without offset")
    zone = ZoneInfo(key)
    valid = set()
    for fold in (0, 1):
        aware = wall.replace(tzinfo=zone, fold=fold)
        utc = aware.astimezone(UTC)
        back = utc.astimezone(zone)
        if back.replace(tzinfo=None) == wall:
            valid.add(utc.isoformat())
    return sorted(valid)

cases = [
    ("2020-11-01T01:30:00", "America/Los_Angeles", 2),
    ("2020-03-08T02:30:00", "America/Los_Angeles", 0),
    ("2020-11-01T12:00:00", "America/Los_Angeles", 1),
    ("2020-11-01T12:00:00", "Asia/Shanghai", 1),
]
for s, key, expected in cases:
    result = candidates(s, key)
    assert len(result) == expected
    print(s, key, result)

zone = ZoneInfo("America/Los_Angeles")
for s, expected_hours in [
    ("2020-03-07T12:00:00", 23),
    ("2020-10-31T12:00:00", 25),
]:
    start = datetime.fromisoformat(s).replace(tzinfo=zone)
    next_wall = start + timedelta(days=1)
    hours = (next_wall.astimezone(UTC) -
             start.astimezone(UTC)).total_seconds() / 3600
    after_24h = (start.astimezone(UTC) +
                 timedelta(hours=24)).astimezone(zone)
    assert hours == expected_hours
    print(next_wall.isoformat(), hours, after_24h.isoformat())
```

本轮执行条件：Python 3.12.14，系统时区数据库 2026b。四个候选数断言和两个经过时长断言全部通过（6/6）；表中数值为实际运行结果。此数据版本落后于核验日 IANA 官网列出的版本，因此本实验仅报告这些历史用例，不为当前或未来业务排期出具验证结论。未更新软件或时区数据，未连接发布平台。

## 下一步验证与停止条件

拟执行、尚未执行：在已有授权的只读检查范围内，取一个平台已保存计划的完整日期、显示钟点与可确认时区依据，独立换算并与条目回读对照。公开仓库不保存实际条目、后台截图或账号标识。

完成字段对照即可记录一致／不一致／证据不足；时区依据缺失、软件规则版本不明或显示无法消除歧义时停止在待核。发现差异先报告，不自动取消、重传或改排期。平台最终公开仍单独验收。

本轮仅核读公开官方文字并运行合成日期检查；不新增两平台发布规则断言，不声称完成真实排期或指标复盘。公开共享仅保留方法、可复现用例与公开链接。
