# Arrow Showcase: Date and Time Without the Pain 📅⏰

> I used to dread handling dates in Python. Time zones, formatting, parsing… pure chaos. Then I found Arrow.

A comprehensive collection of Arrow examples, utilities, and best practices for handling dates, times, and timezones in Python with elegance and simplicity.

## 🎯 Why This Project?

I used to dread handling dates in Python. Timezone conversions, date formatting, parsing strings—it was always a mess. Then I discovered Arrow, and suddenly working with time became effortless. I ended up automating reminders, scheduling backups, and even making a script that auto-renamed files with timestamps. If you've ever fought with Python's `datetime`, Arrow feels like a breath of fresh air.

## ✨ Features

- **Basic Examples**: Fundamental Arrow operations and time manipulation
- **Formatting & Parsing**: Convert between formats, parse strings, handle ISO 8601
- **Timezone Operations**: UTC/local conversion, world clock, DST handling
- **Automation Examples**: Timestamped files, scheduled backups, reminders, log rotation
- **Advanced Features**: Date ranges, business days, humanization, time series
- **Integration Examples**: Pandas, JSON, databases, APIs
- **Reusable Utilities**: Drop-in helper functions for common operations
- **Full Test Coverage**: Comprehensive unit tests with >85% coverage

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/yourusername/arrow-showcase.git
cd arrow-showcase
pip install -r requirements.txt
```

### Your First Arrow Example

```python
import arrow

# Get current time and shift it
dt = arrow.utcnow()
print(dt.shift(hours=5).format('YYYY-MM-DD HH:mm'))
```

That's it! You now have elegant date handling. 😎

## 📚 Examples

### Basic Usage

Run the basic examples to see fundamental Arrow features:

```bash
python examples/basic_examples.py
```

Features demonstrated:
- Current time in UTC and local timezones
- Time shifting (add/subtract hours, days, months)
- Time ranges and iteration
- Relative time calculations
- Time comparisons
- Accessing date/time properties

### Formatting & Parsing

See various ways to format and parse dates:

```bash
python examples/formatting_parsing.py
```

Includes:
- Format conversions (ISO, US, EU formats)
- ISO 8601 formatting
- Custom format strings
- Locale-aware formatting
- String parsing with various formats
- Unix timestamp conversion

### Timezone Operations

Master timezone handling:

```bash
python examples/timezone_operations.py
```

Demonstrates:
- UTC and local time conversion
- Converting between different timezones
- Timezone-aware calculations
- World clock implementation
- DST (Daylight Saving Time) handling
- Timezone information display

### Automation Examples

See real-world automation use cases:

```bash
python examples/automation_examples.py
```

Features:
- Timestamped filename generation
- Scheduled backup systems
- Reminder/notification systems
- Log file rotation by date
- Deadline tracking
- Periodic task scheduling
- File organization by date

### Advanced Features

Explore advanced Arrow capabilities:

```bash
python examples/advanced_examples.py
```

Includes:
- Date ranges with various spans
- Business day calculations
- Humanized date formatting
- Time series generation
- Calendar operations (floor/ceil)
- Span operations
- Replace operations
- JSON serialization

### Integration Examples

See how Arrow integrates with other libraries:

```bash
python examples/integration_examples.py
```

Demonstrates:
- Pandas DataFrame date operations
- JSON serialization/deserialization
- Database timestamp handling
- API date parsing and formatting
- Configuration file date handling
- CSV date processing
- Logging with timestamps

## 🛠️ Utilities

### Date Helpers

Convenient functions for common date operations:

```python
from utils.date_helpers import get_date_range, is_business_day, age_from_birthdate

# Generate date range
start = arrow.get('2024-02-01')
end = arrow.get('2024-02-05')
dates = get_date_range(start, end, 'day')

# Check business days
if is_business_day(arrow.utcnow()):
    print("It's a weekday!")

# Calculate age
age = age_from_birthdate(arrow.get('1990-01-01'))
```

### Timezone Helpers

Functions for timezone operations:

```python
from utils.timezone_helpers import convert_timezone, get_world_times

# Convert between timezones
ny_time = convert_timezone(utc_time, 'UTC', 'America/New_York')

