import dataclasses
import datetime

import pytest

import goodtime


def test_eq() -> None:
  assert goodtime.Duration.from_nanos(1) == goodtime.Duration.from_nanos(1)
  assert goodtime.Duration.from_nanos(1) == goodtime.Duration(ns=1)
  assert goodtime.Duration.from_nanos(1) != goodtime.Duration.from_nanos(2)
  assert goodtime.Duration.from_nanos(1) != goodtime.Duration(ns=2)


def test_negative() -> None:
  with pytest.raises(ValueError, match=r"^ns must be non-negative, was -1"):
    goodtime.Duration.from_nanos(-1)


def test_hash() -> None:
  assert isinstance(hash(goodtime.Duration.from_nanos(1)), int)


def test_repr() -> None:
  assert repr(goodtime.Duration.from_nanos(59_123_456_789)) == "Duration(ns=59123456789)"
  assert repr(goodtime.SignedDuration.from_nanos(59_123_456_789)) == "PositiveDuration(Duration(ns=59123456789))"
  assert repr(goodtime.SignedDuration.from_nanos(-59_123_456_789)) == "NegativeDuration(Duration(ns=59123456789))"


def test_order() -> None:
  assert goodtime.Duration.from_nanos(59_123_456_700) > goodtime.Duration.from_nanos(59_123_456_699)
  assert goodtime.Duration.from_nanos(59_123_456_700) >= goodtime.Duration.from_nanos(59_123_456_699)
  assert goodtime.Duration.from_nanos(59_123_456_700) < goodtime.Duration.from_nanos(59_123_456_701)
  assert goodtime.Duration.from_nanos(59_123_456_700) <= goodtime.Duration.from_nanos(59_123_456_701)


def test_frozen() -> None:
  with pytest.raises(dataclasses.FrozenInstanceError):
    goodtime.Duration.from_nanos(10).ns = 17  # type: ignore[misc]


def test_enforces_type() -> None:
  with pytest.raises(TypeError, match=r"^ns must be int, was <class 'NoneType'>$"):
    goodtime.Duration.from_nanos(None)  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^ns must be int, was <class 'str'>$"):
    goodtime.Duration.from_nanos("abc")  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^ns must be int, was <class 'float'>$"):
    goodtime.Duration.from_nanos(1.0)  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^absolute_value must be Duration, was <class 'NoneType'>$"):
    goodtime.PositiveDuration(None)  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^absolute_value must be Duration, was <class 'NoneType'>$"):
    goodtime.NegativeDuration(None)  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^absolute_value must be Duration, was <class 'str'>$"):
    goodtime.PositiveDuration("abc")  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^absolute_value must be Duration, was <class 'str'>$"):
    goodtime.NegativeDuration("abc")  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^absolute_value must be Duration, was <class 'int'>$"):
    goodtime.PositiveDuration(1)  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^absolute_value must be Duration, was <class 'int'>$"):
    goodtime.NegativeDuration(1)  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^absolute_value must be Duration, was <class 'float'>$"):
    goodtime.PositiveDuration(1.0)  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^absolute_value must be Duration, was <class 'float'>$"):
    goodtime.NegativeDuration(1.0)  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^value must be datetime.timedelta, was <class 'NoneType'>$"):
    goodtime.SignedDuration.from_timedelta(None)  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^value must be datetime.timedelta, was <class 'str'>$"):
    goodtime.SignedDuration.from_timedelta("abc")  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^value must be datetime.timedelta, was <class 'int'>$"):
    goodtime.SignedDuration.from_timedelta(1)  # type: ignore[arg-type]
  with pytest.raises(TypeError, match=r"^value must be datetime.timedelta, was <class 'float'>$"):
    goodtime.SignedDuration.from_timedelta(1.0)  # type: ignore[arg-type]


def test_from() -> None:
  assert goodtime.Duration.from_nanos(59_000) == goodtime.Duration.from_micros(59)
  assert goodtime.Duration.from_nanos(59_000_000) == goodtime.Duration.from_millis(59)
  assert goodtime.Duration.from_nanos(59_000_000_000) == goodtime.Duration.from_seconds(59)
  assert goodtime.SignedDuration.from_nanos(59_000) == goodtime.SignedDuration.from_micros(59)
  assert goodtime.SignedDuration.from_nanos(59_000_000) == goodtime.SignedDuration.from_millis(59)
  assert goodtime.SignedDuration.from_nanos(59_000_000_000) == goodtime.SignedDuration.from_seconds(59)
  assert goodtime.SignedDuration.from_nanos(-59_000) == goodtime.SignedDuration.from_micros(-59)
  assert goodtime.SignedDuration.from_nanos(-59_000_000) == goodtime.SignedDuration.from_millis(-59)
  assert goodtime.SignedDuration.from_nanos(-59_000_000_000) == goodtime.SignedDuration.from_seconds(-59)


