# Timezone Guide

A comprehensive guide to handling timezones with Arrow.

## Understanding Timezones

### What is a Timezone?

A timezone is a region of the globe that observes a uniform standard time. Timezones are defined by their offset from Coordinated Universal Time (UTC).

**Example:**
- UTC+0: London (GMT/BST)
- UTC-5/-4: New York (EST/EDT)
- UTC+9: Tokyo (JST)

### UTC: The Universal Reference

**UTC (Coordinated Universal Time)** is the primary time standard by which the world regulates clocks and time. It's not affected by Daylight Saving Time and serves as the reference point for all timezones.

**Why UTC Matters:**
- No DST transitions
- Unambiguous
- Ideal for storage and calculations
- Universal standard

---

## Working with Timezones in Arrow

### Getting Current Time

```python
import arrow

# UTC time (recommended)
utc_now = arrow.utcnow()
print(utc_now)  # <Arrow [2024-02-07T14:30:45.123456+00:00]>

# Local system time
local_now = arrow.now()
print(local_now)  # Uses system timezone

# Specific timezone
ny_now = arrow.now('America/New_York')
tokyo_now = arrow.now('Asia/Tokyo')
```

### Creating Timezone-Aware Dates

```python
import arrow

# Method 1: Specify timezone during creation
dt = arrow.get('2024-02-07 14:30:00', tzinfo='America/New_York')

# Method 2: Create in UTC then convert
dt = arrow.get('2024-02-07 14:30:00').replace(tzinfo='UTC')

# Method 3: Parse ISO 8601 with timezone
dt = arrow.get('2024-02-07T14:30:00-05:00')
```

### Converting Between Timezones

```python
import arrow

# Start with UTC
utc = arrow.utcnow()

# Convert to different timezones
ny = utc.to('America/New_York')
london = utc.to('Europe/London')
tokyo = utc.to('Asia/Tokyo')

# All represent the same moment in time
assert utc.timestamp() == ny.timestamp() == tokyo.timestamp()
```

---

## Common Timezone Names

### North America
```python
'America/New_York'      # Eastern Time
'America/Chicago'       # Central Time
'America/Denver'        # Mountain Time
'America/Los_Angeles'   # Pacific Time
'America/Anchorage'     # Alaska Time
'America/Toronto'       # Toronto
'America/Mexico_City'   # Mexico City
```

### Europe
```python
'Europe/London'         # GMT/BST
'Europe/Paris'          # CET/CEST
'Europe/Berlin'         # CET/CEST
'Europe/Moscow'         # MSK
'Europe/Istanbul'       # TRT
```

### Asia
```python
'Asia/Tokyo'           # JST
'Asia/Shanghai'        # CST
'Asia/Hong_Kong'       # HKT
'Asia/Singapore'       # SGT
'Asia/Dubai'           # GST
'Asia/Kolkata'         # IST (India)
```

### Pacific
```python
'Australia/Sydney'     # AEDT/AEST
'Australia/Melbourne'  # AEDT/AEST
'Pacific/Auckland'     # NZDT/NZST
```

---

## Daylight Saving Time (DST)

### What is DST?

Daylight Saving Time is the practice of advancing clocks during warmer months so that darkness falls at a later clock time. Not all regions observe DST.

### DST Transitions

**Spring Forward (March):**
- 2:00 AM becomes 3:00 AM
- One hour is "lost"

**Fall Back (November):**
- 2:00 AM becomes 1:00 AM again
- One hour is repeated

### Handling DST in Arrow

```python
import arrow

# Check if DST is active
winter = arrow.get('2024-01-15', tzinfo='America/New_York')
summer = arrow.get('2024-07-15', tzinfo='America/New_York')

print(f"Winter DST: {winter.dst().total_seconds() != 0}")  # False (EST)
print(f"Summer DST: {summer.dst().total_seconds() != 0}")  # True (EDT)

# Get UTC offset
print(f"Winter offset: {winter.format('ZZ')}")  # -05:00 (EST)
print(f"Summer offset: {summer.format('ZZ')}")  # -04:00 (EDT)
```

### DST Transition Example

