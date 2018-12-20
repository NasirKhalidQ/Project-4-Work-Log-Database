import os
import datetime


from peewee import *
from collections import OrderedDict


db = SqliteDatabase('worklog.db')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


class Entry(Model):
    employee_name = TextField()
    task_title = TextField()
    time_spent = IntegerField()
    notes = TextField()
    task_date = DateTimeField()

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    """Add an entry."""
    input_name = input('Enter the name of the employee: ')
    input_title = input('Enter the title of your task: ')

    while True:
        try:
            input_time_spent = input('Enter the time spent on the task in '
                                     'minutes: ')
            break
        except ValueError:
            print('Please enter a valid integer')

    input_notes = input('Enter notes(these are optional): ')

    while True:
            input_date = input('Enter the date of the task. Please use the '
                               'MM/DD/YYYY format: ')
            try:
                datetime.datetime.strptime(input_date, '%m/%d/%Y')
                break
            except ValueError:
                print('You have entered an invalid date. Please try again.')

    Entry.create(
      employee_name=input_name,
      task_title=input_title,
      time_spent=input_time_spent,
      notes=input_notes,
      task_date=input_date)

    print("Saved successfully!")


def view_entries(entries):
    """View previous entries."""
    for entry in entries:
        clear()
        print('='*50)
        print('Employee name:', entry.employee_name)
        print('Task Title:', entry.task_title)
        print('Time Spent:', entry.time_spent)
        print('Notes:', entry.notes)
        print('Task date:', datetime.datetime.strftime(entry.task_date,
              '%m/%d/%Y'))
        print('='*50)
        print('n) next entry')
        print('q) return to main menu')

        next_action = input('Action: [Nq] ').lower().strip()
        if next_action == 'q':
            break


def find_by_employee():
    """Search entries by employee name"""
    employee_name = input('Enter the name of the employee for searching: ')

    entries = Entry.select()
    entries = entries.where(Entry.employee_name.contains(employee_name))
    view_entries(entries)

    if entries.exists():
        input('Search results displayed. Press enter to return to '
              'the menu')
    else:
        input('Entry does not exist. Press enter to return to menu')


def find_by_date():
    """Search entries by date of task"""
    while True:
        date = input('Enter the date of the task for searching. Please use '
                     'the MM/DD/YYYY format: ')
        try:
            datetime.datetime.strptime(date, '%m/%d/%Y')
            break
        except ValueError:
            print('You have entered an invalid date. Please try again.')

    entries = Entry.select().where(
              Entry.task_date == datetime.datetime.strptime(date, '%m/%d/%Y'))
    view_entries(entries)

    if entries.exists():
        input('Search results displayed. Press enter to return to '
              'the menu')
    else:
        input('Entry does not exist. Press enter to return to menu')


def find_by_time_spent():
    """Search entries by total time spent on the task"""
    while True:
                try:
                    spent_time = int(input('Enter the time spent on the '
                                           'task for searching: '))
                    break
                except ValueError:
                    print('Please enter a valid integer')

    entries = Entry.select()
    entries = Entry.select().where(Entry.time_spent == spent_time)
    view_entries(entries)

    if entries.exists():
        input('Search results displayed. Press enter to return to '
              'the menu')
    else:
        input('Entry does not exist. Press enter to return to menu')


def find_by_term():
    """Search entries by task name or notes(which are optional)"""
    term = input('Enter the name of the task or notes for searching: ')

    entries = Entry.select()
    entries = entries.where(Entry.task_title.contains(term) | (
        Entry.notes.contains(term)))
    view_entries(entries)

    if entries.exists():
        input('Search results displayed. Press enter to return to '
              'the menu')
    else:
        input('Entry does not exist. Press enter to return to menu')


menu = OrderedDict([
    ('a', add_entry),
    ('e', find_by_employee),
    ('d', find_by_date),
    ('s', find_by_time_spent),
    ('t', find_by_term)
])

if __name__ == '__main__':
    initialize()
    menu_loop()