def test_from_not_supported() -> None:
  with pytest.raises(
    TypeError, match=r"^Calling PositiveDuration.from_nanos is not supported. Call SignedDuration.from_nanos instead.$"
  ):
    goodtime.PositiveDuration.from_nanos(1)
  with pytest.raises(
    TypeError,
    match=r"^Calling PositiveDuration.from_micros is not supported. Call SignedDuration.from_micros instead.$",
  ):
    goodtime.PositiveDuration.from_micros(1)
  with pytest.raises(
    TypeError,
    match=r"^Calling PositiveDuration.from_millis is not supported. Call SignedDuration.from_millis instead.$",
  ):
    goodtime.PositiveDuration.from_millis(1)
  with pytest.raises(
    TypeError,
    match=r"^Calling PositiveDuration.from_seconds is not supported. Call SignedDuration.from_seconds instead.$",
  ):
    goodtime.PositiveDuration.from_seconds(1)
  with pytest.raises(
    TypeError, match=r"^Calling NegativeDuration.from_nanos is not supported. Call SignedDuration.from_nanos instead.$"
  ):
    goodtime.NegativeDuration.from_nanos(1)
  with pytest.raises(
    TypeError,
    match=r"^Calling NegativeDuration.from_micros is not supported. Call SignedDuration.from_micros instead.$",
  ):
    goodtime.NegativeDuration.from_micros(1)
  with pytest.raises(
    TypeError,
    match=r"^Calling NegativeDuration.from_millis is not supported. Call SignedDuration.from_millis instead.$",
  ):
    goodtime.NegativeDuration.from_millis(1)
  with pytest.raises(
    TypeError,
    match=r"^Calling NegativeDuration.from_seconds is not supported. Call SignedDuration.from_seconds instead.$",
  ):
    goodtime.NegativeDuration.from_seconds(1)


def test_to() -> None:
  assert goodtime.Duration.from_nanos(59_123_456_789).to_nanos() == 59_123_456_789
  assert goodtime.Duration.from_nanos(59_123_456_789).to_micros() == 59_123_456
  assert goodtime.Duration.from_nanos(59_123_456_789).to_millis() == 59_123
  assert goodtime.Duration.from_nanos(59_123_456_789).to_seconds() == 59


def test_to_timedelta() -> None:
  td = goodtime.Duration.from_nanos(1470034987654719).to_timedelta()
  assert td.days == 17
  assert td.seconds == 1234
  assert td.microseconds == 987654


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
  ],
)
def test_rounding(from_value: int, to_value: int) -> None:
  assert goodtime.Duration.from_nanos(from_value).to_micros() == to_value
  assert goodtime.Duration.from_micros(from_value).to_millis() == to_value
  assert goodtime.Duration.from_millis(from_value).to_seconds() == to_value


@pytest.mark.parametrize(
  ("from_value", "to_value"),
  [
    (datetime.timedelta(days=0, seconds=0, microseconds=0), goodtime.PositiveDuration(goodtime.Duration(ns=0))),
    (datetime.timedelta(days=0, seconds=0, microseconds=1), goodtime.PositiveDuration(goodtime.Duration(ns=1000))),
    (
      datetime.timedelta(days=0, seconds=1, microseconds=2),
      goodtime.PositiveDuration(goodtime.Duration(ns=1000002000)),
    ),
    (
      datetime.timedelta(days=1, seconds=2, microseconds=3),
      goodtime.PositiveDuration(goodtime.Duration(ns=86402000003000)),
    ),
    (
      datetime.timedelta(days=-1, seconds=2, microseconds=3),
      goodtime.NegativeDuration(goodtime.Duration(ns=86397999997000)),
    ),
    (
      datetime.timedelta(days=-1, seconds=86399, microseconds=999999),
      goodtime.NegativeDuration(goodtime.Duration(ns=1000)),
    ),
  ],
)
def test_signed_from_timedelta(from_value: datetime.timedelta, to_value: goodtime.SignedDuration) -> None:
  assert goodtime.SignedDuration.from_timedelta(from_value) == to_value