```python
import arrow

# Night before DST starts (Spring forward)
dt = arrow.get('2024-03-10 01:30:00', tzinfo='America/New_York')
print(f"Before DST: {dt.format('YYYY-MM-DD HH:mm:ss ZZ')}")

# Add 2 hours - crosses DST boundary
later = dt.shift(hours=2)
print(f"After DST: {later.format('YYYY-MM-DD HH:mm:ss ZZ')}")
# Note: Clock time jumped from 1:30 AM to 4:30 AM (3 hours)
```

### The "Missing Hour" Problem

```python
import arrow

# This time doesn't exist! (2:00-3:00 AM skipped)
try:
    # Arrow handles this gracefully
    dt = arrow.get('2024-03-10 02:30:00', tzinfo='America/New_York')
    print(f"Arrow adjusted to: {dt}")
except Exception as e:
    print(f"Error: {e}")
```

### Best Practices for DST

1. **Always use UTC for calculations**
2. **Convert to local time only for display**
3. **Test code around March and November**
4. **Don't assume fixed UTC offsets**
5. **Use timezone names, not abbreviations** (EST vs America/New_York)

---

## Common Timezone Patterns

### Pattern 1: Store UTC, Display Local

```python
import arrow

class Event:
    def __init__(self, title, utc_time):
        self.title = title
        self.utc_time = utc_time  # Store in UTC

    def display_time(self, timezone='local'):
        """Display in user's timezone."""
        return self.utc_time.to(timezone).format('YYYY-MM-DD HH:mm:ss')

# Usage
event = Event('Meeting', arrow.utcnow().shift(hours=2))
print(f"In New York: {event.display_time('America/New_York')}")
print(f"In Tokyo: {event.display_time('Asia/Tokyo')}")
```

### Pattern 2: World Clock

```python
import arrow

def show_world_times():
    """Display current time in major cities."""
    utc = arrow.utcnow()

    cities = {
        'UTC': 'UTC',
        'New York': 'America/New_York',
        'London': 'Europe/London',
        'Paris': 'Europe/Paris',
        'Dubai': 'Asia/Dubai',
        'Tokyo': 'Asia/Tokyo',
        'Sydney': 'Australia/Sydney',
    }

    print(f"\n🌍 World Times - {utc.format('YYYY-MM-DD')}\n")

    for city, tz in cities.items():
        local = utc.to(tz)
        print(f"{city:12} {local.format('HH:mm:ss')} "
              f"({local.format('ZZ')})")
```

### Pattern 3: Meeting Scheduler

```python
import arrow

def schedule_meeting(date_str, time_str, organizer_tz):
    """Schedule a meeting and show time for all participants."""
    # Parse in organizer's timezone
    dt_str = f"{date_str} {time_str}"
    meeting_time = arrow.get(dt_str, tzinfo=organizer_tz)

    # Show in different timezones
    timezones = {
        'Organizer': organizer_tz,
        'New York': 'America/New_York',
        'London': 'Europe/London',
        'Tokyo': 'Asia/Tokyo',
    }

    print(f"\nMeeting scheduled for:\n")
    for name, tz in timezones.items():
        local = meeting_time.to(tz)
        print(f"{name:12} {local.format('YYYY-MM-DD HH:mm ZZ')}")

# Usage
schedule_meeting('2024-02-15', '14:00', 'America/New_York')
```

### Pattern 4: Timezone-Safe Date Range

```python
import arrow

def get_business_day_range(start_tz, end_tz, timezone='UTC'):
    """Get business days in a specific timezone."""
    # Convert to target timezone
    start = arrow.get(start_tz).to(timezone).floor('day')
    end = arrow.get(end_tz).to(timezone).floor('day')

    business_days = []
    current = start

    while current <= end:
        if current.weekday() < 5:  # Monday-Friday
            business_days.append(current)
        current = current.shift(days=1)

    return business_days
```

---

## Timezone Pitfalls to Avoid

### Pitfall 1: Using Timezone Abbreviations

```python
# ❌ BAD: Abbreviations are ambiguous
# CST could be Central Standard Time (US) or China Standard Time
dt = arrow.now('CST')  # Don't do this!

# ✅ GOOD: Use full timezone names
dt = arrow.now('America/Chicago')  # Unambiguous
```

