"""
Tests for date helper functions.
"""

import pytest
from freezegun import freeze_time

import arrow
from utils.date_helpers import (
    age_from_birthdate,
    days_until,
    get_date_range,
    get_month_dates,
    get_quarter_dates,
    is_business_day,
    next_business_day,
)


class TestGetDateRange:
    def test_daily_range(self):
        start = arrow.get('2024-02-01')
        end = arrow.get('2024-02-05')
        dates = get_date_range(start, end, 'day')

        assert len(dates) == 5
        assert dates[0].format('YYYY-MM-DD') == '2024-02-01'
        assert dates[-1].format('YYYY-MM-DD') == '2024-02-05'

    def test_weekly_range(self):
        start = arrow.get('2024-02-01')
        end = arrow.get('2024-02-29')
        dates = get_date_range(start, end, 'week')

        assert len(dates) == 5
        assert dates[0].format('YYYY-MM-DD') == '2024-02-01'

    def test_monthly_range(self):
        start = arrow.get('2024-01-01')
        end = arrow.get('2024-03-01')
        dates = get_date_range(start, end, 'month')

        assert len(dates) == 3

    def test_invalid_step(self):
        start = arrow.get('2024-02-01')
        end = arrow.get('2024-02-05')

        with pytest.raises(ValueError, match="Invalid step"):
            get_date_range(start, end, 'invalid')


class TestBusinessDay:
    def test_monday_is_business_day(self):
        date = arrow.get('2024-02-05')
        assert is_business_day(date) is True

    def test_saturday_is_not_business_day(self):
        date = arrow.get('2024-02-10')
        assert is_business_day(date) is False

    def test_sunday_is_not_business_day(self):
        date = arrow.get('2024-02-11')
        assert is_business_day(date) is False

    def test_next_business_day_from_friday(self):
        friday = arrow.get('2024-02-09')
        next_day = next_business_day(friday)

        assert next_day.format('YYYY-MM-DD') == '2024-02-12'

    def test_next_business_day_from_monday(self):
        monday = arrow.get('2024-02-05')
        next_day = next_business_day(monday)

        assert next_day.format('YYYY-MM-DD') == '2024-02-06'


class TestQuarterDates:
    def test_first_quarter(self):
        start, end = get_quarter_dates(2024, 1)

        assert start.format('YYYY-MM-DD') == '2024-01-01'
        assert end.month == 3

    def test_second_quarter(self):
        start, end = get_quarter_dates(2024, 2)

        assert start.month == 4
        assert end.month == 6

    def test_invalid_quarter(self):
        with pytest.raises(ValueError, match="Quarter must be"):
            get_quarter_dates(2024, 5)


class TestMonthDates:
    def test_january(self):
        start, end = get_month_dates(2024, 1)

        assert start.format('YYYY-MM-DD') == '2024-01-01'
        assert end.month == 1
        assert end.day == 31

    def test_february_leap_year(self):
        start, end = get_month_dates(2024, 2)

        assert start.format('YYYY-MM-DD') == '2024-02-01'
        assert end.day == 29

    def test_february_non_leap_year(self):
        start, end = get_month_dates(2023, 2)

        assert end.day == 28


@freeze_time("2024-02-07")
class TestDaysUntil:
    def test_future_date(self):
        future = arrow.get('2024-02-12')
        days = days_until(future)

        assert days == 5

    def test_past_date(self):
        past = arrow.get('2024-02-01')
        days = days_until(past)

        assert days == -6

    def test_same_date(self):
        today = arrow.get('2024-02-07')
        days = days_until(today)

        assert days == 0


@freeze_time("2024-02-07")
class TestAgeFromBirthdate:
    def test_adult_age(self):
        birthdate = arrow.get('1990-01-01')
        age = age_from_birthdate(birthdate)

        assert age == 34

    def test_birthday_not_yet_this_year(self):
        birthdate = arrow.get('1990-03-01')
        age = age_from_birthdate(birthdate)

        assert age == 33

    def test_birthday_today(self):
        birthdate = arrow.get('1990-02-07')
        age = age_from_birthdate(birthdate)

        assert age == 34

    def test_future_birthdate_raises_error(self):
        future = arrow.get('2025-01-01')

        with pytest.raises(ValueError, match="cannot be in the future"):
            age_from_birthdate(future)
