"""
Date formatting and parsing examples with Arrow.

Demonstrates various ways to format and parse dates.
"""

import time

import arrow


def demo_format_conversions() -> None:
    """Convert between different date formats."""
    print("\n=== Format Conversions Demo ===")

    dt = arrow.get('2024-02-07 14:30:45')

    print("Various date formats:")
    print(f"  ISO 8601: {dt.format('YYYY-MM-DD')}")
    print(f"  US Format: {dt.format('MM/DD/YYYY')}")
    print(f"  EU Format: {dt.format('DD/MM/YYYY')}")
    print(f"  Full: {dt.format('MMMM DD, YYYY')}")
    print(f"  With Time: {dt.format('YYYY-MM-DD HH:mm:ss')}")
    print(f"  12-hour: {dt.format('YYYY-MM-DD hh:mm:ss A')}")


def demo_iso8601_formatting() -> None:
    """Work with ISO 8601 standard."""
    print("\n=== ISO 8601 Formatting Demo ===")

    dt = arrow.utcnow()

    print("ISO 8601 formats:")
    print(f"  Basic: {dt.format('YYYY-MM-DD')}")
    print(f"  With time: {dt.format('YYYY-MM-DDTHH:mm:ss')}")
    print(f"  Full: {dt.isoformat()}")
    print(f"  Custom: {dt.format('YYYY-MM-DDTHH:mm:ssZZ')}")


def demo_custom_formats() -> None:
    """Create custom format strings."""
    print("\n=== Custom Formats Demo ===")

    dt = arrow.get('2024-02-07 14:30:45')

    print("Custom formats:")
    print(f"  Log format: {dt.format('YYYY-MM-DD HH:mm:ss')}")
    print(f"  Filename: {dt.format('YYYYMMDD_HHmmss')}")
    print(f"  Display: {dt.format('MMM DD, YYYY [at] h:mm A')}")
    print(f"  Short: {dt.format('YY/MM/DD')}")
    print(f"  Long: {dt.format('dddd, MMMM DD, YYYY')}")


def demo_locale_formatting() -> None:
    """Format dates in different locales."""
    print("\n=== Locale Formatting Demo ===")

    dt = arrow.get('2024-02-07 14:30:45')

    try:
        print("Date in different locales:")
        print(f"  English: {dt.format('MMMM DD, YYYY', locale='en')}")
        print(f"  Day: {dt.format('dddd', locale='en')}")
    except Exception as e:
        print(f"  Locale formatting: {e}")


def demo_parsing_strings() -> None:
    """Parse date strings with various formats."""
    print("\n=== String Parsing Demo ===")

    print("Parsing different date formats:")

    dt1 = arrow.get('2024-02-07', 'YYYY-MM-DD')
    print(f"  ISO: '2024-02-07' -> {dt1}")

    dt2 = arrow.get('02/07/2024', 'MM/DD/YYYY')
    print(f"  US: '02/07/2024' -> {dt2}")

    dt3 = arrow.get('07-02-2024', 'DD-MM-YYYY')
    print(f"  EU: '07-02-2024' -> {dt3}")

    dt4 = arrow.get('2024-02-07 14:30:45', 'YYYY-MM-DD HH:mm:ss')
    print(f"  Datetime: '2024-02-07 14:30:45' -> {dt4}")

    dt5 = arrow.get('20240207_143045', 'YYYYMMDD_HHmmss')
    print(f"  Filename: '20240207_143045' -> {dt5}")


def demo_timestamp_conversion() -> None:
    """Convert to/from Unix timestamps."""
    print("\n=== Timestamp Conversion Demo ===")

    dt = arrow.get('2024-02-07 14:30:45')

    timestamp = dt.timestamp()
    print(f"Datetime: {dt}")
    print(f"Unix timestamp: {timestamp}")

    dt_from_ts = arrow.get(timestamp)
    print(f"Back to datetime: {dt_from_ts}")

    print(f"\nMilliseconds: {int(timestamp * 1000)}")


def demo_natural_dates() -> None:
    """Parse natural language dates."""
    print("\n=== Natural Date Parsing Demo ===")

    print("Common date shortcuts:")
    print(f"  Today: {arrow.now().format('YYYY-MM-DD')}")
    print(f"  Yesterday: {arrow.now().shift(days=-1).format('YYYY-MM-DD')}")
    print(f"  Tomorrow: {arrow.now().shift(days=1).format('YYYY-MM-DD')}")

    print("\nRelative dates:")
    print(f"  Last week: {arrow.now().shift(weeks=-1).format('YYYY-MM-DD')}")
    print(f"  Next month: {arrow.now().shift(months=1).format('YYYY-MM-DD')}")


def main() -> None:
    """Run all formatting and parsing examples."""
    print("=" * 60)
    print("Arrow Formatting & Parsing Examples")
    print("=" * 60)

    demo_format_conversions()
    time.sleep(0.5)

    demo_iso8601_formatting()
    time.sleep(0.5)

    demo_custom_formats()
    time.sleep(0.5)

    demo_locale_formatting()
    time.sleep(0.5)

    demo_parsing_strings()
    time.sleep(0.5)

    demo_timestamp_conversion()
    time.sleep(0.5)

    demo_natural_dates()

    print("\n" + "=" * 60)
    print("All formatting & parsing examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