### Pitfall 2: Assuming Fixed Offsets

```python
# ❌ BAD: Hardcoding offsets
ny_time = utc_time.shift(hours=-5)  # Wrong during DST!

# ✅ GOOD: Use timezone conversion
ny_time = utc_time.to('America/New_York')  # Handles DST
```

### Pitfall 3: Comparing Across Timezones

```python
# ❌ BAD: Comparing without normalization
ny_time = arrow.now('America/New_York')
tokyo_time = arrow.now('Asia/Tokyo')
if ny_time > tokyo_time:  # Meaningless comparison!
    pass

# ✅ GOOD: Convert to UTC first
ny_utc = arrow.now('America/New_York').to('UTC')
tokyo_utc = arrow.now('Asia/Tokyo').to('UTC')
if ny_utc > tokyo_utc:
    pass
```

### Pitfall 4: Ignoring User's Timezone

```python
# ❌ BAD: Showing server time to users
server_time = arrow.utcnow()
print(f"Event at: {server_time}")  # Confusing for users!

# ✅ GOOD: Convert to user's timezone
server_time = arrow.utcnow()
user_time = server_time.to(user_timezone)
print(f"Event at: {user_time.format('YYYY-MM-DD HH:mm')}")
```

---

## Testing Timezone Code

### Use freezegun for Deterministic Tests

```python
import arrow
from freezegun import freeze_time

@freeze_time("2024-02-07 12:00:00", tz_offset=0)
def test_timezone_conversion():
    """Test with frozen time."""
    utc = arrow.utcnow()
    ny = utc.to('America/New_York')

    assert utc.format('HH:mm') == '12:00'
    assert ny.format('HH:mm') == '07:00'  # EST

@freeze_time("2024-07-07 12:00:00", tz_offset=0)
def test_dst_timezone():
    """Test DST handling."""
    utc = arrow.utcnow()
    ny = utc.to('America/New_York')

    assert ny.format('HH:mm') == '08:00'  # EDT (DST active)
```

### Test DST Transitions

```python
import arrow

def test_dst_spring_forward():
    """Test spring DST transition."""
    # Night before DST
    before = arrow.get('2024-03-10 01:00:00',
                       tzinfo='America/New_York')

    # 2 hours later (crosses DST)
    after = before.shift(hours=2)

    # Verify UTC offset changed
    assert before.format('ZZ') == '-05:00'  # EST
    assert after.format('ZZ') == '-04:00'   # EDT

def test_dst_fall_back():
    """Test fall DST transition."""
    before = arrow.get('2024-11-03 01:00:00',
                       tzinfo='America/New_York')
    after = before.shift(hours=2)

    # Verify UTC offset changed back
    assert after.format('ZZ') == '-05:00'  # EST
```

---

## Timezone Resources

### Timezone Database
- **IANA Time Zone Database**: Official source for timezone data
- **URL**: https://www.iana.org/time-zones

### Useful Tools
- **timeanddate.com**: Compare times across timezones
- **worldtimebuddy.com**: Visual timezone converter
- **everytimezone.com**: See all timezones at once

### Python Libraries
- **arrow**: Human-friendly dates (this project!)
- **pytz**: Timezone definitions
- **python-dateutil**: Date parsing utilities
- **freezegun**: Time mocking for tests

---

## Quick Reference

### Key Concepts
- **UTC**: Universal reference time
- **Timezone**: Region with uniform time
- **DST**: Seasonal clock adjustment
- **Offset**: Hours from UTC (+/- HH:MM)

### Arrow Timezone Methods
```python
arrow.utcnow()              # Current UTC time
arrow.now('timezone')       # Current time in timezone
dt.to('timezone')           # Convert timezone
dt.format('ZZ')             # Show UTC offset
dt.dst()                    # Get DST offset
```

### Best Practices
1. Store everything in UTC
2. Convert to local for display only
3. Use full timezone names
4. Test DST transitions
5. Validate user timezone input

---

**Remember:** When in doubt, use UTC internally and convert to local timezones only when displaying to users!
