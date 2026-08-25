import unittest

def normalize_score(value: float, maximum: float = 100.0) -> float:
    if maximum <= 0: raise ValueError("maximum must be positive")
    if not 0 <= value <= maximum: raise ValueError("value outside range")
    return value / maximum

class Tests(unittest.TestCase):
    def test_middle(self): self.assertAlmostEqual(normalize_score(75), .75)
    def test_invalid_maximum(self):
        with self.assertRaises(ValueError): normalize_score(1, 0)

if __name__ == "__main__": unittest.main()
