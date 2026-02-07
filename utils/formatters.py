"""
Date formatting utilities.

Custom formatters for various use cases.
"""

from typing import Optional

import arrow


def format_for_filename(dt: Optional[arrow.Arrow] = None) -> str:
    """
    Format date for safe filename usage.

    Args:
        dt: Arrow datetime (uses current time if None)

    Returns:
        Formatted string safe for filenames

    Example:
        >>> dt = arrow.get('2024-02-07 14:30:45')
        >>> format_for_filename(dt)
        '20240207_143045'
    """
    if dt is None:
        dt = arrow.utcnow()

    return dt.format('YYYYMMDD_HHmmss')


def format_for_display(
    dt: arrow.Arrow,
    locale: str = 'en'
) -> str:
    """
    Format date for human-readable display.

    Args:
        dt: Arrow datetime object
        locale: Locale for formatting

    Returns:
        Human-readable date string

    Example:
        >>> dt = arrow.get('2024-02-07 14:30:45')
        >>> format_for_display(dt)
        'February 07, 2024 at 2:30 PM'
    """
    return dt.format('MMMM DD, YYYY [at] h:mm A', locale=locale)


def format_for_api(dt: arrow.Arrow) -> str:
    """
    Format date for API communication (ISO 8601).

    Args:
        dt: Arrow datetime object

    Returns:
        ISO 8601 formatted string

    Example:
        >>> dt = arrow.get('2024-02-07 14:30:45', 'UTC')
        >>> format_for_api(dt)
        '2024-02-07T14:30:45+00:00'
    """
    return dt.isoformat()


def format_relative(dt: arrow.Arrow) -> str:
    """
    Format as relative time ('2 hours ago').

    Args:
        dt: Arrow datetime object

    Returns:
        Humanized relative time string

    Example:
        >>> past = arrow.utcnow().shift(hours=-2)
        >>> 'ago' in format_relative(past)
        True
    """
    return dt.humanize()


def format_for_log(dt: arrow.Arrow) -> str:
    """
    Format date for log file entries.

    Args:
        dt: Arrow datetime object

    Returns:
        Log-friendly formatted string

    Example:
        >>> dt = arrow.get('2024-02-07 14:30:45')
        >>> format_for_log(dt)
        '2024-02-07 14:30:45'
    """
    return dt.format('YYYY-MM-DD HH:mm:ss')


class DateFormatter:
    """
    Custom date formatter with templates.

    Example:
        >>> formatter = DateFormatter()
        >>> dt = arrow.get('2024-02-07 14:30:45')
        >>> formatter.format(dt, 'short')
        '2024-02-07'
    """

    def __init__(self) -> None:
        """Initialize formatter with predefined templates."""
        self.templates = {
            'short': 'YYYY-MM-DD',
            'long': 'MMMM DD, YYYY',
            'time': 'HH:mm:ss',
            'datetime': 'YYYY-MM-DD HH:mm:ss',
            'iso': 'YYYY-MM-DDTHH:mm:ssZZ',
            'filename': 'YYYYMMDD_HHmmss',
            'log': 'YYYY-MM-DD HH:mm:ss',
            'display': 'MMMM DD, YYYY [at] h:mm A',
        }

    def format(
        self,
        dt: arrow.Arrow,
        template: str = 'datetime'
    ) -> str:
        """
        Format datetime using template.

        Args:
            dt: Arrow datetime object
            template: Template name

        Returns:
            Formatted string

        Raises:
            ValueError: If template not found
        """
        if template not in self.templates:
            raise ValueError(f"Unknown template: {template}")

        return dt.format(self.templates[template])

    def add_template(self, name: str, format_string: str) -> None:
        """
        Add custom template.

        Args:
            name: Template name
            format_string: Arrow format string
        """
        self.templates[name] = format_string

    def list_templates(self) -> list:
        """
        List available templates.

        Returns:
            List of template names
        """
        return list(self.templates.keys())
