"""Representations for civil (local) date and time."""

import dataclasses
import datetime
from typing import final

from ._duration import Duration


@final
@dataclasses.dataclass(init=False, repr=False, order=True, frozen=True, slots=True)
class CivilSecond:
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
    return self.dt.year

  @property
  def month(self) -> int:
    return self.dt.month

  @property
  def day(self) -> int:
    return self.dt.day

  @property
  def hour(self) -> int:
    return self.dt.hour

  @property
  def minute(self) -> int:
    return self.dt.minute

  @property
  def second(self) -> int:
    return self.dt.second


@final
@dataclasses.dataclass(init=False, repr=True, order=True, frozen=True, slots=True)
class CivilTime:
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