@pytest.mark.parametrize(
  ("to_value", "from_value"),
  [
    (datetime.timedelta(days=0, seconds=0, microseconds=0), goodtime.SignedDuration.from_nanos(0)),
    (datetime.timedelta(days=0, seconds=0, microseconds=1), goodtime.SignedDuration.from_nanos(1000)),
    (datetime.timedelta(days=0, seconds=1, microseconds=2), goodtime.SignedDuration.from_nanos(1000002000)),
    (datetime.timedelta(days=1, seconds=2, microseconds=3), goodtime.SignedDuration.from_nanos(86402000003000)),
    (datetime.timedelta(days=-1, seconds=2, microseconds=3), goodtime.SignedDuration.from_nanos(-86397999997000)),
    (datetime.timedelta(days=-1, seconds=86399, microseconds=999999), goodtime.SignedDuration.from_nanos(-1000)),
  ],
)
def test_signed_to_timedelta(to_value: datetime.timedelta, from_value: goodtime.SignedDuration) -> None:
  assert from_value.to_timedelta() == to_value


def test_signed_to_timedelta_not_implemented() -> None:
  with pytest.raises(NotImplementedError):
    goodtime.SignedDuration(absolute_value=goodtime.Duration(ns=1)).to_timedelta()


def test_helpers() -> None:
  assert goodtime.hours(17) == goodtime.PositiveDuration(goodtime.Duration(ns=17 * 3600 * 1_000_000_000))
  assert goodtime.hours(-17) == goodtime.NegativeDuration(goodtime.Duration(ns=17 * 3600 * 1_000_000_000))
  assert goodtime.minutes(17) == goodtime.PositiveDuration(goodtime.Duration(ns=17 * 60 * 1_000_000_000))
  assert goodtime.minutes(-17) == goodtime.NegativeDuration(goodtime.Duration(ns=17 * 60 * 1_000_000_000))
  assert goodtime.seconds(17) == goodtime.PositiveDuration(goodtime.Duration(ns=17 * 1_000_000_000))
  assert goodtime.seconds(-17) == goodtime.NegativeDuration(goodtime.Duration(ns=17 * 1_000_000_000))
  assert goodtime.milliseconds(17) == goodtime.PositiveDuration(goodtime.Duration(ns=17 * 1_000_000))
  assert goodtime.milliseconds(-17) == goodtime.NegativeDuration(goodtime.Duration(ns=17 * 1_000_000))
  assert goodtime.microseconds(17) == goodtime.PositiveDuration(goodtime.Duration(ns=17 * 1_000))
  assert goodtime.microseconds(-17) == goodtime.NegativeDuration(goodtime.Duration(ns=17 * 1_000))
  assert goodtime.nanoseconds(17) == goodtime.PositiveDuration(goodtime.Duration(ns=17))
  assert goodtime.nanoseconds(-17) == goodtime.NegativeDuration(goodtime.Duration(ns=17))


@pytest.mark.parametrize(
  ("a", "b", "result"),
  [
    (goodtime.Duration(ns=1000), goodtime.Duration(ns=1), goodtime.Duration(ns=1001)),
    (goodtime.Duration(ns=1000), goodtime.nanoseconds(1), goodtime.nanoseconds(1001)),
    (goodtime.Duration(ns=1000), goodtime.nanoseconds(-1), goodtime.nanoseconds(999)),
    (goodtime.nanoseconds(1), goodtime.Duration(ns=1000), goodtime.nanoseconds(1001)),
    (goodtime.nanoseconds(-1), goodtime.Duration(ns=1000), goodtime.nanoseconds(999)),
    (goodtime.nanoseconds(1), goodtime.nanoseconds(1000), goodtime.nanoseconds(1001)),
    (goodtime.nanoseconds(-1), goodtime.nanoseconds(1000), goodtime.nanoseconds(999)),
    (goodtime.nanoseconds(1000), goodtime.nanoseconds(-1), goodtime.nanoseconds(999)),
    (goodtime.nanoseconds(-1000), goodtime.nanoseconds(-1), goodtime.nanoseconds(-1001)),
  ],
)
def test_add(a: goodtime.Duration, b: goodtime.Duration, result: goodtime.Duration) -> None:
  assert a + b == result


