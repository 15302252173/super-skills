#!/usr/bin/env python3
"""Offline synthetic frame-window regression; no real footage or rights verdict."""
import json
import subprocess
import tempfile
from pathlib import Path

W, H, COUNT = 32, 24, 60
SIZE = W * H

def run(*args, data=None):
    return subprocess.run(args, input=data, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=True).stdout

def frames(raw):
    assert len(raw) % SIZE == 0
    return [raw[i:i + SIZE] for i in range(0, len(raw), SIZE)]

def main():
    source = [bytes([n]) * SIZE for n in range(COUNT)]
    expected = source[15:45]
    with tempfile.TemporaryDirectory(prefix="shot-boundary-") as tmp:
        clip = str(Path(tmp) / "synthetic.mkv")
        run("ffmpeg", "-v", "error", "-n", "-f", "rawvideo", "-pix_fmt", "gray",
            "-s", f"{W}x{H}", "-r", "30", "-i", "pipe:0", "-an", "-c:v", "ffv1", clip,
            data=b"".join(source))
        def trim(end):
            return frames(run("ffmpeg", "-v", "error", "-i", clip, "-vf",
                              f"trim=start_frame=15:end_frame={end},setpts=PTS-STARTPTS",
                              "-an", "-fps_mode", "passthrough", "-pix_fmt", "gray",
                              "-f", "rawvideo", "pipe:1"))
        good = trim(45)
        bad_end = trim(46)
        assert good == expected
        assert len(bad_end) == 31 and bad_end[-1] == source[45]
        assert bad_end != expected
        # Synthetic one-frame corner overlay, standing in for stale text/branding.
        contaminated = list(good)
        changed = bytearray(contaminated[14])
        changed[:4] = b"\xff" * 4
        contaminated[14] = bytes(changed)
        sparse = [0, len(good) // 2, len(good) - 1]
        assert all(contaminated[n] == expected[n] for n in sparse)
        differences = [n for n, (a, b) in enumerate(zip(contaminated, expected)) if a != b]
        assert differences == [14]
        # Validate adjacent windows partition the source, without a duplicated boundary.
        adjacent = frames(run("ffmpeg", "-v", "error", "-i", clip, "-vf",
                             "trim=start_frame=45:end_frame=60,setpts=PTS-STARTPTS",
                             "-an", "-fps_mode", "passthrough", "-pix_fmt", "gray",
                             "-f", "rawvideo", "pipe:1"))
        assert good + adjacent == source[15:60]
        print(json.dumps({"correct_window_frames": len(good), "first_source_frame": good[0][0],
                          "last_source_frame": good[-1][0], "off_by_one_frames": len(bad_end),
                          "off_by_one_rejected": True, "sparse_checked": sparse,
                          "sparse_missed_overlay": True, "full_scan_difference_frames": differences,
                          "adjacent_partition_passed": True}, indent=2))

if __name__ == "__main__":
    main()
