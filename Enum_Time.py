"""Sort the time in an Enum."""

from enum import Enum


class PeriodEnum(Enum):
    """Sorted period slider."""

    DAY1 = ("1 day", "1d")
    DAY5 = ("5 days", "5d")
    MONTH1 = ("1 month", "1mo")
    MONTH3 = ("3 months", "3mo")
    MONTH6 = ("6 months", "6mo")
    YTD = ("year to date", "ytd")
    YEAR = ("1 year", "1y")
    YEARS2 = ("2 years", "2y")
    YEARS5 = ("5 years", "5y")
    YRARS10 = ("10 years", "10y")
    MAX = ("maximum", "max")

    def __init__(self, full_name, short_name):
        """Inicialization."""

        self.full_name = full_name
        self.short_name = short_name


class IntervalEnum(Enum):
    """Sorted Interval slider."""

    MINUTE1 = ("1 Minute", "1m")
    MINUTES2 = ("2 Minutes", "2m")
    MINUTES5 = ("5 Minutes", "5m")
    MINUTES15 = ("15 Minutes", "15m")
    MINUTES30 = ("30 Minutes", "30m")
    MINUTES60 = ("60 Minutes", "60m")
    MINUTES90 = ("90 Minutes", "90m")
    HOUR1 = ("1 Hour", "1h")
    DAY1 = ("1 Day", "1d")
    DAYS5 = ("5 Days", "5d")
    WEEK1 = ("1 Week", "1wk")
    MONTH1 = ("1 Month", "1mo")
    MONTH3 = ("3 Month", "3mo")

    def __init__(self, full_name, short_name):
        """Inicialization."""

        self.full_name = full_name
        self.short_name = short_name