@pytest.mark.parametrize(
  ("a", "b"),
  [
    (goodtime.Duration(ns=1000), 1),
    (1, goodtime.Duration(ns=1000)),
    (goodtime.hours(1), 1),
    (1, goodtime.hours(1)),
    (goodtime.hours(-1), 1),
    (1, goodtime.hours(-1)),
  ],
)
def test_add_not_implemented(a: goodtime.Duration, b: goodtime.Duration) -> None:
  with pytest.raises(TypeError):
    a + b


@pytest.mark.parametrize(
  ("a", "b", "result"),
  [
    (goodtime.Duration(ns=1000), goodtime.Duration(ns=1), goodtime.nanoseconds(999)),
    (goodtime.Duration(ns=1000), goodtime.nanoseconds(1), goodtime.nanoseconds(999)),
    (goodtime.Duration(ns=1000), goodtime.nanoseconds(-1), goodtime.nanoseconds(1001)),
    (goodtime.nanoseconds(1), goodtime.Duration(ns=1000), goodtime.nanoseconds(-999)),
    (goodtime.nanoseconds(-1), goodtime.Duration(ns=1000), goodtime.nanoseconds(-1001)),
    (goodtime.nanoseconds(1), goodtime.nanoseconds(1000), goodtime.nanoseconds(-999)),
    (goodtime.nanoseconds(-1), goodtime.nanoseconds(1000), goodtime.nanoseconds(-1001)),
    (goodtime.nanoseconds(1000), goodtime.nanoseconds(-1), goodtime.nanoseconds(1001)),
    (goodtime.nanoseconds(-1000), goodtime.nanoseconds(-1), goodtime.nanoseconds(-999)),
  ],
)
def test_sub(a: goodtime.Duration, b: goodtime.Duration, result: goodtime.SignedDuration) -> None:
  assert a - b == result


@pytest.mark.parametrize(
  ("a", "b"),
  [
    (goodtime.Duration(ns=1000), 1),
    (1, goodtime.Duration(ns=1000)),
    (goodtime.hours(1), 1),
    (1, goodtime.hours(1)),
    (goodtime.hours(-1), 1),
    (1, goodtime.hours(-1)),
  ],
)
def test_sub_not_implemented(a: goodtime.Duration, b: goodtime.Duration) -> None:
  with pytest.raises(TypeError):
    a - b


@pytest.mark.parametrize(
  ("smaller", "bigger"),
  [
    (goodtime.Duration(ns=1000), goodtime.nanoseconds(1001)),
    (goodtime.nanoseconds(999), goodtime.Duration(ns=1000)),
    (goodtime.nanoseconds(-1), goodtime.Duration(ns=1)),
    (goodtime.nanoseconds(0), goodtime.Duration(ns=1)),
    (goodtime.nanoseconds(-1), goodtime.Duration(ns=0)),
    (goodtime.nanoseconds(1000), goodtime.nanoseconds(1001)),
    (goodtime.nanoseconds(-1), goodtime.nanoseconds(1)),
    (goodtime.nanoseconds(-1), goodtime.nanoseconds(0)),
    (goodtime.nanoseconds(-2), goodtime.nanoseconds(-1)),
  ],
)
def test_signed_order(smaller: goodtime.SignedDuration, bigger: goodtime.SignedDuration) -> None:
  assert smaller < bigger
  assert smaller <= bigger
  assert bigger > smaller
  assert bigger >= smaller


@pytest.mark.parametrize(
  ("a", "b"),
  [
    (goodtime.Duration(ns=1000), 1),
    (1, goodtime.Duration(ns=1000)),
    (goodtime.hours(1), 1),
    (1, goodtime.hours(1)),
    (goodtime.hours(-1), 1),
    (1, goodtime.hours(-1)),
  ],
)
def test_order_not_implemented(a: goodtime.Duration, b: goodtime.Duration) -> None:
  with pytest.raises(TypeError):
    a < b  # noqa: B015
  with pytest.raises(TypeError):
    a <= b  # noqa: B015
  with pytest.raises(TypeError):
    a > b  # noqa: B015
  with pytest.raises(TypeError):
    a >= b  # noqa: B015
