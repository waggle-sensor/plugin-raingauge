import parse
import unittest


class TestParse(unittest.TestCase):
    def test_valid(self):
        r = parse.parse_values(
            "Acc  1.23 mm, EventAcc  4.56 mm, TotalAcc  7.89 mm, RInt  2.48 mmph\n"
        )
        self.assertDictEqual(
            r, {"Acc": 1.23, "EventAcc": 4.56, "TotalAcc": 7.89, "RInt": 2.48}
        )

    def test_partial(self):
        r = parse.parse_values(
            "cc  1.23 mm, EventAcc  4.56 mm, TotalAcc  7.89 mm, RInt  2.48 mmph\n"
        )
        self.assertDictEqual(r, {"EventAcc": 4.56, "TotalAcc": 7.89, "RInt": 2.48})

    def test_glitch(self):
        r = parse.parse_values(
            "AcQ  1.23 mm, EventAcc  4.x6 mm, TotalAcc  7.89 mm, RInt2.48 mmph\n"
        )
        self.assertDictEqual(r, {"TotalAcc": 7.89})

    def test_num_fields(self):
        r = parse.parse_values("7.89 mm, RInt 2.48 mmph\n")
        self.assertDictEqual(r, {"RInt": 2.48})

    def test_skip_inches(self):
        r = parse.parse_values("Acc  1.23 in\n")
        self.assertDictEqual(r, {})
        r = parse.parse_values("RInt 2.03 iph\n")
        self.assertDictEqual(r, {})
        r = parse.parse_values(
            "Acc  1.23 mm, EventAcc  4.56 in, TotalAcc  7.89 mm, RInt  2.48 iph\n"
        )
        self.assertDictEqual(r, {"Acc": 1.23, "TotalAcc": 7.89})


if __name__ == "__main__":
    unittest.main()
