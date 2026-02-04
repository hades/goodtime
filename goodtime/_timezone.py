"""Representations for time zones."""

import dataclasses
import datetime
import zoneinfo

from ._civil_time import CivilSecond, CivilTime
from ._duration import Duration
from ._instant import Instant


@dataclasses.dataclass(frozen=True, repr=True, init=True, slots=True, eq=True)
class UniqueCivilTimeInstant:
  """Civil time that has been uniquely mapped to an absolute instant.

  This will be the result of Timezone.civil_time_to_instant most of the time
  (i.e. except DST transitions).
  """

  instant: Instant


@dataclasses.dataclass(frozen=True, repr=True, init=True, slots=True, eq=True)
class RepeatedCivilTimeInstant:
  """Civil time that happens twice due to DST transitions.

  When Daylight Savings Time ends, the civil wall clock will display time that
  it has already displayed before. It is therefore impossible to uniquely
  identify the exact absolute instant of when the provided civil time was
  observed.

  Two possible options are pre_transition (civil time was observed before the
  DST ended) and post_transition (after the DST ended). The instant of the
  transition itself is returned in the transition field.
  """

  pre_transition: Instant
  post_transition: Instant
  transition: Instant


@dataclasses.dataclass(frozen=True, repr=True, init=True, slots=True, eq=True)
class SkippedCivilTimeInstant:
  """Civil time that was (or will be) skipped.

  When Daylight Savings Time begins, the civil wall clock will skip certain
  times. The provided civil time never happened (and never will happen).

  For convenience, the instant of the transition itself is returned, as well as
  instants when two hypothetical incorrect wall clocks would have shown the
  provided civil time: pre_transition (wall clock that was not updated for the
  DST), and post_transition (wall clock that was updated for the DST too early).
  """

  pre_transition: Instant
  post_transition: Instant
  transition: Instant


CivilTimeInstant = UniqueCivilTimeInstant | RepeatedCivilTimeInstant | SkippedCivilTimeInstant


@dataclasses.dataclass(frozen=True, repr=True, order=False, slots=True, eq=False)
class Timezone:
  """A Timezone represents a geographical region with identical civil time.

  This is not the same as a UTC offset, since multiple regions have different
  UTC offsets throughout the year (such as offsets for standard time and
  daylight saving time).

  To construct an instance of Timezone, use the from_tzdata_identifier factory
  function.
  """

  tzinfo: datetime.tzinfo

  @classmethod
  def from_tzdata_identifier(cls, identifier: str) -> "Timezone":
    """Construct a Timezone instance from a string identifier.

    This identifier is also known as tzdata identifier, zoneinfo identifier or
    IANA time zone. Examples are "America/Los_Angeles" and "Europe/Berlin".
    """
    return Timezone(zoneinfo.ZoneInfo(identifier))

  def instant_to_civil_time(self, instant: Instant) -> CivilTime:
    """Return the civil time for this timezone at a certain instant."""
    seconds, nanoseconds = divmod(instant.to_unix_nanos(), 1_000_000_000)
    dt = datetime.datetime.fromtimestamp(seconds, tz=datetime.timezone.utc).astimezone(self.tzinfo)
    dt = datetime.datetime(
      year=dt.year,
      month=dt.month,
      day=dt.day,
      hour=dt.hour,
      minute=dt.minute,
      second=dt.second,
      tzinfo=datetime.timezone.utc,
    )
    return CivilTime(second=CivilSecond.from_utc_datetime(dt), subsecond=Duration.from_nanos(nanoseconds))

  def civil_time_to_instant(self, civil_time: CivilTime) -> CivilTimeInstant:
    """Return the absolute instant when a given civil time was observed in this timezone.

    When a civil time is repeated or skipped due to DST transitions, returns times calculated
    before and after the transition, as well as the transition time itself.
    """
    utc_ts = int(
      datetime.datetime(
        year=civil_time.second.year,
        month=civil_time.second.month,
        day=civil_time.second.day,
        hour=civil_time.second.hour,
        minute=civil_time.second.minute,
        second=civil_time.second.second,
        tzinfo=datetime.timezone.utc,
      ).timestamp()
    )
    offsets: list[tuple[int, int]] = []
    for ts in range(utc_ts - 38 * 3600, utc_ts + 38 * 3600):
      offset_td = datetime.datetime.fromtimestamp(ts, tz=self.tzinfo).utcoffset()
      if not offset_td:
        continue
      offset = int(offset_td.total_seconds())
      if not offsets or offsets[-1][0] != offset:
        offsets.append((offset, ts))
    if not offsets:
      msg = (
        "Unable to look up Instant based on given time zone and civil_time: tzinfo {self.tzinfo!r} did not "
        "return UTC offsets as expected."
      )
      raise ValueError(msg)
    if len(offsets) == 1:
      return UniqueCivilTimeInstant(Instant.from_unix_seconds(utc_ts - offsets[0][0]) + civil_time.subsecond)
    if len(offsets) > 2:  # noqa: PLR2004
      msg = (
        "Unable to look up Instant based on given time zone and civil_time: tzinfo {self.tzinfo!r} returned "
        "too many different UTC offsets around the expected time."
      )
      raise ValueError(msg)
    transition_ts = offsets[1][1]
    pre_ts = utc_ts - offsets[0][0]
    post_ts = utc_ts - offsets[1][0]
    is_pre_ts_valid = pre_ts < transition_ts
    is_post_ts_valid = post_ts >= transition_ts
    match (is_pre_ts_valid, is_post_ts_valid):
      case (True, True):
        return RepeatedCivilTimeInstant(
          Instant.from_unix_seconds(pre_ts) + civil_time.subsecond,
          Instant.from_unix_seconds(post_ts) + civil_time.subsecond,
          Instant.from_unix_seconds(transition_ts),
        )
      case (True, False):
        return UniqueCivilTimeInstant(
          Instant.from_unix_seconds(pre_ts) + civil_time.subsecond,
        )
      case (False, True):
        return UniqueCivilTimeInstant(
          Instant.from_unix_seconds(post_ts) + civil_time.subsecond,
        )
    return SkippedCivilTimeInstant(
      Instant.from_unix_seconds(pre_ts) + civil_time.subsecond,
      Instant.from_unix_seconds(post_ts) + civil_time.subsecond,
      Instant.from_unix_seconds(transition_ts),
    )
