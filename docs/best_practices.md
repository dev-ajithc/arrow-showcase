# Arrow Best Practices

Essential guidelines for working with dates and times using Arrow.

## 1. Always Use UTC Internally

### ❌ Bad Practice
```python
import arrow

# Using local time for everything
now = arrow.now()  # Which timezone?
stored_time = now.format('YYYY-MM-DD HH:mm:ss')
```

### ✅ Good Practice
```python
import arrow

# Use UTC for storage and processing
utc_time = arrow.utcnow()
stored_time = utc_time.isoformat()

# Convert to local only for display
display_time = utc_time.to('local')
```

**Why?** UTC is unambiguous and doesn't have DST transitions. Store everything in UTC and convert to local timezones only when displaying to users.

---

## 2. Be Explicit About Timezones

### ❌ Bad Practice
```python
# Ambiguous - what timezone is this?
dt = arrow.now()
meeting_time = arrow.get('2024-02-07 14:30:00')
```

### ✅ Good Practice
```python
# Explicit timezone
dt = arrow.now('UTC')
meeting_time = arrow.get('2024-02-07 14:30:00', tzinfo='America/New_York')
```

**Why?** Explicit timezones prevent confusion and bugs, especially in distributed systems.

---

## 3. Use ISO 8601 for Storage and APIs

### ❌ Bad Practice
```python
# Custom format - hard to parse
date_string = dt.format('MM/DD/YYYY HH:mm:ss')
```

### ✅ Good Practice
```python
# ISO 8601 - universally understood
date_string = dt.isoformat()
# Result: 2024-02-07T14:30:45+00:00
```

**Why?** ISO 8601 is the international standard for date representation. It's sortable, unambiguous, and widely supported.

---

## 4. Handle DST Transitions Carefully

### ❌ Bad Practice
```python
# Ignoring DST transitions
ny_time = arrow.get('2024-03-10 02:30:00', tzinfo='America/New_York')
# This time doesn't exist! (DST spring forward)
```

### ✅ Good Practice
```python
# Be aware of DST transitions
winter = arrow.get('2024-01-01 12:00:00', tzinfo='America/New_York')
summer = arrow.get('2024-07-01 12:00:00', tzinfo='America/New_York')

# Check DST status
print(f"Winter DST: {winter.dst().total_seconds() != 0}")  # False
print(f"Summer DST: {summer.dst().total_seconds() != 0}")  # True
```

**Why?** DST transitions can cause unexpected behavior. Always test your code around March and November for locations that observe DST.

---

## 5. Validate User Input

### ❌ Bad Practice
```python
# No validation - will crash on bad input
user_input = request.form['date']
dt = arrow.get(user_input)
```

### ✅ Good Practice
```python
# Validate and handle errors
user_input = request.form['date']

try:
    dt = arrow.get(user_input, 'YYYY-MM-DD')
    if dt > arrow.utcnow().shift(years=100):
        raise ValueError("Date too far in the future")
except arrow.parser.ParserError:
    return "Invalid date format. Please use YYYY-MM-DD"
except ValueError as e:
    return str(e)
```

**Why?** User input is unpredictable. Always validate and provide helpful error messages.

---

## 6. Use Appropriate Precision

### ❌ Bad Practice
```python
# Unnecessary precision for logs
log_timestamp = dt.format('YYYY-MM-DD HH:mm:ss.SSSSSS')
```

### ✅ Good Practice
```python
# Match precision to use case
log_timestamp = dt.format('YYYY-MM-DD HH:mm:ss')      # Logs
api_timestamp = dt.isoformat()                         # APIs
filename_ts = dt.format('YYYYMMDD_HHmmss')            # Filenames
unix_ts = int(dt.timestamp())                          # Unix time
```

**Why?** Too much precision wastes space and makes data harder to read. Use seconds for logs, ISO 8601 for APIs.

---

## 7. Don't Compare Naive Datetimes

### ❌ Bad Practice
```python
# Comparing times from different timezones
ny_time = arrow.now('America/New_York')
tokyo_time = arrow.now('Asia/Tokyo')

if ny_time > tokyo_time:  # This comparison is wrong!
    print("NY is later")
```

### ✅ Good Practice
```python
# Convert to UTC before comparing
ny_utc = arrow.now('America/New_York').to('UTC')
tokyo_utc = arrow.now('Asia/Tokyo').to('UTC')

if ny_utc > tokyo_utc:
    print("NY time is later")
```

**Why?** Comparing times from different timezones directly is meaningless. Always normalize to UTC first.

---

## 8. Use Floor/Ceil for Time Ranges

### ❌ Bad Practice
```python
# Manual date manipulation
start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
end = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
```

### ✅ Good Practice
```python
# Use floor and ceil
start = dt.floor('day')
end = dt.ceil('day')

# Or use span
day_start, day_end = dt.span('day')
```

**Why?** Floor and ceil are clearer and less error-prone than manual manipulation.

---

## 9. Prefer Shift Over Replace for Dates

### ❌ Bad Practice
```python
# Using replace can be confusing
next_month = dt.replace(month=dt.month + 1)  # What if month is 12?
```

### ✅ Good Practice
```python
# Shift handles edge cases automatically
next_month = dt.shift(months=1)  # Works even for December
```

**Why?** Shift automatically handles month/year boundaries, leap years, and other edge cases.

---

## 10. Document Timezone Assumptions

### ❌ Bad Practice
```python
def process_date(date_string):
    """Process a date."""
    return arrow.get(date_string)
```

