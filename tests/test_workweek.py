import unittest

from bautomate.workweek import WorkWeek


class TestWorkWeek(unittest.TestCase):
    def test_days_type(self):
        ww = WorkWeek()
        with self.assertRaises(TypeError):
            ww.days = "foobar"

    def test_days_create_element(self):
        ww = WorkWeek()
        ww.days = [
            {"date_day": "4/8/2022", "end_time": "17.00", "mode": "norm"},
            {
                "date_day": "1.8.2022",
                "start_time": "9.00",
                "end_time": "15.00",
                "mode": "normal",
            },
        ]
        self.assertEqual(ww.days[0].date_day, "2022.08.04")
        self.assertEqual(ww.days[0].start_time, "08:00")
        self.assertEqual(ww.days[0].end_time, "17:00")
        self.assertEqual(ww.days[0].break_duration, "00:30")
        self.assertEqual(ww.days[0].mode, "normal")

        self.assertEqual(ww.days[1].date_day, "2022.08.01")
        self.assertEqual(ww.days[1].start_time, "09:00")
        self.assertEqual(ww.days[1].end_time, "15:00")
        self.assertEqual(ww.days[1].break_duration, "00:30")
        self.assertEqual(ww.days[1].mode, "normal")


if __name__ == "__main__":
    unittest.main()
