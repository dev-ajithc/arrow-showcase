"""
Timezone operations and conversions with Arrow.

Demonstrates timezone handling, conversions, and world clock.
"""

import time

import arrow


def demo_utc_local_conversion() -> None:
    """Convert between UTC and local time."""
    print("\n=== UTC/Local Conversion Demo ===")

    utc = arrow.utcnow()
    print(f"UTC: {utc.format('YYYY-MM-DD HH:mm:ss ZZ')}")

    local = utc.to('local')
    print(f"Local: {local.format('YYYY-MM-DD HH:mm:ss ZZ')}")

    back_to_utc = local.to('UTC')
    print(f"Back to UTC: {back_to_utc.format('YYYY-MM-DD HH:mm:ss ZZ')}")


def demo_timezone_conversion() -> None:
    """Convert between different timezones."""
    print("\n=== Timezone Conversion Demo ===")

    utc = arrow.utcnow()
    print(f"UTC: {utc.format('YYYY-MM-DD HH:mm:ss')}")

    ny = utc.to('America/New_York')
    print(f"New York: {ny.format('YYYY-MM-DD HH:mm:ss ZZ')}")

    london = utc.to('Europe/London')
    print(f"London: {london.format('YYYY-MM-DD HH:mm:ss ZZ')}")

    tokyo = utc.to('Asia/Tokyo')
    print(f"Tokyo: {tokyo.format('YYYY-MM-DD HH:mm:ss ZZ')}")

    sydney = utc.to('Australia/Sydney')
    print(f"Sydney: {sydney.format('YYYY-MM-DD HH:mm:ss ZZ')}")


def demo_timezone_aware_operations() -> None:
    """Perform calculations across timezones."""
    print("\n=== Timezone-Aware Operations Demo ===")

    ny_time = arrow.now('America/New_York')
    print(f"New York: {ny_time.format('YYYY-MM-DD HH:mm:ss ZZ')}")

    shifted = ny_time.shift(hours=3)
    print(f"3 hours later: {shifted.format('YYYY-MM-DD HH:mm:ss ZZ')}")

    tokyo_same_moment = ny_time.to('Asia/Tokyo')
    print(f"Same moment in Tokyo: "
          f"{tokyo_same_moment.format('YYYY-MM-DD HH:mm:ss ZZ')}")


def demo_world_clock() -> None:
    """Display time in multiple timezones."""
    print("\n=== World Clock Demo ===")

    utc = arrow.utcnow()
    print(f"Current time: {utc.format('YYYY-MM-DD HH:mm:ss')} UTC\n")

    timezones = [
        ('UTC', 'UTC'),
        ('New York', 'America/New_York'),
        ('Los Angeles', 'America/Los_Angeles'),
        ('London', 'Europe/London'),
        ('Paris', 'Europe/Paris'),
        ('Dubai', 'Asia/Dubai'),
        ('Mumbai', 'Asia/Kolkata'),
        ('Singapore', 'Asia/Singapore'),
        ('Tokyo', 'Asia/Tokyo'),
        ('Sydney', 'Australia/Sydney'),
    ]

    print("World Clock:")
    for city, tz in timezones:
        local_time = utc.to(tz)
        print(f"  {city:15} {local_time.format('HH:mm:ss')} "
              f"({local_time.format('ZZ')})")


def demo_dst_handling() -> None:
    """Handle daylight saving time transitions."""
    print("\n=== DST Handling Demo ===")

    winter = arrow.get('2024-01-15 12:00:00', tzinfo='America/New_York')
    summer = arrow.get('2024-07-15 12:00:00', tzinfo='America/New_York')

    print(f"Winter (EST): {winter.format('YYYY-MM-DD HH:mm:ss ZZ')}")
    print(f"DST active: {winter.dst().total_seconds() != 0}")

    print(f"\nSummer (EDT): {summer.format('YYYY-MM-DD HH:mm:ss ZZ')}")
    print(f"DST active: {summer.dst().total_seconds() != 0}")


def demo_timezone_info() -> None:
    """Display timezone information."""
    print("\n=== Timezone Info Demo ===")

    timezones = [
        'America/New_York',
        'Europe/London',
        'Asia/Tokyo',
    ]

    for tz_name in timezones:
        dt = arrow.now(tz_name)
        print(f"\n{tz_name}:")
        print(f"  Current time: {dt.format('YYYY-MM-DD HH:mm:ss')}")
        print(f"  UTC offset: {dt.format('ZZ')}")
        print(f"  Timezone abbr: {dt.tzinfo.tzname(None)}")
        print(f"  DST active: {dt.dst().total_seconds() != 0}")


def main() -> None:
    """Run all timezone examples."""
    print("=" * 60)
    print("Arrow Timezone Operations Examples")
    print("=" * 60)

    demo_utc_local_conversion()
    time.sleep(0.5)

    demo_timezone_conversion()
    time.sleep(0.5)

    demo_timezone_aware_operations()
    time.sleep(0.5)

    demo_world_clock()
    time.sleep(0.5)

    demo_dst_handling()
    time.sleep(0.5)

    demo_timezone_info()

    print("\n" + "=" * 60)
    print("All timezone examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
