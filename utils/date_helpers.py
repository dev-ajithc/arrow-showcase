"""
Date manipulation utility functions.

Common operations for working with dates using Arrow.
"""

from typing import List, Optional

import arrow


def get_date_range(
    start: arrow.Arrow,
    end: arrow.Arrow,
    step: str = 'day'
) -> List[arrow.Arrow]:
    """
    Generate list of dates between start and end.

    Args:
        start: Starting date
        end: Ending date
        step: Step interval ('day', 'week', 'month', 'year')

    Returns:
        List of Arrow date objects

    Example:
        >>> start = arrow.get('2024-01-01')
        >>> end = arrow.get('2024-01-05')
        >>> dates = get_date_range(start, end)
        >>> len(dates)
        5
    """
    dates = []
    current = start

    while current <= end:
        dates.append(current)
        if step == 'day':
            current = current.shift(days=1)
        elif step == 'week':
            current = current.shift(weeks=1)
        elif step == 'month':
            current = current.shift(months=1)
        elif step == 'year':
            current = current.shift(years=1)
        else:
            raise ValueError(f"Invalid step: {step}")

    return dates


def is_business_day(date: arrow.Arrow) -> bool:
    """
    Check if date is a business day (Monday-Friday).

    Args:
        date: Arrow date object to check

    Returns:
        True if business day, False otherwise

    Example:
        >>> dt = arrow.get('2024-02-07')
        >>> is_business_day(dt)
        True
    """
    return date.weekday() < 5


def next_business_day(date: arrow.Arrow) -> arrow.Arrow:
    """
    Get next business day from given date.

    Args:
        date: Starting date

    Returns:
        Next business day

    Example:
        >>> dt = arrow.get('2024-02-09')
        >>> next_day = next_business_day(dt)
        >>> next_day.format('YYYY-MM-DD')
        '2024-02-12'
    """
    next_day = date.shift(days=1)

    while not is_business_day(next_day):
        next_day = next_day.shift(days=1)

    return next_day


def get_quarter_dates(year: int, quarter: int) -> tuple:
    """
    Get start and end dates for a quarter.

    Args:
        year: Year (e.g., 2024)
        quarter: Quarter number (1-4)

    Returns:
        Tuple of (start_date, end_date)

    Raises:
        ValueError: If quarter not in 1-4

    Example:
        >>> start, end = get_quarter_dates(2024, 1)
        >>> start.format('YYYY-MM-DD')
        '2024-01-01'
    """
    if quarter not in [1, 2, 3, 4]:
        raise ValueError("Quarter must be 1, 2, 3, or 4")

    start_month = (quarter - 1) * 3 + 1
    end_month = start_month + 2

    start_date = arrow.get(year, start_month, 1)
    end_date = arrow.get(year, end_month, 1).ceil('month')

    return start_date, end_date


def get_month_dates(year: int, month: int) -> tuple:
    """
    Get start and end dates for a month.

    Args:
        year: Year (e.g., 2024)
        month: Month number (1-12)

    Returns:
        Tuple of (start_date, end_date)

    Example:
        >>> start, end = get_month_dates(2024, 2)
        >>> start.format('YYYY-MM-DD')
        '2024-02-01'
    """
    start_date = arrow.get(year, month, 1)
    end_date = start_date.ceil('month')

    return start_date, end_date


def days_until(target_date: arrow.Arrow) -> int:
    """
    Calculate days until target date.

    Args:
        target_date: Target date

    Returns:
        Number of days until target (negative if in past)

    Example:
        >>> future = arrow.utcnow().shift(days=5)
        >>> days_until(future)
        5
    """
    now = arrow.utcnow().floor('day')
    target = target_date.floor('day')

    delta = target - now
    return delta.days


def age_from_birthdate(birthdate: arrow.Arrow) -> int:
    """
    Calculate age from birthdate.

    Args:
        birthdate: Birthdate as Arrow object

    Returns:
        Age in years

    Raises:
        ValueError: If birthdate is in the future

    Example:
        >>> bd = arrow.get('1990-01-01')
        >>> age = age_from_birthdate(bd)
        >>> age >= 34
        True
    """
    now = arrow.utcnow()

    if birthdate > now:
        raise ValueError("Birthdate cannot be in the future")

    age = now.year - birthdate.year

    if (now.month, now.day) < (birthdate.month, birthdate.day):
        age -= 1

    return age
