"""
Tests for formatter functions.
"""

import pytest
from freezegun import freeze_time

import arrow
from utils.formatters import (
    DateFormatter,
    format_for_api,
    format_for_display,
    format_for_filename,
    format_for_log,
    format_relative,
)


class TestFormatForFilename:
    @freeze_time("2024-02-07 14:30:45")
    def test_default_format(self):
        result = format_for_filename()

        assert result == '20240207_143045'

    def test_with_specific_date(self):
        dt = arrow.get('2024-12-31 23:59:59')
        result = format_for_filename(dt)

        assert result == '20241231_235959'


class TestFormatForDisplay:
    def test_default_locale(self):
        dt = arrow.get('2024-02-07 14:30:45')
        result = format_for_display(dt)

        assert 'February' in result
        assert '07' in result
        assert '2024' in result
        assert 'PM' in result


class TestFormatForAPI:
    def test_returns_iso8601(self):
        dt = arrow.get('2024-02-07 14:30:45', tzinfo='UTC')
        result = format_for_api(dt)

        assert 'T' in result
        assert '+00:00' in result or 'Z' in result


class TestFormatRelative:
    def test_past_time(self):
        past = arrow.utcnow().shift(hours=-2)
        result = format_relative(past)

        assert 'ago' in result

    def test_future_time(self):
        future = arrow.utcnow().shift(hours=2)
        result = format_relative(future)

        assert 'in' in result


class TestFormatForLog:
    def test_log_format(self):
        dt = arrow.get('2024-02-07 14:30:45')
        result = format_for_log(dt)

        assert result == '2024-02-07 14:30:45'


class TestDateFormatter:
    def test_initialization(self):
        formatter = DateFormatter()

        assert len(formatter.templates) > 0

    def test_format_short(self):
        formatter = DateFormatter()
        dt = arrow.get('2024-02-07 14:30:45')
        result = formatter.format(dt, 'short')

        assert result == '2024-02-07'

    def test_format_long(self):
        formatter = DateFormatter()
        dt = arrow.get('2024-02-07 14:30:45')
        result = formatter.format(dt, 'long')

        assert 'February' in result

    def test_format_datetime(self):
        formatter = DateFormatter()
        dt = arrow.get('2024-02-07 14:30:45')
        result = formatter.format(dt, 'datetime')

        assert result == '2024-02-07 14:30:45'

    def test_format_filename(self):
        formatter = DateFormatter()
        dt = arrow.get('2024-02-07 14:30:45')
        result = formatter.format(dt, 'filename')

        assert result == '20240207_143045'

    def test_invalid_template_raises_error(self):
        formatter = DateFormatter()
        dt = arrow.get('2024-02-07 14:30:45')

        with pytest.raises(ValueError, match="Unknown template"):
            formatter.format(dt, 'invalid')

    def test_add_template(self):
        formatter = DateFormatter()
        formatter.add_template('custom', 'YYYY/MM/DD')

        dt = arrow.get('2024-02-07')
        result = formatter.format(dt, 'custom')

        assert result == '2024/02/07'

    def test_list_templates(self):
        formatter = DateFormatter()
        templates = formatter.list_templates()

        assert isinstance(templates, list)
        assert 'short' in templates
        assert 'long' in templates
