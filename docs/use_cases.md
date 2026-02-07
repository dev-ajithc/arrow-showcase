# Arrow Use Cases

Practical examples of using Arrow in real-world scenarios.

## 1. Timestamped File Naming

### Problem
You need to create files with unique, sortable names based on timestamps.

### Solution

```python
import arrow

def create_timestamped_file(prefix, extension='.txt'):
    timestamp = arrow.utcnow().format('YYYYMMDD_HHmmss')
    filename = f"{prefix}_{timestamp}{extension}"
    return filename

# Usage
backup_file = create_timestamped_file('backup', '.tar.gz')
# Result: backup_20240207_143045.tar.gz

log_file = create_timestamped_file('app_log', '.log')
# Result: app_log_20240207_143045.log
```

### Benefits
- Filenames are sortable chronologically
- No filename collisions
- Easy to parse timestamps from filenames

---

## 2. Scheduled Backups

### Problem
You need to schedule regular backups at a specific time each day.

### Solution

```python
import arrow
import time

def schedule_daily_backup(hour=2, minute=0):
    """Schedule next backup at 2 AM UTC."""
    now = arrow.utcnow()
    next_backup = now.replace(hour=hour, minute=minute, second=0)

    if next_backup <= now:
        next_backup = next_backup.shift(days=1)

    return next_backup

def run_backup_scheduler():
    while True:
        next_backup = schedule_daily_backup()
        print(f"Next backup: {next_backup.format('YYYY-MM-DD HH:mm:ss')}")

        # Wait until backup time
        sleep_seconds = (next_backup - arrow.utcnow()).total_seconds()

        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

        # Run backup
        perform_backup()
```

---

## 3. Log File Rotation

### Problem
Rotate log files older than 7 days to keep disk space manageable.

### Solution

```python
import arrow
from pathlib import Path

def rotate_old_logs(log_dir, retention_days=7):
    """Archive or delete logs older than retention period."""
    cutoff_date = arrow.utcnow().shift(days=-retention_days)

    for log_file in Path(log_dir).glob('*.log'):
        # Extract date from filename (e.g., app_20240207.log)
        try:
            date_str = log_file.stem.split('_')[-1]
            file_date = arrow.get(date_str, 'YYYYMMDD')

            if file_date < cutoff_date:
                # Archive or delete
                archive_path = log_file.with_suffix('.log.gz')
                compress_and_move(log_file, archive_path)
                print(f"Archived: {log_file.name}")
        except Exception as e:
            print(f"Error processing {log_file.name}: {e}")
```

---

## 4. Deadline Tracking

### Problem
Track project deadlines and send alerts when deadlines are approaching.

### Solution

```python
import arrow

class DeadlineTracker:
    def __init__(self):
        self.deadlines = []

    def add_deadline(self, task, deadline_date):
        """Add a deadline."""
        self.deadlines.append({
            'task': task,
            'deadline': arrow.get(deadline_date),
            'created': arrow.utcnow()
        })

    def check_deadlines(self, warning_days=7):
        """Check for approaching deadlines."""
        now = arrow.utcnow()
        urgent = []

        for item in self.deadlines:
            days_left = (item['deadline'] - now).days

            if 0 <= days_left <= warning_days:
                urgent.append({
                    'task': item['task'],
                    'days_left': days_left,
                    'deadline': item['deadline'].format('YYYY-MM-DD')
                })

        return urgent

# Usage
tracker = DeadlineTracker()
tracker.add_deadline('Project Launch', '2024-03-01')
tracker.add_deadline('Tax Filing', '2024-04-15')

urgent = tracker.check_deadlines(warning_days=30)
for item in urgent:
    print(f"⚠️  {item['task']} due in {item['days_left']} days!")
```

---

## 5. API Date Handling

### Problem
Parse and format dates consistently for API communication.

### Solution

```python
import arrow
import requests

class APIClient:
    def format_for_api(self, dt):
        """Format datetime for API (ISO 8601)."""
        return dt.isoformat()

    def parse_from_api(self, date_string):
        """Parse datetime from API response."""
        return arrow.get(date_string)

    def get_events(self, start_date, end_date):
        """Fetch events between dates."""
        params = {
            'start': self.format_for_api(start_date),
            'end': self.format_for_api(end_date)
        }

        response = requests.get('/api/events', params=params)

        for event in response.json():
            event['created_at'] = self.parse_from_api(event['created_at'])
            event['updated_at'] = self.parse_from_api(event['updated_at'])

        return response.json()
```

---

## 6. Time-Based Analytics

### Problem
Generate reports for specific time periods (daily, weekly, monthly).

### Solution

```python
import arrow

def get_report_date_range(period='daily', date=None):
    """Get start and end dates for a report period."""
    if date is None:
        date = arrow.utcnow()

    if period == 'daily':
        start = date.floor('day')
        end = date.ceil('day')
    elif period == 'weekly':
        start = date.floor('week')
        end = date.ceil('week')
    elif period == 'monthly':
        start = date.floor('month')
        end = date.ceil('month')
    elif period == 'quarterly':
        quarter = (date.month - 1) // 3
        start = date.replace(month=quarter * 3 + 1, day=1).floor('day')
        end = start.shift(months=3).ceil('day')
    else:
        raise ValueError(f"Invalid period: {period}")

    return start, end

# Usage
start, end = get_report_date_range('monthly')
print(f"Monthly report: {start} to {end}")
```

---

## 7. Reminder System

### Problem
Send reminders at specific times or intervals.

### Solution