### ✅ Good Practice
```python
def process_date(date_string: str, timezone: str = 'UTC') -> arrow.Arrow:
    """
    Process a date string.

    Args:
        date_string: ISO 8601 formatted date string
        timezone: Timezone to use (default: UTC)

    Returns:
        Arrow object in specified timezone

    Example:
        >>> process_date('2024-02-07T14:30:00Z')
        <Arrow [2024-02-07T14:30:00+00:00]>
    """
    return arrow.get(date_string).to(timezone)
```

**Why?** Clear documentation prevents confusion about timezone handling.

---

## 11. Handle Leap Years and Month Boundaries

### ❌ Bad Practice
```python
# Assuming all months have 30 days
next_month_same_day = dt.replace(month=dt.month + 1)
# Fails on Jan 31 -> Feb 31 (doesn't exist!)
```

### ✅ Good Practice
```python
# Use shift which handles boundaries
next_month = dt.shift(months=1)

# Or use ceiling/flooring
month_end = dt.ceil('month')
```

**Why?** Arrow handles edge cases like leap years and varying month lengths automatically.

---

## 12. Cache Timezone Objects for Performance

### ❌ Bad Practice
```python
# Creating timezone object repeatedly in loop
for item in large_list:
    dt = arrow.now('America/New_York')  # Slow!
    item['timestamp'] = dt
```

### ✅ Good Practice
```python
# Get time once, use many times
now = arrow.now('America/New_York')

for item in large_list:
    item['timestamp'] = now  # Fast!
```

**Why?** Timezone lookups have overhead. Cache when possible for performance.

---

## 13. Use Context-Appropriate Formats

### ❌ Bad Practice
```python
# Using same format everywhere
filename = f"log_{dt.isoformat()}.txt"  # Contains colons!
print(f"Created: {dt.format('YYYYMMDD_HHmmss')}")  # Hard to read
```

### ✅ Good Practice
```python
# Match format to context
filename = f"log_{dt.format('YYYYMMDD_HHmmss')}.txt"  # Safe for files
print(f"Created: {dt.format('YYYY-MM-DD HH:mm:ss')}")  # Human-readable
api_payload = {'timestamp': dt.isoformat()}  # Standard for APIs
```

**Why?** Different contexts require different formats. Filenames need safe characters, humans need readability, APIs need standards.

---

## 14. Test Time-Dependent Code Properly

### ❌ Bad Practice
```python
def test_reminder():
    reminder = create_reminder(arrow.utcnow().shift(hours=1))
    # Test will fail randomly based on when it runs!
```

### ✅ Good Practice
```python
from freezegun import freeze_time

@freeze_time("2024-02-07 12:00:00")
def test_reminder():
    # Time is frozen - test is deterministic
    reminder = create_reminder(arrow.utcnow().shift(hours=1))
    assert reminder.due_at.hour == 13
```

**Why?** Use libraries like `freezegun` to make time-dependent tests deterministic and reliable.

---

## 15. Avoid Storing Datetimes as Strings

### ❌ Bad Practice
```python
# Storing as string in database
record = {
    'created_at': dt.format('YYYY-MM-DD HH:mm:ss'),
    'timezone': 'America/New_York'
}
```

### ✅ Good Practice
```python
# Store as ISO 8601 with timezone info
record = {
    'created_at': dt.isoformat(),  # Includes timezone
}

# Or store as Unix timestamp if appropriate
record = {
    'created_at': int(dt.timestamp())
}
```

**Why?** ISO format or Unix timestamps are easier to query and sort in databases.

---

## Common Pitfalls Checklist

- [ ] All stored times are in UTC
- [ ] Timezone conversions only happen for display
- [ ] All datetimes include timezone information
- [ ] DST transitions are tested
- [ ] User date inputs are validated
- [ ] Date comparisons use normalized timezones
- [ ] Code is tested with frozen time
- [ ] API dates use ISO 8601
- [ ] Filenames use safe date formats
- [ ] Documentation specifies timezone assumptions

---

## Quick Reference Table

| Use Case | Recommended Approach |
|----------|---------------------|
| Storage | ISO 8601 (`dt.isoformat()`) |
| Database | Unix timestamp or ISO 8601 |
| API Request/Response | ISO 8601 |
| Logging | `YYYY-MM-DD HH:mm:ss` |
| Filenames | `YYYYMMDD_HHmmss` |
| User Display | Localized format |
| Comparisons | Convert to UTC first |
| Calculations | Use `.shift()` |
| Time Ranges | Use `.span()` or `.floor()`/`.ceil()` |

---

## Performance Tips

1. **Avoid repeated timezone conversions** in loops
2. **Cache Arrow objects** when possible
3. **Use Unix timestamps** for high-frequency operations
4. **Batch timezone conversions** for bulk data
5. **Profile before optimizing** - Arrow is already fast

---

## Security Considerations

1. **Validate all user-provided dates** before parsing
2. **Set reasonable bounds** on date inputs (e.g., not 1000 years in future)
3. **Sanitize dates in filenames** to prevent directory traversal
4. **Use timezone allowlists** if accepting timezone input
5. **Log timezone conversions** for audit trails

---

## Further Reading

- [ISO 8601 Standard](https://en.wikipedia.org/wiki/ISO_8601)
- [IANA Time Zone Database](https://www.iana.org/time-zones)
- [Arrow Documentation](https://arrow.readthedocs.io/)
- [The Falsehoods Programmers Believe About Time](https://gist.github.com/timvisee/fcda9bbdff88d45cc9061606b4b923ca)

---

**Remember:** Time and timezones are complex. When in doubt, use UTC internally and convert to local time only for display!
