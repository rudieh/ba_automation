import unittest

from bautomate.workday import WorkDay


class TestWorkDay(unittest.TestCase):
    def test_date_day_type(self):
        wd = WorkDay()
        with self.assertRaises(TypeError):
            wd.date_day = 20220801

    def test_date_day_reverse(self):
        wd = WorkDay()
        wd.date_day = "01.08.2022"
        self.assertEqual(wd.date_day, "2022.08.01")

    def test_date_day_slash(self):
        wd = WorkDay()
        wd.date_day = "01/08/2022"
        self.assertEqual(wd.date_day, "2022.08.01")

    def test_date_day_hyphen(self):
        wd = WorkDay()
        wd.date_day = "01-08-2022"
        self.assertEqual(wd.date_day, "2022.08.01")

    def test_start_time_type(self):
        wd = WorkDay()
        with self.assertRaises(TypeError):
            wd.start_time = 8.0

    def test_start_time_default(self):
        wd = WorkDay()
        self.assertEqual(wd.start_time, "08:00")

    def test_start_time_dot(self):
        wd = WorkDay()
        wd.start_time = "13.30"
        self.assertEqual(wd.start_time, "13:30")

    def test_start_time_colon(self):
        wd = WorkDay()
        wd.start_time = "14:30"
        self.assertEqual(wd.start_time, "14:30")

    def test_end_time_type(self):
        wd = WorkDay()
        with self.assertRaises(TypeError):
            wd.end_time = 8.0

    def test_end_time_default(self):
        wd = WorkDay()
        self.assertEqual(wd.end_time, "16:30")

    def test_end_time_dot(self):
        wd = WorkDay()
        wd.end_time = "13.30"
        self.assertEqual(wd.end_time, "13:30")

    def test_end_time_colon(self):
        wd = WorkDay()
        wd.end_time = "14:30"
        self.assertEqual(wd.end_time, "14:30")

    def test_break_duration_type(self):
        wd = WorkDay()
        with self.assertRaises(TypeError):
            wd.break_duration = 8.0

    def test_break_duration_default(self):
        wd = WorkDay()
        self.assertEqual(wd.break_duration, "00:30")

    def test_break_duration_dot(self):
        wd = WorkDay()
        wd.break_duration = "13.30"
        self.assertEqual(wd.break_duration, "13:30")

    def test_break_duration_colon(self):
        wd = WorkDay()
        wd.break_duration = "14:30"
        self.assertEqual(wd.break_duration, "14:30")

    def test_mode_lower(self):
        wd = WorkDay()
        wd.mode = "Normal"
        self.assertEqual(wd.mode, "normal")

    def test_mode_short(self):
        wd = WorkDay()
        wd.mode = "norm"
        self.assertEqual(wd.mode, "normal")

    def test_mode_type(self):
        wd = WorkDay()
        with self.assertRaises(TypeError):
            wd.mode = 3

    def test_mode_valid(self):
        wd = WorkDay()
        with self.assertRaises(ValueError):
            wd.mode = "foobar"

    def test_blocks_type(self):
        wd = WorkDay()
        with self.assertRaises(TypeError):
            wd.blocks = "foobar"

    def test_blocks_create_element(self):
        wd = WorkDay()
        wd.blocks = [
            {
                "project_name": "foobar",
                "activity": "work",
                "duration": "08:00",
            },
            {
                "project_name": "barfoo",
                "activity": "not work",
                "duration": "09:30",
            },
        ]
        self.assertEqual(wd.blocks[0].project_name, "foobar")
        self.assertEqual(wd.blocks[0].activity, "work")
        self.assertEqual(wd.blocks[0].duration, 480)

    def test_kwargs(self):
        kw = {"date_day": "1.8.2022", "end_time": "17.00", "mode": "normal"}
        wd = WorkDay(**kw)
        self.assertEqual(wd.date_day, "2022.08.01")
        self.assertEqual(wd.start_time, "08:00")
        self.assertEqual(wd.end_time, "17:00")
        self.assertEqual(wd.break_duration, "00:30")
        self.assertEqual(wd.mode, "normal")


if __name__ == "__main__":
    unittest.main()
