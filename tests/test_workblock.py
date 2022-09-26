import unittest
from bautomate.workblock import WorkBlock


class TestWorkBlock(unittest.TestCase):

    def test_project_name_strip(self):
        wb = WorkBlock()
        wb.project_name = '  foo bar    '
        self.assertEqual(wb.project_name, 'foo bar')

    def test_project_name_newline(self):
        wb = WorkBlock()
        wb.project_name = 'foo\nbar'
        self.assertEqual(wb.project_name, 'foobar')

    def test_project_name_type(self):
        wb = WorkBlock()
        wb.project_name = 1337
        self.assertIsInstance(wb.project_name, str)

    def test_activity_strip(self):
        wb = WorkBlock()
        wb.activity = '  foo bar    '
        self.assertEqual(wb.activity, 'foo bar')

    def test_activity_newline(self):
        wb = WorkBlock()
        wb.activity = 'foo\nbar'
        self.assertEqual(wb.activity, 'foobar')

    def test_activity_type(self):
        wb = WorkBlock()
        wb.activity = 1337
        self.assertIsInstance(wb.activity, str)

    def test_duration_type(self):
        wb = WorkBlock()
        wb.duration = '30'
        self.assertIsInstance(wb.duration, int)

    def test_duration_negative(self):
        wb = WorkBlock()
        with self.assertRaises(ValueError):
            wb.duration = -1

    def test_duration_zero(self):
        wb = WorkBlock()
        with self.assertRaises(ValueError):
            wb.duration = 0

    def test_duration_conversion(self):
        wb = WorkBlock()
        wb.duration = '8:30'
        self.assertEqual(wb.duration, 510)

        wb.duration = '4.00'
        self.assertEqual(wb.duration, 240)

    def test_duration_calculation(self):
        wb = WorkBlock()
        wb.duration = 4.25
        self.assertEqual(wb.duration, 255)

    def test_duration_too_long(self):
        wb = WorkBlock()
        with self.assertRaises(ValueError):
            wb.duration = 10.25

    def test_kwargs(self):
        kw = {
            "project_name": "foobar",
            "activity": "work",
            "duration": "8:00"
        }
        wb = WorkBlock(**kw)
        self.assertEqual(wb.project_name, "foobar")
        self.assertEqual(wb.activity, "work")
        self.assertEqual(wb.duration, 480)


if __name__ == "__main__":
    unittest.main()