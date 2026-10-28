#!/usr/bin/env python3
"""Three offline scheduling-time experiments; no platform calls or real schedules.

Requires Python 3.9+ and an already available IANA timezone database.
Runs unittest assertions before emitting a synthetic JSON report. No installation,
network access, credentials, file writes, or scheduling side effects.
"""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import unittest
from zoneinfo import TZPATH, ZoneInfo, ZoneInfoNotFoundError

UTC = timezone.utc
BJ_KEY = "Asia/Shanghai"
UI_KEY = "America/Los_Angeles"  # Explicit hypothetical UI, not platform detection.


def confirmed_ui_zone(key, *, confirmed):
    """A caller assertion is a gate, not evidence that a platform uses this zone."""
    if not confirmed or not isinstance(key, str) or not key.strip():
        raise ValueError("UI timezone is unknown or unconfirmed")
    return ZoneInfo(key)


def require_aware(value):
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("An aware instant is required; do not assume the OS zone")


def convert_instant(value, key, *, confirmed=False):
    require_aware(value)
    return value.astimezone(confirmed_ui_zone(key, confirmed=confirmed))


def elapsed_seconds(start, end):
    require_aware(start)
    require_aware(end)
    return (end.astimezone(UTC) - start.astimezone(UTC)).total_seconds()


def valid_instants(wall, zone):
    """Return UTC candidates surviving a wall -> UTC -> wall round trip.

    Zero candidates means a gap; two means a fold. UTC keys avoid same-tzinfo
    datetime equality treating two folds as the same wall time.
    """
    if wall.tzinfo is not None:
        raise ValueError("Pass a naive wall label, not an already aware instant")
    result = set()
    for fold in (0, 1):
        candidate = wall.replace(tzinfo=zone, fold=fold).astimezone(UTC)
        returned = candidate.astimezone(zone).replace(tzinfo=None, fold=0)
        if returned == wall.replace(fold=0):
            result.add(candidate)
    return sorted(result)


def resolve_wall(wall, key, *, confirmed=False, fold=None):
    """Resolve a hypothetical UI label only when its interpretation is unique."""
    zone = confirmed_ui_zone(key, confirmed=confirmed)
    candidates = valid_instants(wall, zone)
    if not candidates:
        raise ValueError("Nonexistent local time (DST gap)")
    if fold is not None and fold not in (0, 1):
        raise ValueError("fold must be 0 or 1")
    if len(candidates) > 1 and fold is None:
        raise ValueError("Ambiguous local time: explicit fold/instant required")
    if fold is None:
        return candidates[0]
    selected = [c for c in candidates if c.astimezone(zone).fold == fold]
    if len(selected) != 1:
        raise ValueError("The requested fold does not identify a valid instant")
    return selected[0]


def synthetic_rows():
    bj = ZoneInfo(BJ_KEY)
    rows = []
    for day in (datetime(2026, 10, 31), datetime(2026, 11, 1), datetime(2026, 11, 2)):
        for hour in (12, 18):
            source = day.replace(hour=hour, tzinfo=bj)
            ui = convert_instant(source, UI_KEY, confirmed=True)
            back = ui.astimezone(bj)
            rows.append({
                "beijing": source.isoformat(), "ui": ui.isoformat(),
                "utc": ui.astimezone(UTC).isoformat(), "fold": ui.fold,
                "round_trip": back.isoformat(),
            })
    return rows


