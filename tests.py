from unittest.mock import patch

import unittest
import coverage
import work


from work import Entry


class WorkTests(unittest.TestCase):
    def setUp(self):
        """Here we create a sample data to test in our mock function"""
        self.entry = work
        self.employee_name = 'JK Rowling'
        self.task_title = 'Writing Books'
        self.time_spent = 25
        self.task_date = '7/20/1990'
        self.notes = 'Harry Potter'

    def test_employee(self):
        """Checks if employee name is added correctly to the database"""
        assert Entry.employee_name == self.employee_name

    def test_task_title(self):
        """Checks if task title is added correctly to the database"""
        assert Entry.task_title == self.task_title

    def test_time_spent(self):
        """Checks if time spent is added correctly to the database"""
        assert Entry.time_spent == self.time_spent

    def test_task_date(self):
        """Checks if task date is added correctly to the database"""
        assert Entry.task_date == self.task_date

    def test_notes(self):
        """Checks if notes are added correctly to the database"""
        assert Entry.notes == self.notes

    def test_employee_search(self):
        """Checks if entry can be searched by employee name"""
        with patch('builtins.input', side_effect=[self.employee_name, '\n',
                   '']) as mock:
            self.entry.find_by_employee()

    def test_date_search(self):
        """Checks if entry can be searched by date"""
        with patch('builtins.input', side_effect=['20/07/1995',
                   self.task_date,  '\n', '']) as mock:
            self.entry.find_by_date()

    def test_time_spent_search(self):
        """Checks if entry can be searched by time spent on task"""
        with patch('builtins.input', side_effect=[self.time_spent, '\n',
                   '']) as mock:
            self.entry.find_by_time_spent()

    def test_term_search(self):
        """Checks if entry can be searched by notes or task title"""
        with patch('builtins.input', side_effect=[self.notes, '\n', '']) as  \
                mock:
            self.entry.find_by_term()


if __name__ == '__main__':
    unittest.main()
