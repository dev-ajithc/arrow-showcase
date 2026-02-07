"""
Scheduling and task automation utilities.

Helper functions for scheduling tasks and creating reminders.
"""

from typing import Callable, Dict, List, Optional

import arrow


def schedule_daily(
    hour: int,
    minute: int,
    task: Callable,
    timezone: str = 'UTC'
) -> Dict[str, str]:
    """
    Schedule task to run daily at specific time.

    Args:
        hour: Hour (0-23)
        minute: Minute (0-59)
        task: Function to execute
        timezone: Timezone for scheduling

    Returns:
        Dictionary with schedule information

    Example:
        >>> def my_task():
        ...     print("Task executed")
        >>> info = schedule_daily(2, 0, my_task)
        >>> 'next_run' in info
        True
    """
    now = arrow.now(timezone)
    next_run = now.replace(hour=hour, minute=minute, second=0)

    if next_run <= now:
        next_run = next_run.shift(days=1)

    return {
        'task': task.__name__,
        'schedule': f"Daily at {hour:02d}:{minute:02d}",
        'timezone': timezone,
        'next_run': next_run.isoformat(),
    }


class Reminder:
    """
    Simple reminder/notification system.

    Example:
        >>> reminder = Reminder()
        >>> future = arrow.utcnow().shift(hours=2)
        >>> reminder.add("Meeting", future)
        >>> len(reminder.list_active())
        1
    """

    def __init__(self) -> None:
        """Initialize reminder system."""
        self.reminders: List[Dict] = []

    def add(
        self,
        title: str,
        remind_at: arrow.Arrow,
        recurring: bool = False,
        interval: Optional[str] = None
    ) -> None:
        """
        Add a new reminder.

        Args:
            title: Reminder title
            remind_at: When to trigger reminder
            recurring: Whether reminder repeats
            interval: Recurrence interval ('daily', 'weekly')
        """
        reminder = {
            'title': title,
            'remind_at': remind_at,
            'recurring': recurring,
            'interval': interval,
            'created_at': arrow.utcnow(),
            'active': True,
        }
        self.reminders.append(reminder)

    def list_active(self) -> List[Dict]:
        """
        List all active reminders.

        Returns:
            List of active reminder dictionaries
        """
        return [r for r in self.reminders if r['active']]

    def check_due(self) -> List[Dict]:
        """
        Check for due reminders.

        Returns:
            List of reminders that are due
        """
        now = arrow.utcnow()
        due = []

        for reminder in self.reminders:
            if reminder['active'] and reminder['remind_at'] <= now:
                due.append(reminder)

                if not reminder['recurring']:
                    reminder['active'] = False
                else:
                    if reminder['interval'] == 'daily':
                        reminder['remind_at'] = (
                            reminder['remind_at'].shift(days=1)
                        )
                    elif reminder['interval'] == 'weekly':
                        reminder['remind_at'] = (
                            reminder['remind_at'].shift(weeks=1)
                        )

        return due

    def cancel(self, title: str) -> bool:
        """
        Cancel a reminder by title.

        Args:
            title: Reminder title

        Returns:
            True if cancelled, False if not found
        """
        for reminder in self.reminders:
            if reminder['title'] == title and reminder['active']:
                reminder['active'] = False
                return True
        return False


class TaskScheduler:
    """
    Advanced task scheduling system.

    Example:
        >>> scheduler = TaskScheduler()
        >>> def backup():
        ...     print("Backup running")
        >>> scheduler.add_daily_task("backup", 2, 0, backup)
        >>> len(scheduler.list_tasks())
        1
    """

    def __init__(self) -> None:
        """Initialize task scheduler."""
        self.tasks: List[Dict] = []

    def add_daily_task(
        self,
        name: str,
        hour: int,
        minute: int,
        task: Callable,
        timezone: str = 'UTC'
    ) -> None:
        """
        Add daily scheduled task.

        Args:
            name: Task name
            hour: Hour (0-23)
            minute: Minute (0-59)
            task: Function to execute
            timezone: Timezone for scheduling
        """
        now = arrow.now(timezone)
        next_run = now.replace(hour=hour, minute=minute, second=0)

        if next_run <= now:
            next_run = next_run.shift(days=1)

        task_info = {
            'name': name,
            'type': 'daily',
            'hour': hour,
            'minute': minute,
            'task': task,
            'timezone': timezone,
            'next_run': next_run,
            'active': True,
        }
        self.tasks.append(task_info)

    def add_weekly_task(
        self,
        name: str,
        day: int,
        hour: int,
        minute: int,
        task: Callable,
        timezone: str = 'UTC'
    ) -> None:
        """
        Add weekly scheduled task.

        Args:
            name: Task name
            day: Day of week (0=Monday, 6=Sunday)
            hour: Hour (0-23)
            minute: Minute (0-59)
            task: Function to execute
            timezone: Timezone for scheduling
        """
        now = arrow.now(timezone)
        next_run = now.replace(hour=hour, minute=minute, second=0)

        days_ahead = day - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7

        next_run = next_run.shift(days=days_ahead)

        task_info = {
            'name': name,
            'type': 'weekly',
            'day': day,
            'hour': hour,
            'minute': minute,
            'task': task,
            'timezone': timezone,
            'next_run': next_run,
            'active': True,
        }
        self.tasks.append(task_info)

    def list_tasks(self) -> List[Dict]:
        """
        List all active tasks.

        Returns:
            List of active task dictionaries
        """
        return [t for t in self.tasks if t['active']]

    def get_next_task(self) -> Optional[Dict]:
        """
        Get next task to run.

        Returns:
            Next task dictionary or None
        """
        active_tasks = self.list_tasks()
        if not active_tasks:
            return None

        return min(active_tasks, key=lambda t: t['next_run'])
