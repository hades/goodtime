import dataclasses
import datetime

import pytest

import goodtime


def test_eq() -> None:
  assert goodtime.Instant.from_unix_nanos(1) == goodtime.Instant.from_unix_nanos(1)
  assert goodtime.Instant.from_unix_nanos(1) == goodtime.Instant(unix_timestamp_ns=1)
  assert goodtime.Instant.from_unix_nanos(1) != goodtime.Instant.from_unix_nanos(-1)
  assert goodtime.Instant.from_unix_nanos(1) != goodtime.Instant(unix_timestamp_ns=-1)


def test_hash() -> None:
  assert isinstance(hash(goodtime.Instant.from_unix_nanos(1)), int)


def test_repr() -> None:
  assert repr(goodtime.Instant.from_unix_nanos(59_123_456_789)) == "Instant(unix_timestamp_ns=59123456789)"


def test_order() -> None:
  assert goodtime.Instant.from_unix_nanos(59_123_456_700) > goodtime.Instant.from_unix_nanos(59_123_456_699)
  assert goodtime.Instant.from_unix_nanos(59_123_456_700) >= goodtime.Instant.from_unix_nanos(59_123_456_699)
  assert goodtime.Instant.from_unix_nanos(59_123_456_700) < goodtime.Instant.from_unix_nanos(59_123_456_701)
  assert goodtime.Instant.from_unix_nanos(59_123_456_700) <= goodtime.Instant.from_unix_nanos(59_123_456_701)


def test_frozen() -> None:
  with pytest.raises(dataclasses.FrozenInstanceError):
    goodtime.Instant.from_unix_nanos(10).unix_timestamp_ns = 17  # type: ignore[misc]


def test_enforces_type() -> None:
  with pytest.raises(TypeError, match=r"^unix_timestamp_ns must be int, was <class 'NoneType'>$"):
    goodtime.Instant.from_unix_nanos(None)  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^unix_timestamp_ns must be int, was <class 'str'>$"):
    goodtime.Instant.from_unix_nanos("abc")  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^unix_timestamp_ns must be int, was <class 'float'>$"):
    goodtime.Instant.from_unix_nanos(1.0)  # type: ignore[arg-type]


def test_from_unix() -> None:
  assert goodtime.Instant.from_unix_nanos(59_000) == goodtime.Instant.from_unix_micros(59)
  assert goodtime.Instant.from_unix_nanos(59_000_000) == goodtime.Instant.from_unix_millis(59)
  assert goodtime.Instant.from_unix_nanos(59_000_000_000) == goodtime.Instant.from_unix_seconds(59)


def test_to_unix() -> None:
  assert goodtime.Instant.from_unix_nanos(59_123_456_789).to_unix_nanos() == 59_123_456_789
  assert goodtime.Instant.from_unix_nanos(59_123_456_789).to_unix_micros() == 59_123_456
  assert goodtime.Instant.from_unix_nanos(59_123_456_789).to_unix_millis() == 59_123
  assert goodtime.Instant.from_unix_nanos(59_123_456_789).to_unix_seconds() == 59


@pytest.mark.parametrize(
  ("from_value", "to_value"),
  [
    (59_001, 59),
    (59_449, 59),
    (59_500, 59),
    (59_501, 59),
    (59_999, 59),
    (1, 0),
    (449, 0),
    (500, 0),
    (501, 0),
    (999, 0),
    (-59_001, -60),
    (-59_449, -60),
    (-59_500, -60),
    (-59_501, -60),
    (-59_999, -60),
  ],
)
def test_rounding(from_value: int, to_value: int) -> None:
  assert goodtime.Instant.from_unix_nanos(from_value).to_unix_micros() == to_value
  assert goodtime.Instant.from_unix_micros(from_value).to_unix_millis() == to_value
  assert goodtime.Instant.from_unix_millis(from_value).to_unix_seconds() == to_value


def test_now() -> None:
  now = goodtime.Instant.now()
  # Hello, 2029, how's it going?
  assert goodtime.Instant.from_unix_millis(1769939551062) < now < goodtime.Instant.from_unix_millis(1869939551062)


def test_add() -> None:
  assert goodtime.Instant.from_unix_seconds(1) + goodtime.seconds(2) == goodtime.Instant.from_unix_seconds(3)
  assert goodtime.Instant.from_unix_seconds(1) + goodtime.milliseconds(2) == goodtime.Instant.from_unix_millis(1002)
  assert goodtime.Instant.from_unix_seconds(1) + goodtime.microseconds(2) == goodtime.Instant.from_unix_micros(
    1_000_002
  )
  assert goodtime.Instant.from_unix_seconds(1) + goodtime.nanoseconds(2) == goodtime.Instant.from_unix_nanos(
    1_000_000_002
  )
  assert goodtime.Instant.from_unix_seconds(1) + goodtime.seconds(-2) == goodtime.Instant.from_unix_seconds(-1)
  assert goodtime.Instant.from_unix_seconds(1) + goodtime.milliseconds(-2) == goodtime.Instant.from_unix_millis(998)
  assert goodtime.Instant.from_unix_seconds(1) + goodtime.microseconds(-2) == goodtime.Instant.from_unix_micros(999_998)
  assert goodtime.Instant.from_unix_seconds(1) + goodtime.nanoseconds(-2) == goodtime.Instant.from_unix_nanos(
    999_999_998
  )


