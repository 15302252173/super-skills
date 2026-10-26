"""Synthetic CFR timeline mathematics; no media, network, or user inputs."""
from fractions import Fraction
from itertools import accumulate
from math import ceil
from random import Random


def allocate(samples, rate, fps):
    if not samples or any(type(n) is not int or n <= 0 for n in samples):
        raise ValueError('positive integer sample-frame counts required')
    if type(rate) is not int or rate <= 0 or fps <= 0:
        raise ValueError('positive rate and fps required')
    boundaries = [0] + [ceil(Fraction(n, rate) * fps)
                        for n in accumulate(samples)]
    counts = [b - a for a, b in zip(boundaries, boundaries[1:])]
    naive = sum(ceil(Fraction(n, rate) * fps) for n in samples)
    total = ceil(Fraction(sum(samples), rate) * fps)
    assert sum(counts) == total
    assert all(n >= 0 for n in counts)
    assert 0 <= naive - total <= len(samples) - 1
    for sample_boundary, frame_boundary in zip(accumulate(samples), boundaries[1:]):
        error = Fraction(frame_boundary, 1) / fps - Fraction(sample_boundary, rate)
        assert 0 <= error < 1 / fps
    return naive, total, counts


def main():
    cases = [
        ('fractional_30', [48001] * 60, 48000, Fraction(30)),
        ('aligned_25', [48000] * 60, 48000, Fraction(25)),
        ('ntsc', [48000] * 60, 48000, Fraction(30000, 1001)),
        ('tiny_segments', [1] * 100, 48000, Fraction(30)),
        ('mixed_44100', [44099, 44100, 44101], 44100, Fraction(24)),
    ]
    for name, samples, rate, fps in cases:
        naive, total, counts = allocate(samples, rate, fps)
        print(f'{name}: naive={naive}, global={total}, excess={naive-total}, '
              f'zero_frame_segments={counts.count(0)}')
    rng = Random(20261027)
    for _ in range(1000):
        allocate([rng.randint(1, 300000) for _ in range(rng.randint(1, 80))],
                 rng.choice([44100, 48000]), rng.choice([Fraction(24), Fraction(25),
                 Fraction(30), Fraction(30000, 1001)]))
    for bad in [[], [0], [-1], [1.5]]:
        try:
            allocate(bad, 48000, Fraction(30))
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input accepted')
    # Half-open sample intervals reconstruct the source exactly once.
    source = list(range(20))
    assert source[:7] + source[7:13] + source[13:20] == source
    assert source[:7] + source[6:13] + source[13:20] != source
    assert Fraction(30000, 1001) != Fraction('29.97')
    print('PASS: 5 fixed + 1000 seeded cases; 4 invalid inputs; interval checks')


if __name__ == '__main__':
    main()
