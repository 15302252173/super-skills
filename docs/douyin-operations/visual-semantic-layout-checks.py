"""Synthetic layout/semantic regression checks. No media, network or dependencies."""
import unittest

def overlaps(a, b):
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])

def inside(box, region):
    return region[0] <= box[0] <= box[2] <= region[2] and region[1] <= box[1] <= box[3] <= region[3]

def visible(frame, start, end):
    return start <= frame < end

def semantic_errors(footage, labels, claims):
    errors = []
    if footage and "not-to-scale diagram" in labels:
        errors.append("diagram label on footage")
    if footage and "curvature evidence" in claims:
        errors.append("unrelated footage used as evidence")
    return errors

class LayoutTests(unittest.TestCase):
    def test_eraser(self):
        card = (30, 880, 690, 938)
        self.assertTrue(overlaps((0, 230, 720, 910), card))
        self.assertFalse(overlaps((0, 230, 720, 870), card))

    def test_unit_label(self):
        card = (30, 880, 690, 938)
        self.assertTrue(overlaps((250, 864, 470, 884), card))
        self.assertFalse(overlaps((250, 260, 470, 280), card))

    def test_subtitle_bounds(self):
        safe = (30, 1080, 690, 1240)
        self.assertTrue(inside((60, 1102, 660, 1181), safe))
        self.assertFalse(inside((60, 1102, 700, 1181), safe))

    def test_frame_boundary(self):
        start, end = 240, 330
        self.assertFalse(visible(start - 1, start, end))
        self.assertTrue(visible(start, start, end))
        self.assertTrue(visible(end - 1, start, end))
        self.assertFalse(visible(end, start, end))

    def test_semantic_switch(self):
        for frame in range(239, 332):
            footage = visible(frame, 240, 330)
            labels = {"montage, not continuous"} if footage else {"not-to-scale diagram"}
            claims = set() if footage else {"curvature evidence"}
            self.assertEqual(semantic_errors(footage, labels, claims), [])
        self.assertEqual(len(semantic_errors(True, {"not-to-scale diagram"}, {"curvature evidence"})), 2)

    def test_target_constraint(self):
        # Normalized distance from observer; rod at one third of sight line.
        self.assertLess(0.25, 1 / 3)  # a bad animation endpoint
        for i in range(101):
            z = 0.45 + 0.45 * i / 100
            self.assertGreater(z, 1 / 3)
            self.assertLessEqual(z, 0.9)

if __name__ == "__main__":
    unittest.main(verbosity=2)