def test_radd() -> None:
  assert goodtime.seconds(2) + goodtime.Instant.from_unix_seconds(1) == goodtime.Instant.from_unix_seconds(3)
  assert goodtime.milliseconds(2) + goodtime.Instant.from_unix_seconds(1) == goodtime.Instant.from_unix_millis(1002)
  assert goodtime.microseconds(2) + goodtime.Instant.from_unix_seconds(1) == goodtime.Instant.from_unix_micros(
    1_000_002
  )
  assert goodtime.nanoseconds(2) + goodtime.Instant.from_unix_seconds(1) == goodtime.Instant.from_unix_nanos(
    1_000_000_002
  )
  assert goodtime.seconds(-2) + goodtime.Instant.from_unix_seconds(1) == goodtime.Instant.from_unix_seconds(-1)
  assert goodtime.milliseconds(-2) + goodtime.Instant.from_unix_seconds(1) == goodtime.Instant.from_unix_millis(998)
  assert goodtime.microseconds(-2) + goodtime.Instant.from_unix_seconds(1) == goodtime.Instant.from_unix_micros(999_998)
  assert goodtime.nanoseconds(-2) + goodtime.Instant.from_unix_seconds(1) == goodtime.Instant.from_unix_nanos(
    999_999_998
  )


def test_add_not_implemented() -> None:
  with pytest.raises(TypeError):
    goodtime.Instant.from_unix_seconds(1) + goodtime.Instant.from_unix_seconds(1)  # type: ignore[operator]
  with pytest.raises(TypeError):
    goodtime.Instant.from_unix_seconds(1) + 1  # type: ignore[operator]
  with pytest.raises(TypeError):
    goodtime.Instant.from_unix_seconds(1) + datetime.datetime.now()  # type: ignore[operator]  # noqa: DTZ005
  with pytest.raises(TypeError):
    1 + goodtime.Instant.from_unix_seconds(1)  # type: ignore[operator]
  with pytest.raises(TypeError):
    datetime.datetime.now() + goodtime.Instant.from_unix_seconds(1)  # type: ignore[operator]  # noqa: DTZ005


def test_sub_signed_duration() -> None:
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.seconds(-2) == goodtime.Instant.from_unix_seconds(3)
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.milliseconds(-2) == goodtime.Instant.from_unix_millis(1002)
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.microseconds(-2) == goodtime.Instant.from_unix_micros(
    1_000_002
  )
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.nanoseconds(-2) == goodtime.Instant.from_unix_nanos(
    1_000_000_002
  )
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.seconds(2) == goodtime.Instant.from_unix_seconds(-1)
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.milliseconds(2) == goodtime.Instant.from_unix_millis(998)
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.microseconds(2) == goodtime.Instant.from_unix_micros(999_998)
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.nanoseconds(2) == goodtime.Instant.from_unix_nanos(
    999_999_998
  )


def test_sub_unsigned_duration() -> None:
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.Duration.from_seconds(
    2
  ) == goodtime.Instant.from_unix_seconds(-1)
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.Duration.from_millis(2) == goodtime.Instant.from_unix_millis(
    998
  )
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.Duration.from_micros(2) == goodtime.Instant.from_unix_micros(
    999_998
  )
  assert goodtime.Instant.from_unix_seconds(1) - goodtime.Duration.from_nanos(2) == goodtime.Instant.from_unix_nanos(
    999_999_998
  )


def test_sub_instant() -> None:
  assert goodtime.Instant.from_unix_seconds(3601) - goodtime.Instant.from_unix_seconds(1) == goodtime.hours(1)


def test_sub_not_implemented() -> None:
  with pytest.raises(TypeError):
    goodtime.Instant.from_unix_seconds(1) - 1  # type: ignore[operator]
  with pytest.raises(TypeError):
    goodtime.Instant.from_unix_seconds(1) - datetime.datetime.now()  # type: ignore[operator]  # noqa: DTZ005
  with pytest.raises(TypeError):
    1 - goodtime.Instant.from_unix_seconds(1)  # type: ignore[operator]
  with pytest.raises(TypeError):
    datetime.datetime.now() - goodtime.Instant.from_unix_seconds(1)  # type: ignore[operator]  # noqa: DTZ005
