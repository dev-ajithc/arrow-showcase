"""
Tests for timestamp tool functions.
"""

import pytest
from freezegun import freeze_time

import arrow
from utils.timestamp_tools import (
    datetime_to_timestamp,
    generate_timestamp,
    generate_timestamped_filename,
    generate_unique_id,
    parse_timestamp_filename,
    timestamp_to_datetime,
)


class TestGenerateTimestamp:
    @freeze_time("2024-02-07 14:30:45")
    def test_unix_timestamp(self):
        result = generate_timestamp('unix')

        assert result.isdigit()
        assert int(result) > 0

    @freeze_time("2024-02-07 14:30:45")
    def test_iso_timestamp(self):
        result = generate_timestamp('iso')

        assert 'T' in result
        assert '2024' in result

    @freeze_time("2024-02-07 14:30:45")
    def test_filename_timestamp(self):
        result = generate_timestamp('filename')

        assert result == '20240207_143045'

    @freeze_time("2024-02-07 14:30:45")
    def test_human_timestamp(self):
        result = generate_timestamp('human')

        assert result == '2024-02-07 14:30:45'

    def test_invalid_format_raises_error(self):
        with pytest.raises(ValueError, match="Invalid format_type"):
            generate_timestamp('invalid')


class TestTimestampToDatetime:
    def test_seconds_timestamp(self):
        ts = 1707318645
        dt = timestamp_to_datetime(ts, 'seconds')

        assert dt.year == 2024
        assert isinstance(dt, arrow.Arrow)

    def test_milliseconds_timestamp(self):
        ts = 1707318645000
        dt = timestamp_to_datetime(ts, 'milliseconds')

        assert dt.year == 2024


class TestDatetimeToTimestamp:
    def test_to_seconds(self):
        dt = arrow.get('2024-02-07 14:30:45')
        ts = datetime_to_timestamp(dt, 'seconds')

        assert isinstance(ts, int)
        assert ts > 0

    def test_to_milliseconds(self):
        dt = arrow.get('2024-02-07 14:30:45')
        ts = datetime_to_timestamp(dt, 'milliseconds')

        assert isinstance(ts, int)
        assert ts > datetime_to_timestamp(dt, 'seconds')


class TestGenerateUniqueId:
    def test_returns_string(self):
        id1 = generate_unique_id()

        assert isinstance(id1, str)
        assert len(id1) > 0

    def test_unique_ids(self):
        id1 = generate_unique_id()
        id2 = generate_unique_id()

        assert id1 != id2


class TestParseTimestampFilename:
    def test_parse_valid_filename(self):
        filename = 'backup_20240207_143045.zip'
        dt = parse_timestamp_filename(filename)

        assert dt is not None
        assert dt.format('YYYY-MM-DD') == '2024-02-07'
        assert dt.hour == 14

    def test_parse_filename_without_extension(self):
        filename = 'log_20240207_143045'
        dt = parse_timestamp_filename(filename)

        assert dt is not None
        assert dt.format('YYYY-MM-DD') == '2024-02-07'

    def test_parse_invalid_filename(self):
        filename = 'backup_invalid.zip'
        dt = parse_timestamp_filename(filename)

        assert dt is None

    def test_parse_filename_with_multiple_timestamps(self):
        filename = 'backup_20240101_120000_20240207_143045.zip'
        dt = parse_timestamp_filename(filename)

        assert dt is not None


class TestGenerateTimestampedFilename:
    @freeze_time("2024-02-07 14:30:45")
    def test_with_extension(self):
        result = generate_timestamped_filename('backup', '.zip')

        assert result == 'backup_20240207_143045.zip'

    @freeze_time("2024-02-07 14:30:45")
    def test_without_dot_in_extension(self):
        result = generate_timestamped_filename('backup', 'zip')

        assert result == 'backup_20240207_143045.zip'

    @freeze_time("2024-02-07 14:30:45")
    def test_without_extension(self):
        result = generate_timestamped_filename('backup', '')

        assert result == 'backup_20240207_143045'

    @freeze_time("2024-02-07 14:30:45")
    def test_custom_format(self):
        result = generate_timestamped_filename(
            'report', '.pdf', 'YYYY-MM-DD'
        )

        assert result == 'report_2024-02-07.pdf'