# World clock
timezones = ['UTC', 'America/New_York', 'Asia/Tokyo']
times = get_world_times(arrow.utcnow(), timezones)
```

### Formatters

Custom date formatting utilities:

```python
from utils.formatters import format_for_filename, format_for_api, DateFormatter

# Safe filename
filename = f"backup_{format_for_filename()}.tar.gz"
# Result: backup_20240207_143045.tar.gz

# API-ready format
api_date = format_for_api(arrow.utcnow())

# Custom formatter
formatter = DateFormatter()
formatted = formatter.format(arrow.utcnow(), 'short')
```

### Schedulers

Task scheduling and reminder systems:

```python
from utils.schedulers import Reminder, TaskScheduler

# Create reminder
reminder = Reminder()
reminder.add("Team Meeting", arrow.utcnow().shift(hours=2))

# Schedule daily task
scheduler = TaskScheduler()
scheduler.add_daily_task("backup", 2, 0, backup_function)
```

### Timestamp Tools

Timestamp generation and manipulation:

```python
from utils.timestamp_tools import generate_timestamped_filename, parse_timestamp_filename

# Generate timestamped filename
filename = generate_timestamped_filename('backup', '.zip')
# Result: backup_20240207_143045.zip

# Parse timestamp from filename
dt = parse_timestamp_filename('backup_20240207_143045.zip')
```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage report:

```bash
pytest --cov=. --cov-report=term-missing
```

Run code quality checks:

```bash
flake8 .
```

Run type checking:

```bash
mypy utils/ examples/
```

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[getting_started.md](docs/getting_started.md)** - Introduction to Arrow and basic concepts
- **[use_cases.md](docs/use_cases.md)** - Real-world use cases and patterns
- **[best_practices.md](docs/best_practices.md)** - Best practices and common pitfalls
- **[timezone_guide.md](docs/timezone_guide.md)** - Complete guide to timezone handling

## 🎨 Project Structure

```
arrow-showcase/
├── examples/              # Example scripts
│   ├── basic_examples.py
│   ├── formatting_parsing.py
│   ├── timezone_operations.py
│   ├── automation_examples.py
│   ├── advanced_examples.py
│   └── integration_examples.py
├── utils/                 # Reusable utilities
│   ├── date_helpers.py
│   ├── timezone_helpers.py
│   ├── formatters.py
│   ├── schedulers.py
│   └── timestamp_tools.py
├── tests/                 # Unit tests
│   ├── test_date_helpers.py
│   ├── test_timezone_helpers.py
│   ├── test_formatters.py
│   ├── test_schedulers.py
│   └── test_timestamp_tools.py
├── docs/                  # Documentation
│   ├── getting_started.md
│   ├── use_cases.md
│   ├── best_practices.md
│   └── timezone_guide.md
├── data/                  # Sample data files
│   ├── sample_logs.txt
│   ├── sample_schedules.json
│   └── sample_events.csv
├── requirements.txt       # Dependencies
├── setup.cfg             # Configuration
├── .env.example          # Environment template
└── README.md
```

## 💡 Common Use Cases

### Timestamped File Naming

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

### World Clock

```python
import arrow

utc = arrow.utcnow()

timezones = {
    'New York': 'America/New_York',
    'London': 'Europe/London',
    'Tokyo': 'Asia/Tokyo',
}

for city, tz in timezones.items():
    local = utc.to(tz)
    print(f"{city}: {local.format('HH:mm:ss')}")
```

### API Date Handling

```python
import arrow

# Parse API response
api_date = "2024-02-07T14:30:45Z"
dt = arrow.get(api_date)

# Format for API request
request_date = arrow.utcnow().isoformat()
```

### Business Day Calculation

```python
import arrow

def is_business_day(date):
    return date.weekday() < 5

start = arrow.get('2024-02-07')  # Wednesday
current = start

for _ in range(5):  # Next 5 business days
    if not is_business_day(current):
        current = current.shift(days=1)
        continue
    print(current.format('YYYY-MM-DD dddd'))
    current = current.shift(days=1)
