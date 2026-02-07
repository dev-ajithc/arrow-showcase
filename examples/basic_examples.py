"""
Basic Arrow examples demonstrating fundamental operations.

Run this script to see Arrow basics in action.
"""

import time

import arrow


def demo_current_time() -> None:
    """Get current time in various formats."""
    print("\n=== Current Time Demo ===")

    utc_now = arrow.utcnow()
    print(f"UTC Now: {utc_now}")

    local_now = arrow.now()
    print(f"Local Now: {local_now}")

    formatted = utc_now.format('YYYY-MM-DD HH:mm:ss')
    print(f"Formatted: {formatted}")


def demo_time_shifting() -> None:
    """Add/subtract time units (hours, days, weeks)."""
    print("\n=== Time Shifting Demo ===")

    now = arrow.utcnow()
    print(f"Now: {now.format('YYYY-MM-DD HH:mm:ss')}")

    future = now.shift(hours=5)
    print(f"5 hours later: {future.format('YYYY-MM-DD HH:mm:ss')}")

    past = now.shift(days=-3)
    print(f"3 days ago: {past.format('YYYY-MM-DD HH:mm:ss')}")

    next_week = now.shift(weeks=1)
    print(f"Next week: {next_week.format('YYYY-MM-DD HH:mm:ss')}")

    next_month = now.shift(months=1)
    print(f"Next month: {next_month.format('YYYY-MM-DD HH:mm:ss')}")


def demo_time_ranges() -> None:
    """Create and iterate over time ranges."""
    print("\n=== Time Ranges Demo ===")

    start = arrow.get('2024-02-01')
    end = arrow.get('2024-02-05')

    print("Date range from Feb 1 to Feb 5, 2024:")
    for date in arrow.Arrow.range('day', start, end):
        print(f"  {date.format('YYYY-MM-DD')}")


def demo_relative_time() -> None:
    """Calculate time differences and relative times."""
    print("\n=== Relative Time Demo ===")

    now = arrow.utcnow()

    past = now.shift(hours=-2)
    print(f"2 hours ago: {past.humanize()}")

    future = now.shift(days=3)
    print(f"3 days from now: {future.humanize()}")

    yesterday = now.shift(days=-1)
    print(f"Yesterday: {yesterday.humanize()}")


def demo_time_comparison() -> None:
    """Compare dates and times."""
    print("\n=== Time Comparison Demo ===")

    date1 = arrow.get('2024-02-07')
    date2 = arrow.get('2024-02-10')

    print(f"Date 1: {date1.format('YYYY-MM-DD')}")
    print(f"Date 2: {date2.format('YYYY-MM-DD')}")
    print(f"Date 1 < Date 2: {date1 < date2}")
    print(f"Date 1 == Date 2: {date1 == date2}")

    diff = date2 - date1
    print(f"Difference: {diff.days} days")


def demo_time_properties() -> None:
    """Access date/time components."""
    print("\n=== Time Properties Demo ===")

    dt = arrow.get('2024-02-07 14:30:45')

    print(f"Full datetime: {dt}")
    print(f"Year: {dt.year}")
    print(f"Month: {dt.month}")
    print(f"Day: {dt.day}")
    print(f"Hour: {dt.hour}")
    print(f"Minute: {dt.minute}")
    print(f"Second: {dt.second}")
    print(f"Weekday: {dt.format('dddd')}")
    print(f"Week of year: {dt.week}")


def main() -> None:
    """Run all basic examples."""
    print("=" * 60)
    print("Arrow Basic Examples")
    print("=" * 60)

    demo_current_time()
    time.sleep(0.5)

    demo_time_shifting()
    time.sleep(0.5)

    demo_time_ranges()
    time.sleep(0.5)

    demo_relative_time()
    time.sleep(0.5)

    demo_time_comparison()
    time.sleep(0.5)

    demo_time_properties()

    print("\n" + "=" * 60)
    print("All basic examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
