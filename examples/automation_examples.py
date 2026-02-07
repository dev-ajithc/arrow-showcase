"""
Real-world automation examples using Arrow.

Demonstrates practical use cases like file naming, backups, reminders.
"""

import os
import shutil
import time
from pathlib import Path

import arrow


def demo_timestamped_filenames() -> None:
    """Generate files with timestamp names."""
    print("\n=== Timestamped Filenames Demo ===")

    print("Creating timestamped files:")

    formats = [
        ('YYYYMMDD_HHmmss', 'backup'),
        ('YYYY-MM-DD_HH-mm-ss', 'log'),
        ('YYYYMMDD', 'report'),
        ('YYYY_MM_DD_HHmmss', 'export'),
    ]

    for fmt, prefix in formats:
        timestamp = arrow.utcnow().format(fmt)
        filename = f"{prefix}_{timestamp}.txt"
        print(f"  {filename}")


def demo_scheduled_backups() -> None:
    """Schedule and execute timed backups."""
    print("\n=== Scheduled Backups Demo ===")

    backup_time = arrow.utcnow().replace(hour=2, minute=0, second=0)
    print(f"Backup scheduled for: {backup_time.format('HH:mm:ss')} UTC")

    if backup_time < arrow.utcnow():
        backup_time = backup_time.shift(days=1)

    time_until = backup_time - arrow.utcnow()
    hours = time_until.total_seconds() / 3600

    print(f"Next backup in: {hours:.2f} hours")
    print(f"Next backup at: {backup_time.format('YYYY-MM-DD HH:mm:ss')}")

    filename = f"backup_{arrow.utcnow().format('YYYYMMDD_HHmmss')}.tar.gz"
    print(f"Backup filename: {filename}")


def demo_reminder_system() -> None:
    """Build a simple reminder/notification system."""
    print("\n=== Reminder System Demo ===")

    reminders = [
        {
            'title': 'Team Meeting',
            'time': arrow.utcnow().shift(hours=2),
        },
        {
            'title': 'Code Review',
            'time': arrow.utcnow().shift(hours=5),
        },
        {
            'title': 'Project Deadline',
            'time': arrow.utcnow().shift(days=3),
        },
    ]

    print("Active reminders:")
    for reminder in reminders:
        time_str = reminder['time'].humanize()
        formatted = reminder['time'].format('YYYY-MM-DD HH:mm')
        print(f"  '{reminder['title']}' - {time_str} ({formatted})")


def demo_log_rotation() -> None:
    """Rotate log files based on date."""
    print("\n=== Log Rotation Demo ===")

    log_dir = Path("logs")
    retention_days = 7

    print(f"Log rotation configuration:")
    print(f"  Directory: {log_dir}")
    print(f"  Retention: {retention_days} days")

    cutoff_date = arrow.utcnow().shift(days=-retention_days)
    print(f"  Cutoff date: {cutoff_date.format('YYYY-MM-DD')}")

    sample_logs = [
        arrow.utcnow().shift(days=-1),
        arrow.utcnow().shift(days=-5),
        arrow.utcnow().shift(days=-10),
        arrow.utcnow().shift(days=-15),
    ]

    print("\nLog files (simulated):")
    for log_date in sample_logs:
        filename = f"app_{log_date.format('YYYYMMDD')}.log"
        status = "KEEP" if log_date > cutoff_date else "DELETE"
        print(f"  {filename} - {status}")


def demo_deadline_tracker() -> None:
    """Track and alert on upcoming deadlines."""
    print("\n=== Deadline Tracker Demo ===")

    deadlines = [
        {
            'task': 'Submit tax returns',
            'deadline': arrow.get('2024-04-15'),
        },
        {
            'task': 'Project presentation',
            'deadline': arrow.utcnow().shift(days=5),
        },
        {
            'task': 'Quarterly report',
            'deadline': arrow.utcnow().shift(days=15),
        },
    ]

    now = arrow.utcnow()

    print("Deadline tracking:")
    for item in deadlines:
        deadline = item['deadline']
        days_left = (deadline - now).days

        status = "URGENT" if days_left <= 7 else "OK"
        formatted = deadline.format('YYYY-MM-DD')

        print(f"  {item['task']}")
        print(f"    Due: {formatted} ({days_left} days left) - {status}")


def demo_periodic_tasks() -> None:
    """Execute tasks at specific intervals."""
    print("\n=== Periodic Tasks Demo ===")

    tasks = [
        {'name': 'Database backup', 'interval': 'daily', 'time': '02:00'},
        {'name': 'Report generation', 'interval': 'weekly', 'day': 'Monday'},
        {'name': 'Cache cleanup', 'interval': 'hourly'},
        {'name': 'Health check', 'interval': 'every 5 minutes'},
    ]

    print("Scheduled tasks:")
    for task in tasks:
        if task['interval'] == 'daily':
            print(f"  {task['name']}: Every day at {task['time']}")
        elif task['interval'] == 'weekly':
            print(f"  {task['name']}: Every {task['day']}")
        else:
            print(f"  {task['name']}: {task['interval']}")


def demo_file_organization() -> None:
    """Organize files by date."""
    print("\n=== File Organization Demo ===")

    files = [
        arrow.get('2024-01-15'),
        arrow.get('2024-02-01'),
        arrow.get('2024-02-15'),
        arrow.get('2024-03-01'),
    ]

    print("Organizing files by year/month:")
    for file_date in files:
        path = f"{file_date.year}/{file_date.month:02d}"
        filename = f"file_{file_date.format('YYYYMMDD')}.txt"
        full_path = f"{path}/{filename}"
        print(f"  {full_path}")


def main() -> None:
    """Run all automation examples."""
    print("=" * 60)
    print("Arrow Automation Examples")
    print("=" * 60)

    demo_timestamped_filenames()
    time.sleep(0.5)

    demo_scheduled_backups()
    time.sleep(0.5)

    demo_reminder_system()
    time.sleep(0.5)

    demo_log_rotation()
    time.sleep(0.5)

    demo_deadline_tracker()
    time.sleep(0.5)

    demo_periodic_tasks()
    time.sleep(0.5)

    demo_file_organization()

    print("\n" + "=" * 60)
    print("All automation examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
