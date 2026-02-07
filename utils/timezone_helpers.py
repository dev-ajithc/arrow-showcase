"""
Timezone conversion and manipulation utilities.

Helper functions for working with timezones using Arrow.
"""

from typing import Dict, List, Optional

import arrow


def convert_timezone(
    dt: arrow.Arrow,
    from_tz: str,
    to_tz: str
) -> arrow.Arrow:
    """
    Convert datetime between timezones.

    Args:
        dt: Arrow datetime object
        from_tz: Source timezone (e.g., 'UTC')
        to_tz: Target timezone (e.g., 'America/New_York')

    Returns:
        Converted Arrow datetime

    Example:
        >>> utc = arrow.utcnow()
        >>> ny = convert_timezone(utc, 'UTC', 'America/New_York')
        >>> ny.tzinfo.tzname(None)
        'EST'
    """
    if dt.tzinfo is None or str(dt.tzinfo) != from_tz:
        dt = dt.replace(tzinfo=from_tz)

    return dt.to(to_tz)


def get_local_timezone() -> str:
    """
    Get system's local timezone.

    Returns:
        Timezone name as string

    Example:
        >>> tz = get_local_timezone()
        >>> isinstance(tz, str)
        True
    """
    local = arrow.now()
    return str(local.tzinfo)


def get_timezone_offset(tz: str) -> str:
    """
    Get UTC offset for timezone.

    Args:
        tz: Timezone name

    Returns:
        UTC offset as string (e.g., '+05:30')

    Example:
        >>> offset = get_timezone_offset('America/New_York')
        >>> offset in ['-05:00', '-04:00']
        True
    """
    dt = arrow.now(tz)
    return dt.format('ZZ')


def is_dst(dt: arrow.Arrow, tz: Optional[str] = None) -> bool:
    """
    Check if DST is active for date/timezone.

    Args:
        dt: Arrow datetime object
        tz: Timezone (uses dt's timezone if not provided)

    Returns:
        True if DST is active, False otherwise

    Example:
        >>> dt = arrow.get('2024-07-01', tzinfo='America/New_York')
        >>> is_dst(dt)
        True
    """
    if tz:
        dt = dt.to(tz)

    return dt.dst().total_seconds() != 0


def get_world_times(
    dt: arrow.Arrow,
    timezones: List[str]
) -> Dict[str, str]:
    """
    Get time in multiple timezones.

    Args:
        dt: Arrow datetime object
        timezones: List of timezone names

    Returns:
        Dictionary mapping timezone to formatted time

    Example:
        >>> utc = arrow.utcnow()
        >>> tzs = ['UTC', 'America/New_York', 'Europe/London']
        >>> times = get_world_times(utc, tzs)
        >>> len(times)
        3
    """
    world_times = {}

    for tz in timezones:
        try:
            converted = dt.to(tz)
            world_times[tz] = converted.format('YYYY-MM-DD HH:mm:ss ZZ')
        except Exception as e:
            world_times[tz] = f"Error: {str(e)}"

    return world_times
