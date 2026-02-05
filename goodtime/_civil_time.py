"""Representations for civil (local) date and time."""

import dataclasses
import datetime
from typing import final, overload

from ._duration import Duration


@final
@dataclasses.dataclass(init=False, repr=False, order=True, frozen=True, slots=True)
class CivilSecond:
  """CivilSecond represents a civil time with a precision of one second.

  Civil time (or local time) is a date/time combination observed somewhere in
  the world, and generally speaking, only meaningful within a certain
  jurisdiction. It does not correspond uniquely to an absolute timestamp.

  Use a Timezone instance to convert back and forth between civil time and
  absolute time.

  Unlike absolute time (i.e.  Instant), civil time does not represent points in
  the time dimension, but rather can be viewed as a pointer in an infinite list
  of discrete calendar values: ..., 2026-01-01T12:34:56, 2026-01-01T12:34:57,
  ...

  Civil time supports arithmetic operations and comparisons, but a difference
  between two civil times is not a time unit, but an integer "offset" in the
  above mentioned hypothetical list.
  """

  # For now we use a UTC datetime as the underlying representation. This may
  # change in the future.
  dt: datetime.datetime

  def __init__(self, *, dt: datetime.datetime):
    if not isinstance(dt, datetime.datetime):
      msg = f"dt must be datetime.datetime, was {type(dt)}"
      raise TypeError(msg)
    if dt.tzinfo is not datetime.timezone.utc:
      msg = f"dt must have tzinfo=datetime.timezone.utc, was {dt.tzinfo!r}"
      raise ValueError(msg)
    object.__setattr__(self, "dt", dt)

  @classmethod
  def from_utc_datetime(cls, dt: datetime.datetime) -> "CivilSecond":
    return CivilSecond(dt=dt)

  @classmethod
  def from_fields(cls, year: int, month: int, day: int, hour: int, minute: int, second: int) -> "CivilSecond":  # noqa: PLR0913
    return CivilSecond(
      dt=datetime.datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        tzinfo=datetime.timezone.utc,
      )
    )

  @property
  def year(self) -> int:
    """Return the year field of this civil time as int (e.g. 2025)."""
    return self.dt.year

  @property
  def month(self) -> int:
    """Return the month field of this civil time as int (1-12)."""
    return self.dt.month

  @property
  def day(self) -> int:
    """Return the day of the month field of this civil time as int (1-31)."""
    return self.dt.day

  @property
  def hour(self) -> int:
    """Return the hour of the day field of this civil time as int (1-23)."""
    return self.dt.hour

  @property
  def minute(self) -> int:
    """Return the minute field of this civil time as int (0-59)."""
    return self.dt.minute

  @property
  def second(self) -> int:
    """Return the second field of this civil time as int (0-59)."""
    return self.dt.second

  def __add__(self, other: int) -> "CivilSecond":
    if not isinstance(other, int):
      return NotImplemented
    return CivilSecond(dt=self.dt + datetime.timedelta(seconds=other))

  def __radd__(self, other: int) -> "CivilSecond":
    return self.__add__(other)

  @overload
  def __sub__(self, other: int) -> "CivilSecond": ...

  @overload
  def __sub__(self, other: "CivilSecond") -> int: ...

  def __sub__(self, other: "int|CivilSecond") -> "int|CivilSecond":
    if isinstance(other, int):
      return CivilSecond(dt=self.dt - datetime.timedelta(seconds=other))
    if isinstance(other, CivilSecond):
      return int((other.dt - self.dt).total_seconds())
    return NotImplemented


@final
@dataclasses.dataclass(init=False, repr=True, order=True, frozen=True, slots=True)
class CivilTime:
  """CivilTime represents a civil time with a precision of one nanosecond.

  Civil time (or local time) is a date/time combination observed somewhere in
  the world, and generally speaking, only meaningful within a certain
  jurisdiction.

  Subsecond precision is represented by the subsecond duration field which is
  guaranteed to be less than one second.
  """

  second: CivilSecond
  subsecond: Duration

  def __init__(self, *, second: CivilSecond, subsecond: Duration):
    if not isinstance(subsecond, Duration):
      msg = f"subsecond_ns must be Duration, was {type(subsecond)}"
      raise TypeError(msg)
    if not isinstance(second, CivilSecond):
      msg = f"second must be CivilSecond, was {type(second)}"
      raise TypeError(msg)
    if not (0 <= subsecond.to_nanos() < 1_000_000_000):  # noqa: PLR2004
      msg = f"subsecond must be in [0, 1_000_000_000)ns, was {subsecond.to_nanos()}ns"
      raise ValueError(msg)
    object.__setattr__(self, "second", second)
    object.__setattr__(self, "subsecond", subsecond)
