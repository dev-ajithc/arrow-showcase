# Getting Started with Arrow

## What is Arrow?

Arrow is a Python library for working with dates and times. It offers a sensible, human-friendly approach to creating, manipulating, formatting and converting dates, times, and timestamps.

Arrow aims to help you work with dates and times with fewer imports and much less code.

## Why Arrow?

If you've ever fought with Python's `datetime` module, you know the pain:
- Timezone handling is confusing
- Formatting dates requires memorizing strftime codes
- Parsing dates from strings is cumbersome
- Timezone-aware operations are error-prone

Arrow makes all of this simple and intuitive.

## Installation

```bash
pip install arrow
```

Or install with this project's dependencies:

```bash
pip install -r requirements.txt
```

## Your First Arrow Example

```python
import arrow

# Get current UTC time
utc = arrow.utcnow()
print(utc)

# Shift time by 5 hours
future = utc.shift(hours=5)
print(future.format('YYYY-MM-DD HH:mm'))
```

That's it! You're now working with dates the easy way.

## Basic Concepts

### 1. Creating Arrow Objects

```python
import arrow

# Current time
now = arrow.now()
utc_now = arrow.utcnow()

# From string
dt = arrow.get('2024-02-07')
dt = arrow.get('2024-02-07 14:30:45', 'YYYY-MM-DD HH:mm:ss')

# From timestamp
dt = arrow.get(1707318645)

# From datetime object
from datetime import datetime
dt = arrow.get(datetime.now())
```

### 2. Formatting Dates

```python
dt = arrow.utcnow()

# Built-in formats
print(dt.format('YYYY-MM-DD'))           # 2024-02-07
print(dt.format('YYYY-MM-DD HH:mm:ss'))  # 2024-02-07 14:30:45
print(dt.format('MMMM DD, YYYY'))        # February 07, 2024

# ISO 8601
print(dt.isoformat())
```

### 3. Shifting Time

```python
dt = arrow.utcnow()

# Add time
future = dt.shift(hours=5)
tomorrow = dt.shift(days=1)
next_week = dt.shift(weeks=1)
next_month = dt.shift(months=1)

# Subtract time
past = dt.shift(hours=-2)
yesterday = dt.shift(days=-1)
```

### 4. Timezone Operations

```python
utc = arrow.utcnow()

# Convert to local time
local = utc.to('local')

# Convert to specific timezone
ny = utc.to('America/New_York')
tokyo = utc.to('Asia/Tokyo')
```

### 5. Humanized Dates

```python
past = arrow.utcnow().shift(hours=-2)
print(past.humanize())  # "2 hours ago"

future = arrow.utcnow().shift(days=3)
print(future.humanize())  # "in 3 days"
```

## Common Patterns

### File Naming with Timestamps

```python
import arrow

timestamp = arrow.utcnow().format('YYYYMMDD_HHmmss')
filename = f"backup_{timestamp}.tar.gz"
# Result: backup_20240207_143045.tar.gz
```

### Scheduled Tasks

```python
import arrow

# Schedule for 2 AM UTC
schedule_time = arrow.now('UTC').replace(hour=2, minute=0, second=0)

if schedule_time < arrow.utcnow():
    schedule_time = schedule_time.shift(days=1)

print(f"Next run: {schedule_time}")
```

### Date Ranges

```python
import arrow

start = arrow.get('2024-02-01')
end = arrow.get('2024-02-05')

for date in arrow.Arrow.range('day', start, end):
    print(date.format('YYYY-MM-DD'))
```

### API Date Handling

```python
import arrow

# Parsing API response
api_date = "2024-02-07T14:30:45Z"
dt = arrow.get(api_date)

# Formatting for API request
request_date = arrow.utcnow().isoformat()
```

## Best Practices

### 1. Always Use UTC Internally

```python
# Good
utc_time = arrow.utcnow()

# Convert to local only for display
display_time = utc_time.to('local')
```

### 2. Be Explicit with Timezones

```python
# Good - explicit timezone
dt = arrow.now('America/New_York')

# Avoid - ambiguous
dt = arrow.now()  # What timezone is this?
```

### 3. Use ISO 8601 for Storage and APIs

```python
# Store dates in ISO 8601 format
stored_date = arrow.utcnow().isoformat()

# Parse back
dt = arrow.get(stored_date)
```

### 4. Handle Timezones Carefully

```python
# Don't compare naive datetimes across timezones
# Always convert to UTC first

dt1 = arrow.now('America/New_York').to('UTC')
dt2 = arrow.now('Asia/Tokyo').to('UTC')

if dt1 > dt2:
    print("dt1 is later")
```

## Next Steps

- Explore **basic examples**: `python examples/basic_examples.py`
- Learn **formatting**: `python examples/formatting_parsing.py`
- Master **timezones**: `python examples/timezone_operations.py`
- Build **automation**: `python examples/automation_examples.py`
- Try **advanced features**: `python examples/advanced_examples.py`
- See **integrations**: `python examples/integration_examples.py`

## Common Pitfalls to Avoid

### 1. Timezone Confusion

```python
# BAD - mixing naive and aware datetimes
naive = arrow.get('2024-02-07')
aware = arrow.now('UTC')
# Don't compare these directly!

# GOOD - both timezone-aware
dt1 = arrow.get('2024-02-07', tzinfo='UTC')
dt2 = arrow.now('UTC')
```

### 2. DST Transitions

```python
# Be aware of DST transitions
summer = arrow.get('2024-07-01', tzinfo='America/New_York')
winter = arrow.get('2024-01-01', tzinfo='America/New_York')

# Their UTC offsets are different!
print(summer.format('ZZ'))  # -04:00 (EDT)
print(winter.format('ZZ'))  # -05:00 (EST)
```

### 3. Timestamp Precision

```python
# Unix timestamps are in seconds by default
ts = arrow.utcnow().timestamp()  # Seconds

# For milliseconds, multiply by 1000
ts_ms = int(arrow.utcnow().timestamp() * 1000)
```

## Comparison with datetime

### datetime (Standard Library)

```python
from datetime import datetime, timedelta
import pytz

# Current time in specific timezone
tz = pytz.timezone('America/New_York')
dt = datetime.now(tz)

# Add 5 hours
future = dt + timedelta(hours=5)

# Format
formatted = future.strftime('%Y-%m-%d %H:%M:%S')
```

### Arrow (Simpler)

```python
import arrow

# Current time in specific timezone
dt = arrow.now('America/New_York')

# Add 5 hours
future = dt.shift(hours=5)

# Format
formatted = future.format('YYYY-MM-DD HH:mm:ss')
```

Arrow reduces complexity and makes code more readable!

## Quick Reference

### Creation
- `arrow.now()` - Local time
- `arrow.utcnow()` - UTC time
- `arrow.get('2024-02-07')` - Parse string

### Manipulation
- `.shift(hours=5)` - Add/subtract time
- `.replace(hour=0)` - Replace components
- `.to('UTC')` - Convert timezone

### Formatting
- `.format('YYYY-MM-DD')` - Custom format
- `.isoformat()` - ISO 8601
- `.humanize()` - Relative time

### Properties
- `.year`, `.month`, `.day` - Date components
- `.hour`, `.minute`, `.second` - Time components
- `.timestamp()` - Unix timestamp

## Resources

- Arrow Documentation: https://arrow.readthedocs.io/
- Arrow GitHub: https://github.com/arrow-py/arrow
- ISO 8601 Standard: https://en.wikipedia.org/wiki/ISO_8601
- Timezone Database: https://www.iana.org/time-zones

---

**Ready to dive deeper?** Check out the other documentation files and examples!
