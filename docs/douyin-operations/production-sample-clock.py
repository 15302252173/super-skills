#!/usr/bin/env python3
"""20段整数PCM样本时钟；不调用TTS，不验证听感，不渲染影片。"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tempfile
import wave


def ceil_fraction(x):
    return -(-x.numerator // x.denominator)


def boundaries(counts, rate, fps):
    if rate <= 0 or fps <= 0 or not counts or any(n <= 0 for n in counts):
        raise ValueError('采样率、帧率和每段样本数必须为正')
    result, total, last = [], 0, 0
    for i, n in enumerate(counts, 1):
        start = total
        total += n
        end = ceil_fraction(Fraction(total, rate) * fps)
        result.append(dict(id=f'S{i:02}', start_sample=start, end_sample=total,
                           start_frame=last, end_frame=end, video_frames=end-last))
        last = end
    return result


def build(audio, out, fps):
    # 完成全部输入验证后才创建输出目录；不覆盖已有版本。
    chunks, counts, inputs = [], [], []
    fmt = None
    for i in range(1, 21):
        p = audio / f'S{i:02}.wav'
        with wave.open(str(p), 'rb') as w:
            # Python 3.15 新增浮点WAV支持；必须排除浮点字节被写成整数PCM。
            if hasattr(w, 'getformat') and w.getformat() != wave.WAVE_FORMAT_PCM:
                raise ValueError(f'{p.name}: 仅接受整数PCM，不接受IEEE float')
            current = (w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getcomptype())
            if current[3] != 'NONE' or current[1] not in (1, 2, 3, 4):
                raise ValueError(f'{p.name}: 需要整数PCM WAV')
            if fmt is None:
                fmt = current
            if current != fmt:
                raise ValueError(f'{p.name}: 音频格式不一致，先明确转换再重新对齐')
            n = w.getnframes()
            raw = w.readframes(n)
            if n <= 0 or len(raw) != n * fmt[0] * fmt[1]:
                raise ValueError(f'{p.name}: 空音频或PCM数据截断')
        counts.append(n)
        chunks.append(raw)
        inputs.append(dict(file=p.name, sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    rows = boundaries(counts, fmt[2], fps)
    out.mkdir(parents=True, exist_ok=False)
    raw = b''.join(chunks)
    master = out / 'master.wav'
    with wave.open(str(master), 'wb') as w:
        w.setnchannels(fmt[0]); w.setsampwidth(fmt[1]); w.setframerate(fmt[2])
        w.writeframes(raw)
    with wave.open(str(master), 'rb') as w:
        if w.getnframes() != sum(counts) or w.readframes(w.getnframes()) != raw:
            raise RuntimeError('母带回读失败')
    result = dict(sample_rate=fmt[2], channels=fmt[0], sample_width_bytes=fmt[1],
                  fps=str(fps), total_samples=sum(counts),
                  audio_seconds_exact=str(Fraction(sum(counts), fmt[2])),
                  total_video_frames=rows[-1]['end_frame'],
                  master_sha256=hashlib.sha256(master.read_bytes()).hexdigest(),
                  pcm_sha256=hashlib.sha256(raw).hexdigest(),
                  inputs=inputs, sections=rows,
                  subjective_listening='NOT_PERFORMED', content_validation='NOT_PERFORMED')
    (out / 'sample-clock.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return result


def self_test():
    for rate, fps in [(24000, Fraction(30)), (48000, Fraction(30000, 1001))]:
        rows = boundaries([rate+1]*20, rate, fps)
        assert rows[-1]['end_frame'] == ceil_fraction(Fraction(20*(rate+1), rate)*fps)
        assert sum(r['video_frames'] for r in rows) == rows[-1]['end_frame']
        for r in rows:
            delta = Fraction(r['end_frame']) - Fraction(r['end_sample'], rate)*fps
            assert 0 <= delta < 1
    assert sum(r['video_frames'] == 0 for r in boundaries([1]*20, 48000, Fraction(30))) == 19
    with tempfile.TemporaryDirectory() as d:
        root = Path(d); audio = root/'audio'; audio.mkdir()
        for i in range(1, 21):
            with wave.open(str(audio/f'S{i:02}.wav'), 'wb') as w:
                w.setparams((2, 2, 24000, 0, 'NONE', 'not compressed'))
                w.writeframes(bytes([i, 0, i, 0])*(100+i))
        r = build(audio, root/'out', Fraction(30))
        assert r['total_samples'] == 2210 and r['channels'] == 2
        try:
            build(audio, root/'out', Fraction(30))
        except FileExistsError:
            pass
        else:
            raise AssertionError('必须拒绝覆盖')
        with wave.open(str(audio/'S20.wav'), 'wb') as w:
            w.setparams((1, 2, 24000, 0, 'NONE', 'not compressed'))
            w.writeframes(b'\0\0'*120)
        try:
            build(audio, root/'bad', Fraction(30))
        except ValueError:
            assert not (root/'bad').exists()
        else:
            raise AssertionError('必须拒绝格式不一致')
    print('PASS: 精确帧边界、零帧段、立体声PCM拼接/回读、拒绝覆盖、拒绝格式不一致')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audio', type=Path)
    p.add_argument('--out', type=Path)
    p.add_argument('--fps', default='30')
    p.add_argument('--self-test', action='store_true')
    a = p.parse_args()
    if a.self_test:
        self_test()
    elif a.audio is None or a.out is None:
        p.error('需要 --audio 与 --out，或 --self-test')
    else:
        result = build(a.audio, a.out, Fraction(a.fps))
        print(json.dumps({k: result[k] for k in ('total_samples', 'total_video_frames', 'audio_seconds_exact')}, ensure_ascii=False))
