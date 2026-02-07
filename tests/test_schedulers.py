"""
Tests for scheduler functions.
"""

import pytest
from freezegun import freeze_time

import arrow
from utils.schedulers import Reminder, TaskScheduler, schedule_daily


class TestScheduleDaily:
    @freeze_time("2024-02-07 12:00:00")
    def test_schedule_in_future_same_day(self):
        def task():
            pass

        result = schedule_daily(14, 30, task, 'UTC')

        assert result['task'] == 'task'
        assert '14:30' in result['schedule']
        assert result['timezone'] == 'UTC'
        assert 'next_run' in result

    @freeze_time("2024-02-07 16:00:00")
    def test_schedule_next_day(self):
        def task():
            pass

        result = schedule_daily(14, 30, task, 'UTC')

        next_run = arrow.get(result['next_run'])
        assert next_run.day == 8


class TestReminder:
    def test_initialization(self):
        reminder = Reminder()

        assert len(reminder.reminders) == 0

    def test_add_reminder(self):
        reminder = Reminder()
        future = arrow.utcnow().shift(hours=2)

        reminder.add("Meeting", future)

        assert len(reminder.reminders) == 1
        assert reminder.reminders[0]['title'] == "Meeting"

    def test_list_active(self):
        reminder = Reminder()
        future = arrow.utcnow().shift(hours=2)

        reminder.add("Meeting", future)

        active = reminder.list_active()
        assert len(active) == 1

    @freeze_time("2024-02-07 12:00:00")
    def test_check_due_no_reminders(self):
        reminder = Reminder()

        due = reminder.check_due()

        assert len(due) == 0

    @freeze_time("2024-02-07 12:00:00")
    def test_check_due_with_due_reminder(self):
        reminder = Reminder()
        past = arrow.get('2024-02-07 11:00:00')

        reminder.add("Past Meeting", past)

        due = reminder.check_due()

        assert len(due) == 1
        assert due[0]['title'] == "Past Meeting"

    @freeze_time("2024-02-07 12:00:00")
    def test_check_due_non_recurring_deactivates(self):
        reminder = Reminder()
        past = arrow.get('2024-02-07 11:00:00')

        reminder.add("Meeting", past, recurring=False)
        reminder.check_due()

        active = reminder.list_active()
        assert len(active) == 0

    @freeze_time("2024-02-07 12:00:00")
    def test_check_due_recurring_updates(self):
        reminder = Reminder()
        past = arrow.get('2024-02-07 11:00:00')

        reminder.add("Daily Task", past, recurring=True, interval='daily')
        reminder.check_due()

        assert reminder.reminders[0]['active'] is True
        assert reminder.reminders[0]['remind_at'].day == 8

    def test_cancel_reminder(self):
        reminder = Reminder()
        future = arrow.utcnow().shift(hours=2)

        reminder.add("Meeting", future)
        result = reminder.cancel("Meeting")

        assert result is True
        assert len(reminder.list_active()) == 0

    def test_cancel_nonexistent_reminder(self):
        reminder = Reminder()

        result = reminder.cancel("Nonexistent")

        assert result is False


class TestTaskScheduler:
    def test_initialization(self):
        scheduler = TaskScheduler()

        assert len(scheduler.tasks) == 0

    @freeze_time("2024-02-07 12:00:00")
    def test_add_daily_task(self):
        scheduler = TaskScheduler()

        def task():
            pass

        scheduler.add_daily_task("backup", 2, 0, task)

        assert len(scheduler.tasks) == 1
        assert scheduler.tasks[0]['name'] == "backup"
        assert scheduler.tasks[0]['type'] == 'daily'

    @freeze_time("2024-02-07 12:00:00")
    def test_add_weekly_task(self):
        scheduler = TaskScheduler()

        def task():
            pass

        scheduler.add_weekly_task("report", 0, 9, 0, task)

        assert len(scheduler.tasks) == 1
        assert scheduler.tasks[0]['type'] == 'weekly'

    def test_list_tasks(self):
        scheduler = TaskScheduler()

        def task():
            pass

        scheduler.add_daily_task("task1", 2, 0, task)
        scheduler.add_daily_task("task2", 3, 0, task)

        tasks = scheduler.list_tasks()

        assert len(tasks) == 2

    @freeze_time("2024-02-07 12:00:00")
    def test_get_next_task(self):
        scheduler = TaskScheduler()

        def task():
            pass

        scheduler.add_daily_task("task1", 14, 0, task)
        scheduler.add_daily_task("task2", 16, 0, task)

        next_task = scheduler.get_next_task()

        assert next_task['name'] == "task1"

    def test_get_next_task_empty(self):
        scheduler = TaskScheduler()

        next_task = scheduler.get_next_task()

        assert next_task is None
