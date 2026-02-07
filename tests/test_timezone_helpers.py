"""
Tests for timezone helper functions.
"""

import pytest

import arrow
from utils.timezone_helpers import (
    convert_timezone,
    get_local_timezone,
    get_timezone_offset,
    get_world_times,
    is_dst,
)


class TestConvertTimezone:
    def test_utc_to_new_york(self):
        utc = arrow.get('2024-02-07 12:00:00', tzinfo='UTC')
        ny = convert_timezone(utc, 'UTC', 'America/New_York')

        assert ny.hour in [7, 6]

    def test_new_york_to_london(self):
        ny = arrow.get('2024-02-07 12:00:00', tzinfo='America/New_York')
        london = convert_timezone(ny, 'America/New_York', 'Europe/London')

        assert london.hour in [17, 16, 18]

    def test_preserves_moment_in_time(self):
        utc = arrow.get('2024-02-07 12:00:00', tzinfo='UTC')
        tokyo = convert_timezone(utc, 'UTC', 'Asia/Tokyo')

        assert utc.timestamp() == tokyo.timestamp()


class TestGetLocalTimezone:
    def test_returns_string(self):
        tz = get_local_timezone()

        assert isinstance(tz, str)
        assert len(tz) > 0


class TestGetTimezoneOffset:
    def test_utc_offset_is_zero(self):
        offset = get_timezone_offset('UTC')

        assert offset == '+00:00'

    def test_new_york_offset(self):
        offset = get_timezone_offset('America/New_York')

        assert offset in ['-05:00', '-04:00']

    def test_tokyo_offset(self):
        offset = get_timezone_offset('Asia/Tokyo')

        assert offset == '+09:00'


class TestIsDST:
    def test_dst_active_in_summer(self):
        summer = arrow.get('2024-07-01', tzinfo='America/New_York')
        assert is_dst(summer) is True

    def test_dst_not_active_in_winter(self):
        winter = arrow.get('2024-01-01', tzinfo='America/New_York')
        assert is_dst(winter) is False

    def test_utc_never_has_dst(self):
        utc = arrow.get('2024-07-01', tzinfo='UTC')
        assert is_dst(utc) is False


class TestGetWorldTimes:
    def test_returns_dict(self):
        utc = arrow.utcnow()
        timezones = ['UTC', 'America/New_York', 'Asia/Tokyo']
        times = get_world_times(utc, timezones)

        assert isinstance(times, dict)
        assert len(times) == 3

    def test_all_timezones_present(self):
        utc = arrow.utcnow()
        timezones = ['UTC', 'America/New_York', 'Europe/London']
        times = get_world_times(utc, timezones)

        for tz in timezones:
            assert tz in times

    def test_invalid_timezone_returns_error(self):
        utc = arrow.utcnow()
        timezones = ['Invalid/Timezone']
        times = get_world_times(utc, timezones)

        assert 'Error' in times['Invalid/Timezone']