class SchedulingExperiments(unittest.TestCase):
    def test_1_each_instant_and_round_trip(self):
        expected = [
            "2026-10-30T21:00:00-07:00", "2026-10-31T03:00:00-07:00",
            "2026-10-31T21:00:00-07:00", "2026-11-01T02:00:00-08:00",
            "2026-11-01T20:00:00-08:00", "2026-11-02T02:00:00-08:00",
        ]
        rows = synthetic_rows()
        self.assertEqual([r["ui"] for r in rows], expected)
        for row in rows:
            with self.subTest(beijing=row["beijing"]):
                self.assertEqual(row["beijing"], row["round_trip"])
                self.assertEqual(datetime.fromisoformat(row["beijing"]).astimezone(UTC),
                                 datetime.fromisoformat(row["ui"]).astimezone(UTC))
        # Neither a fixed 15-hour nor a fixed 16-hour subtraction works for all rows.
        for hours in (15, 16):
            mismatch = sum(
                datetime.fromisoformat(r["beijing"]).replace(tzinfo=None)
                - timedelta(hours=hours)
                != datetime.fromisoformat(r["ui"]).replace(tzinfo=None)
                for r in rows
            )
            self.assertEqual(mismatch, 3)

    def test_2_elapsed_time_and_fold_identity(self):
        zone = ZoneInfo(UI_KEY)
        bj = ZoneInfo(BJ_KEY)
        start = datetime(2026, 11, 1, 12, tzinfo=bj).astimezone(zone)
        end = datetime(2026, 11, 1, 18, tzinfo=bj).astimezone(zone)
        self.assertEqual((end - start).total_seconds(), 5 * 3600)
        self.assertEqual(elapsed_seconds(start, end), 6 * 3600)
        first = datetime(2026, 11, 1, 1, 30, tzinfo=zone, fold=0)
        second = first.replace(fold=1)
        self.assertEqual(first, second)  # Documented same-tzinfo wall-time semantics.
        self.assertEqual(len({first, second}), 1)
        self.assertEqual(len({first.astimezone(UTC), second.astimezone(UTC)}), 2)
        self.assertEqual(elapsed_seconds(first, second), 3600)

    def test_3_fail_closed_for_unknown_gap_and_fold(self):
        wall = datetime(2026, 11, 1, 1, 30)
        for key, confirmed in ((None, True), (UI_KEY, False), ("", True)):
            with self.subTest(key=key, confirmed=confirmed), self.assertRaises(ValueError):
                resolve_wall(wall, key, confirmed=confirmed)
        with self.assertRaises(ZoneInfoNotFoundError):
            resolve_wall(wall, "Invalid/Not_A_Zone", confirmed=True)
        with self.assertRaises(ValueError):
            convert_instant(wall, UI_KEY, confirmed=True)
        with self.assertRaises(ValueError):
            elapsed_seconds(wall, wall)
        with self.assertRaises(ValueError):
            resolve_wall(datetime(2026, 3, 8, 2, 30), UI_KEY, confirmed=True)
        with self.assertRaises(ValueError):
            resolve_wall(wall, UI_KEY, confirmed=True)
        first = resolve_wall(wall, UI_KEY, confirmed=True, fold=0)
        second = resolve_wall(wall, UI_KEY, confirmed=True, fold=1)
        self.assertEqual(first.isoformat(), "2026-11-01T08:30:00+00:00")
        self.assertEqual(second.isoformat(), "2026-11-01T09:30:00+00:00")
        self.assertEqual(elapsed_seconds(first, second), 3600)
        normal = resolve_wall(datetime(2026, 11, 1, 2, 30), UI_KEY, confirmed=True)
        self.assertEqual(normal.isoformat(), "2026-11-01T10:30:00+00:00")
        with self.assertRaises(ValueError):
            resolve_wall(wall, UI_KEY, confirmed=True, fold=2)
        with self.assertRaises(ValueError):
            resolve_wall(datetime(2026, 11, 1, 2, 30), UI_KEY, confirmed=True, fold=1)


def tzdata_release_if_available():
    """Report metadata only; do not expose local filesystem paths or infer versions."""
    for root in TZPATH:
        metadata = Path(root) / "tzdata.zi"
        if metadata.is_file():
            with metadata.open(encoding="utf-8") as source:
                first = source.readline().strip()
            if first.startswith("# version "):
                return first.removeprefix("# version ")
    return "not reported by system metadata"


def main():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SchedulingExperiments)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    print(json.dumps({
        "scope": "synthetic offline examples; no detected UI timezone or platform operations",
        "python": sys.version.split()[0],
        "system_tzdata_release_if_available": tzdata_release_if_available(),
        "experiment_groups_passed": result.testsRun,
        "conversion_rows": synthetic_rows(),
        "interval_example": {"same_zone_wall_hours": 5, "utc_elapsed_hours": 6},
        "fold_example": {"wall_label": "2026-11-01 01:30 America/Los_Angeles",
                         "distinct_utc_instants": 2, "elapsed_seconds": 3600},
        "rejected": ["unknown or unconfirmed UI zone", "invalid IANA key", "naive instant",
                     "nonexistent spring time", "ambiguous fall time without fold",
                     "invalid fold"],
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
