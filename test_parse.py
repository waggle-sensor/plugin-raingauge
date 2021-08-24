import parse
import unittest

in2mm = 25.4


class TestParse(unittest.TestCase):
    def test_valid(self):
        r = parse.parse_values(
            "Acc  0.00 mm, EventAcc  0.00 mm, TotalAcc  1.23 mm, RInt  0.00 mmph\n"
        )
        self.assertDictEqual(
            r, {"Acc": 0.00, "EventAcc": 0.00, "TotalAcc": 1.23, "RInt": 0.00}
        )

    def test_partial(self):
        r = parse.parse_values(
            "cc  0.00 mm, EventAcc  0.00 mm, TotalAcc  1.23 mm, RInt  0.00 mmph\n"
        )
        self.assertDictEqual(r, {"EventAcc": 0.00, "TotalAcc": 1.23, "RInt": 0.00})

    def test_glitch(self):
        r = parse.parse_values(
            "AcQ  0.00 mm, EventAcc  0.x0 mm, TotalAcc  1.23 mm, RInt0.00 mmph\n"
        )
        self.assertDictEqual(r, {"TotalAcc": 1.23})

    def test_num_fields(self):
        r = parse.parse_values("0.00 mm, RInt 1.23 mmph\n")
        self.assertDictEqual(r, {"RInt": 1.23})

    def test_conversion(self):
        r = parse.parse_values("Acc  1.23 in\n")
        self.assertDictEqual(r, {"Acc": 1.23 * in2mm})
        r = parse.parse_values("RInt 2.03 iph\n")
        self.assertDictEqual(r, {"RInt": 2.03 * in2mm})


if __name__ == "__main__":
    unittest.main()