```python
import arrow

class ReminderSystem:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, title, remind_at):
        """Add a one-time reminder."""
        self.reminders.append({
            'title': title,
            'remind_at': arrow.get(remind_at),
            'recurring': False
        })

    def add_recurring_reminder(self, title, time_str, interval='daily'):
        """Add a recurring reminder."""
        now = arrow.utcnow()
        hour, minute = map(int, time_str.split(':'))

        remind_at = now.replace(hour=hour, minute=minute, second=0)
        if remind_at < now:
            remind_at = remind_at.shift(days=1)

        self.reminders.append({
            'title': title,
            'remind_at': remind_at,
            'recurring': True,
            'interval': interval
        })

    def check_reminders(self):
        """Check for due reminders."""
        now = arrow.utcnow()
        due = []

        for reminder in self.reminders:
            if reminder['remind_at'] <= now:
                due.append(reminder)

                # Update recurring reminders
                if reminder['recurring']:
                    if reminder['interval'] == 'daily':
                        reminder['remind_at'] = reminder['remind_at'].shift(days=1)
                    elif reminder['interval'] == 'weekly':
                        reminder['remind_at'] = reminder['remind_at'].shift(weeks=1)

        return due
```

---

## 8. Business Day Calculations

### Problem
Calculate business days for project planning or SLA tracking.

### Solution

```python
import arrow

def is_business_day(date):
    """Check if date is a business day (Mon-Fri)."""
    return date.weekday() < 5

def add_business_days(start_date, days):
    """Add business days to a date."""
    current = start_date
    days_added = 0

    while days_added < days:
        current = current.shift(days=1)
        if is_business_day(current):
            days_added += 1

    return current

def count_business_days(start_date, end_date):
    """Count business days between two dates."""
    count = 0
    current = start_date

    while current <= end_date:
        if is_business_day(current):
            count += 1
        current = current.shift(days=1)

    return count

# Usage
start = arrow.get('2024-02-05')  # Monday
delivery = add_business_days(start, 5)  # 5 business days later
print(f"Delivery date: {delivery.format('YYYY-MM-DD dddd')}")
```

---

## 9. World Clock Application

### Problem
Display current time in multiple timezones simultaneously.

### Solution

```python
import arrow

def world_clock(timezones):
    """Display current time in multiple timezones."""
    utc_now = arrow.utcnow()

    print(f"\n🌍 World Clock - {utc_now.format('YYYY-MM-DD HH:mm:ss')} UTC\n")

    for city, tz in timezones.items():
        local_time = utc_now.to(tz)
        offset = local_time.format('ZZ')
        time_str = local_time.format('HH:mm:ss')

        print(f"{city:15} {time_str} (UTC{offset})")

# Usage
timezones = {
    'New York': 'America/New_York',
    'London': 'Europe/London',
    'Paris': 'Europe/Paris',
    'Tokyo': 'Asia/Tokyo',
    'Sydney': 'Australia/Sydney',
    'Dubai': 'Asia/Dubai',
    'Mumbai': 'Asia/Kolkata',
}

world_clock(timezones)
```

---

## 10. Time Series Generation

### Problem
Generate evenly-spaced timestamps for time series data.

### Solution

```python
import arrow

def generate_time_series(start, end, interval='hour'):
    """Generate time series between start and end."""
    timestamps = []
    current = start

    while current <= end:
        timestamps.append(current)

        if interval == 'minute':
            current = current.shift(minutes=1)
        elif interval == 'hour':
            current = current.shift(hours=1)
        elif interval == 'day':
            current = current.shift(days=1)

    return timestamps

# Usage
start = arrow.get('2024-02-01 00:00:00')
end = arrow.get('2024-02-01 23:59:59')

hourly_data = generate_time_series(start, end, 'hour')
print(f"Generated {len(hourly_data)} hourly timestamps")
```

---

## 11. Age Calculation

### Problem
Calculate someone's age from their birthdate.

### Solution

```python
import arrow

def calculate_age(birthdate):
    """Calculate age from birthdate."""
    if isinstance(birthdate, str):
        birthdate = arrow.get(birthdate)

    now = arrow.utcnow()
    age = now.year - birthdate.year

    # Adjust if birthday hasn't occurred this year
    if (now.month, now.day) < (birthdate.month, birthdate.day):
        age -= 1

    return age

# Usage
age = calculate_age('1990-05-15')
print(f"Age: {age} years")
```

---

## 12. Session Timeout Tracking

### Problem
Track user sessions and expire them after inactivity.

### Solution

```python
import arrow

class SessionManager:
    def __init__(self, timeout_minutes=30):
        self.sessions = {}
        self.timeout = timeout_minutes

    def create_session(self, user_id):
        """Create new session."""
        self.sessions[user_id] = {
            'created': arrow.utcnow(),
            'last_activity': arrow.utcnow()
        }

    def update_activity(self, user_id):
        """Update last activity time."""
        if user_id in self.sessions:
            self.sessions[user_id]['last_activity'] = arrow.utcnow()

    def is_session_valid(self, user_id):
        """Check if session is still valid."""
        if user_id not in self.sessions:
            return False

        session = self.sessions[user_id]
        elapsed = arrow.utcnow() - session['last_activity']

        return elapsed.total_seconds() < (self.timeout * 60)

    def cleanup_expired(self):
        """Remove expired sessions."""
        expired = [
            uid for uid in self.sessions
            if not self.is_session_valid(uid)
        ]

        for uid in expired:
            del self.sessions[uid]

        return len(expired)
```

---

## Best Practices Summary

1. **Always use UTC internally** - Convert to local only for display
2. **Be explicit about timezones** - Don't rely on system defaults
3. **Use ISO 8601 for storage** - Standard format for databases and APIs
4. **Handle DST carefully** - Test code around DST transitions
5. **Validate user input** - Always validate date strings before parsing
6. **Use appropriate precision** - Seconds vs milliseconds vs microseconds
7. **Document timezone assumptions** - Make it clear what timezone you expect

---

For more examples, check out the `examples/` directory!
