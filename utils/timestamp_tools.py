"""
Timestamp generation and manipulation utilities.

Functions for working with timestamps and timestamped files.
"""

import re
from typing import Optional

import arrow


def generate_timestamp(format_type: str = 'unix') -> str:
    """
    Generate various timestamp formats.

    Args:
        format_type: Type ('unix', 'iso', 'filename', 'human')

    Returns:
        Formatted timestamp string

    Raises:
        ValueError: If format_type is invalid

    Example:
        >>> ts = generate_timestamp('unix')
        >>> isinstance(int(ts), int)
        True
    """
    now = arrow.utcnow()

    if format_type == 'unix':
        return str(int(now.timestamp()))
    elif format_type == 'iso':
        return now.isoformat()
    elif format_type == 'filename':
        return now.format('YYYYMMDD_HHmmss')
    elif format_type == 'human':
        return now.format('YYYY-MM-DD HH:mm:ss')
    else:
        raise ValueError(f"Invalid format_type: {format_type}")


def timestamp_to_datetime(
    ts: int,
    unit: str = 'seconds'
) -> arrow.Arrow:
    """
    Convert timestamp to Arrow datetime.

    Args:
        ts: Timestamp value
        unit: Unit ('seconds' or 'milliseconds')

    Returns:
        Arrow datetime object

    Example:
        >>> dt = timestamp_to_datetime(1707292800)
        >>> dt.year
        2024
    """
    if unit == 'milliseconds':
        ts = ts / 1000

    return arrow.get(ts)


def datetime_to_timestamp(
    dt: arrow.Arrow,
    unit: str = 'seconds'
) -> int:
    """
    Convert Arrow datetime to timestamp.

    Args:
        dt: Arrow datetime object
        unit: Unit ('seconds' or 'milliseconds')

    Returns:
        Timestamp as integer

    Example:
        >>> dt = arrow.get('2024-02-07')
        >>> ts = datetime_to_timestamp(dt)
        >>> ts > 0
        True
    """
    ts = int(dt.timestamp())

    if unit == 'milliseconds':
        ts = ts * 1000

    return ts


def generate_unique_id() -> str:
    """
    Generate unique timestamp-based ID.

    Returns:
        Unique ID string

    Example:
        >>> id1 = generate_unique_id()
        >>> id2 = generate_unique_id()
        >>> id1 != id2
        True
    """
    now = arrow.utcnow()
    return f"{now.timestamp():.6f}".replace('.', '')


def parse_timestamp_filename(filename: str) -> Optional[arrow.Arrow]:
    """
    Extract timestamp from filename.

    Args:
        filename: Filename containing timestamp

    Returns:
        Arrow datetime or None if no timestamp found

    Example:
        >>> dt = parse_timestamp_filename('backup_20240207_143045.zip')
        >>> dt.format('YYYY-MM-DD')
        '2024-02-07'
    """
    pattern = r'(\d{8})_(\d{6})'
    match = re.search(pattern, filename)

    if match:
        date_str = match.group(1)
        time_str = match.group(2)
        combined = f"{date_str}_{time_str}"

        try:
            return arrow.get(combined, 'YYYYMMDD_HHmmss')
        except Exception:
            return None

    return None


def generate_timestamped_filename(
    base_name: str,
    extension: str = '',
    format_str: str = 'YYYYMMDD_HHmmss'
) -> str:
    """
    Generate filename with timestamp.

    Args:
        base_name: Base name for the file
        extension: File extension (with or without dot)
        format_str: Arrow format string for timestamp

    Returns:
        Timestamped filename

    Example:
        >>> fn = generate_timestamped_filename('backup', '.zip')
        >>> '.zip' in fn
        True
    """
    now = arrow.utcnow()
    timestamp = now.format(format_str)

    if extension and not extension.startswith('.'):
        extension = f".{extension}"

    return f"{base_name}_{timestamp}{extension}"
