import pytest

import goodtime


@pytest.mark.parametrize(
  ("tzname", "instant", "fields"),
  [
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1770233135094), (2026, 2, 4, 20, 25, 35, 94_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1774739700111), (2026, 3, 29, 0, 15, 0, 111_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1774743300111), (2026, 3, 29, 1, 15, 0, 111_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1774746900111), (2026, 3, 29, 3, 15, 0, 111_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1774750500111), (2026, 3, 29, 4, 15, 0, 111_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1792880000222), (2026, 10, 25, 0, 13, 20, 222_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1792883000222), (2026, 10, 25, 1, 3, 20, 222_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1792887000222), (2026, 10, 25, 2, 10, 0, 222_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1792891000222), (2026, 10, 25, 2, 16, 40, 222_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1792894000222), (2026, 10, 25, 3, 6, 40, 222_000_000)),
  ],
)
def test_instant_to_civil_time(tzname: str, instant: goodtime.Instant, fields: tuple) -> None:  # type: ignore[type-arg]
  tz = goodtime.Timezone.from_tzdata_identifier(tzname)
  ct = tz.instant_to_civil_time(instant)
  assert (
    ct.second.year,
    ct.second.month,
    ct.second.day,
    ct.second.hour,
    ct.second.minute,
    ct.second.second,
    ct.subsecond.to_nanos(),
  ) == fields


@pytest.mark.parametrize(
  ("tzname", "instant", "fields"),
  [
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1770233135094), (2026, 2, 4, 20, 25, 35, 94_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1774739700111), (2026, 3, 29, 0, 15, 0, 111_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1774743300111), (2026, 3, 29, 1, 15, 0, 111_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1774746900111), (2026, 3, 29, 3, 15, 0, 111_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1774750500111), (2026, 3, 29, 4, 15, 0, 111_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1774745999999), (2026, 3, 29, 1, 59, 59, 999_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1774746000000), (2026, 3, 29, 3, 0, 0, 0)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1774746000001), (2026, 3, 29, 3, 0, 0, 1_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1792880000222), (2026, 10, 25, 0, 13, 20, 222_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1792883000222), (2026, 10, 25, 1, 3, 20, 222_000_000)),
    ("Europe/Berlin", goodtime.Instant.from_unix_millis(1792894000222), (2026, 10, 25, 3, 6, 40, 222_000_000)),
  ],
)
def test_civil_time_to_instant_unique(tzname: str, instant: goodtime.Instant, fields: tuple) -> None:  # type: ignore[type-arg]
  tz = goodtime.Timezone.from_tzdata_identifier(tzname)
  ct = goodtime.CivilTime(
    second=goodtime.CivilSecond.from_fields(*fields[:6]),
    subsecond=goodtime.Duration.from_nanos(fields[6]),
  )
  result = tz.civil_time_to_instant(ct)
  assert isinstance(result, goodtime.UniqueCivilTimeInstant)
  assert result.instant == instant


@pytest.mark.parametrize(
  ("tzname", "post_instant", "pre_instant", "trans_instant", "fields"),
  [
    (
      "Europe/Berlin",
      goodtime.Instant.from_unix_millis(1774743300111),
      goodtime.Instant.from_unix_millis(1774746900111),
      goodtime.Instant.from_unix_millis(1774746000000),
      (2026, 3, 29, 2, 15, 0, 111_000_000),
    ),
    (
      "Europe/Berlin",
      goodtime.Instant.from_unix_millis(1774742400000),
      goodtime.Instant.from_unix_millis(1774746000000),
      goodtime.Instant.from_unix_millis(1774746000000),
      (2026, 3, 29, 2, 0, 0, 0),
    ),
    (
      "Europe/Berlin",
      goodtime.Instant.from_unix_nanos(1774745999999999999),
      goodtime.Instant.from_unix_nanos(1774749599999999999),
      goodtime.Instant.from_unix_millis(1774746000000),
      (2026, 3, 29, 2, 59, 59, 999_999_999),
    ),
  ],
)
def test_civil_time_to_instant_skipped(
  tzname: str,
  post_instant: goodtime.Instant,
  pre_instant: goodtime.Instant,
  trans_instant: goodtime.Instant,
  fields: tuple,  # type: ignore[type-arg]
) -> None:
  tz = goodtime.Timezone.from_tzdata_identifier(tzname)
  ct = goodtime.CivilTime(
    second=goodtime.CivilSecond.from_fields(*fields[:6]),
    subsecond=goodtime.Duration.from_nanos(fields[6]),
  )
  result = tz.civil_time_to_instant(ct)
  assert isinstance(result, goodtime.SkippedCivilTimeInstant)
  assert result.post_transition == post_instant
  assert result.pre_transition == pre_instant
  assert result.transition == trans_instant


@pytest.mark.parametrize(
  ("tzname", "post_instant", "pre_instant", "trans_instant", "fields"),
  [
    (
      "Europe/Berlin",
      goodtime.Instant.from_unix_millis(1792890600222),
      goodtime.Instant.from_unix_millis(1792887000222),
      goodtime.Instant.from_unix_millis(1792890000000),
      (2026, 10, 25, 2, 10, 0, 222_000_000),
    ),
    (
      "Europe/Berlin",
      goodtime.Instant.from_unix_millis(1792890000000),
      goodtime.Instant.from_unix_millis(1792886400000),
      goodtime.Instant.from_unix_millis(1792890000000),
      (2026, 10, 25, 2, 0, 0, 0),
    ),
    (
      "Europe/Berlin",
      goodtime.Instant.from_unix_nanos(1792893599999999999),
      goodtime.Instant.from_unix_nanos(1792889999999999999),
      goodtime.Instant.from_unix_millis(1792890000000),
      (2026, 10, 25, 2, 59, 59, 999_999_999),
    ),
  ],
)
def test_civil_time_to_instant_repeated(
  tzname: str,
  post_instant: goodtime.Instant,
  pre_instant: goodtime.Instant,
  trans_instant: goodtime.Instant,
  fields: tuple,  # type: ignore[type-arg]
) -> None:
  tz = goodtime.Timezone.from_tzdata_identifier(tzname)
  ct = goodtime.CivilTime(
    second=goodtime.CivilSecond.from_fields(*fields[:6]),
    subsecond=goodtime.Duration.from_nanos(fields[6]),
  )
  result = tz.civil_time_to_instant(ct)
  assert isinstance(result, goodtime.RepeatedCivilTimeInstant)
  assert result.post_transition == post_instant
  assert result.pre_transition == pre_instant
  assert result.transition == trans_instant
