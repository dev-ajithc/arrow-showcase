"""
Advanced Arrow features and use cases.

Demonstrates advanced operations like ranges, business days, humanization.
"""

import time

import arrow


def demo_date_ranges() -> None:
    """Generate date ranges with various spans."""
    print("\n=== Date Ranges Demo ===")

    start = arrow.get('2024-02-01')
    end = arrow.get('2024-02-10')

    print("Daily range:")
    for date in arrow.Arrow.range('day', start, end):
        print(f"  {date.format('YYYY-MM-DD dddd')}")

    print("\nHourly range (first 24 hours):")
    for hour in list(arrow.Arrow.range('hour', start, start.shift(days=1)))[:5]:
        print(f"  {hour.format('YYYY-MM-DD HH:mm')}")
        print("  ...")
        break


def demo_business_days() -> None:
    """Calculate business days (skip weekends)."""
    print("\n=== Business Days Demo ===")

    start = arrow.get('2024-02-05')
    print(f"Starting from: {start.format('YYYY-MM-DD dddd')}")

    business_days = []
    current = start

    for _ in range(10):
        if current.weekday() < 5:
            business_days.append(current)
        current = current.shift(days=1)

    print("\nNext 10 business days:")
    for day in business_days:
        print(f"  {day.format('YYYY-MM-DD dddd')}")


def demo_humanized_dates() -> None:
    """Convert dates to human-readable format."""
    print("\n=== Humanized Dates Demo ===")

    now = arrow.utcnow()

    times = [
        now.shift(seconds=-30),
        now.shift(minutes=-5),
        now.shift(hours=-2),
        now.shift(days=-1),
        now.shift(weeks=-2),
        now.shift(months=-3),
        now.shift(years=-1),
    ]

    print("Past times (humanized):")
    for t in times:
        print(f"  {t.format('YYYY-MM-DD HH:mm:ss')} -> {t.humanize()}")

    future_times = [
        now.shift(hours=1),
        now.shift(days=2),
        now.shift(weeks=1),
        now.shift(months=1),
    ]

    print("\nFuture times (humanized):")
    for t in future_times:
        print(f"  {t.format('YYYY-MM-DD HH:mm:ss')} -> {t.humanize()}")


def demo_time_series() -> None:
    """Generate time series data."""
    print("\n=== Time Series Demo ===")

    start = arrow.get('2024-02-01 00:00:00')

    print("Hourly time series (first 10 points):")
    for i, timestamp in enumerate(
        arrow.Arrow.range('hour', start, start.shift(days=1))
    ):
        if i < 10:
            print(f"  Point {i}: {timestamp.format('YYYY-MM-DD HH:mm:ss')}")
        elif i == 10:
            print(f"  ... ({24 - 10} more points)")
            break


def demo_calendar_operations() -> None:
    """Perform calendar-based calculations."""
    print("\n=== Calendar Operations Demo ===")

    dt = arrow.get('2024-02-15 14:30:45')

    print(f"Original: {dt.format('YYYY-MM-DD HH:mm:ss')}")

    floor_day = dt.floor('day')
    print(f"Floor to day: {floor_day.format('YYYY-MM-DD HH:mm:ss')}")

    ceil_day = dt.ceil('day')
    print(f"Ceil to day: {ceil_day.format('YYYY-MM-DD HH:mm:ss')}")

    floor_month = dt.floor('month')
    print(f"Floor to month: {floor_month.format('YYYY-MM-DD HH:mm:ss')}")

    ceil_month = dt.ceil('month')
    print(f"Ceil to month: {ceil_month.format('YYYY-MM-DD HH:mm:ss')}")


def demo_span_operations() -> None:
    """Work with time spans."""
    print("\n=== Span Operations Demo ===")

    dt = arrow.get('2024-02-15 14:30:45')

    print(f"Date: {dt.format('YYYY-MM-DD HH:mm:ss')}")

    day_span = dt.span('day')
    print(f"\nDay span:")
    print(f"  Start: {day_span[0].format('YYYY-MM-DD HH:mm:ss')}")
    print(f"  End: {day_span[1].format('YYYY-MM-DD HH:mm:ss')}")

    week_span = dt.span('week')
    print(f"\nWeek span:")
    print(f"  Start: {week_span[0].format('YYYY-MM-DD HH:mm:ss')}")
    print(f"  End: {week_span[1].format('YYYY-MM-DD HH:mm:ss')}")

    month_span = dt.span('month')
    print(f"\nMonth span:")
    print(f"  Start: {month_span[0].format('YYYY-MM-DD HH:mm:ss')}")
    print(f"  End: {month_span[1].format('YYYY-MM-DD HH:mm:ss')}")


def demo_replace_operations() -> None:
    """Replace specific date/time components."""
    print("\n=== Replace Operations Demo ===")

    dt = arrow.get('2024-02-15 14:30:45')

    print(f"Original: {dt.format('YYYY-MM-DD HH:mm:ss')}")

    new_year = dt.replace(year=2025)
    print(f"New year: {new_year.format('YYYY-MM-DD HH:mm:ss')}")

    new_month = dt.replace(month=12)
    print(f"New month: {new_month.format('YYYY-MM-DD HH:mm:ss')}")

    new_time = dt.replace(hour=0, minute=0, second=0)
    print(f"Midnight: {new_time.format('YYYY-MM-DD HH:mm:ss')}")


def demo_for_json() -> None:
    """Prepare dates for JSON serialization."""
    print("\n=== JSON Serialization Demo ===")

    dt = arrow.utcnow()

    print("Formats suitable for JSON:")
    print(f"  ISO 8601: {dt.isoformat()}")
    print(f"  Unix timestamp: {dt.timestamp()}")
    print(f"  Custom: {dt.format('YYYY-MM-DD HH:mm:ss')}")

    json_data = {
        'timestamp': dt.timestamp(),
        'iso': dt.isoformat(),
        'formatted': dt.format('YYYY-MM-DD HH:mm:ss'),
    }

    print(f"\nJSON object: {json_data}")


def main() -> None:
    """Run all advanced examples."""
    print("=" * 60)
    print("Arrow Advanced Examples")
    print("=" * 60)

    demo_date_ranges()
    time.sleep(0.5)

    demo_business_days()
    time.sleep(0.5)

    demo_humanized_dates()
    time.sleep(0.5)

    demo_time_series()
    time.sleep(0.5)

    demo_calendar_operations()
    time.sleep(0.5)

    demo_span_operations()
    time.sleep(0.5)

    demo_replace_operations()
    time.sleep(0.5)

    demo_for_json()

    print("\n" + "=" * 60)
    print("All advanced examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