```

## 🔧 Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Example configuration:

```bash
# Timezone Configuration
DEFAULT_TIMEZONE=UTC
LOCAL_TIMEZONE=America/New_York

# Date Format Preferences
DATE_FORMAT=YYYY-MM-DD
DATETIME_FORMAT=YYYY-MM-DD HH:mm:ss

# Scheduling
BACKUP_TIME=02:00
LOG_ROTATION_DAYS=7
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Code Quality

This project maintains high code quality standards:

- **PEP 8 Compliance**: 79 character line length, proper formatting
- **Type Hints**: All functions have type annotations
- **Comprehensive Docstrings**: Every function documented with examples
- **Unit Tests**: >85% test coverage with pytest
- **Security Best Practices**: Input validation, secure file operations
- **No Flake8 Violations**: Clean, consistent code

### Quality Checks

```bash
# Run all quality checks
flake8 .
mypy utils/ examples/
pytest --cov=. --cov-report=term-missing
```

## 🔒 Security

This project follows security best practices:

- **Secure Package Versions**: Latest security patches
- **Input Validation**: All user inputs validated
- **Safe File Operations**: No directory traversal vulnerabilities
- **Environment Variables**: Sensitive data in environment
- **Proper Error Handling**: No information leakage
- **Timezone Validation**: Allowlisted timezone strings

## 📊 Sample Data

Sample data files are provided in the `data/` directory:

- **sample_logs.txt**: Example log file with timestamps
- **sample_schedules.json**: Scheduled task configurations
- **sample_events.csv**: Event data with multiple timezones

## 🎓 Learning Resources

### Arrow Documentation
- Official Docs: https://arrow.readthedocs.io/
- GitHub: https://github.com/arrow-py/arrow

### Related Topics
- ISO 8601 Standard: https://en.wikipedia.org/wiki/ISO_8601
- IANA Timezone Database: https://www.iana.org/time-zones
- Python datetime: https://docs.python.org/3/library/datetime.html

### Recommended Reading
- [The Falsehoods Programmers Believe About Time](https://gist.github.com/timvisee/fcda9bbdff88d45cc9061606b4b923ca)
- [Working with Timezones in Python](https://realpython.com/python-time-module/)

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Arrow](https://github.com/arrow-py/arrow) - The amazing date/time library
- The Python community for continuous inspiration
- All contributors who help improve this project

## 📬 Contact

Questions? Suggestions? Open an issue or reach out!

## 🌟 Why Arrow?

### Before Arrow (datetime)

```python
from datetime import datetime, timedelta
import pytz

# Get time 5 hours from now in New York
tz = pytz.timezone('America/New_York')
now = datetime.now(tz)
future = now + timedelta(hours=5)
formatted = future.strftime('%Y-%m-%d %H:%M:%S')
```

### With Arrow

```python
import arrow

# Get time 5 hours from now in New York
formatted = arrow.now('America/New_York').shift(hours=5).format('YYYY-MM-DD HH:mm:ss')
```

**Arrow makes date/time handling intuitive, readable, and enjoyable!**

---

**Made with ❤️ and lots of timestamps**

## 🚀 Quick Examples Gallery

```python
import arrow

# Current time
arrow.utcnow()                          # UTC now
arrow.now('America/New_York')           # Local now

# Parsing
arrow.get('2024-02-07')                 # From string
arrow.get(1707318645)                   # From timestamp

# Formatting
dt.format('YYYY-MM-DD')                 # Custom format
dt.isoformat()                          # ISO 8601
dt.humanize()                           # "2 hours ago"

# Manipulation
dt.shift(hours=5)                       # Add 5 hours
dt.shift(days=-3)                       # Subtract 3 days
dt.replace(hour=0)                      # Set hour to 0

# Timezone
dt.to('Asia/Tokyo')                     # Convert timezone
dt.to('UTC')                            # To UTC

# Ranges
arrow.Arrow.range('day', start, end)    # Date range

# Properties
dt.year, dt.month, dt.day               # Date parts
dt.timestamp()                          # Unix timestamp
dt.weekday()                            # Day of week
```

Start with `python examples/basic_examples.py` and explore from there!
