"""Durations represent finite lengths of time."""

import dataclasses
import datetime
from typing import final


@final
@dataclasses.dataclass(init=False, repr=True, order=True, frozen=True, slots=True)
class Duration:
  """Duration represents a fixed length of time with nanosecond precision.

  The Duration values can be constructed using factory functions (from_nanos,
  from_micros, from_millis and from_seconds) and can be used for unit
  arithmetic, e.g.  adding or subtracting from each other and to/from the
  Instant values.

  Unlike SignedDuration, the length of time is always non-negative. It is therefore
  useful for measuring, for example, the amount of time a request or a computation took
  place, or to set a timeout.

  Python operators (comparison, hashing, addition, subtraction) are supported
  naturally. Note that subtracting another Duration results in a SignedDuration.

  It is recommended to use this (or SignedDuration) type in all APIs (fields,
  function signatures) instead of raw integers to avoid ambiguity. Use explicit
  conversion functions at the boundary of your code to interoperate with
  non-goodtime libraries and APIs.
  """

  ns: int

  def __init__(self, *, ns: int):
    """Create an instance of Duration from non-negative amount of nanoseconds.

    To improve readability it is recommended to use the explicit factory functions (from_nanos
    from_micros, from_millis and from_seconds) instead.
    """
    if not isinstance(ns, int):
      msg = f"ns must be int, was {type(ns)}"
      raise TypeError(msg)
    if ns < 0:
      msg = f"ns must be non-negative, was {ns}"
      raise ValueError(msg)
    object.__setattr__(self, "ns", ns)

  @classmethod
  def from_nanos(cls, value: int) -> "Duration":
    """Create an instance of Duration from non-negative amount of nanoseconds."""
    return cls(ns=value)

  @classmethod
  def from_micros(cls, value: int) -> "Duration":
    """Create an instance of Duration from non-negative amount of microseconds."""
    return cls(ns=value * 1000)

  @classmethod
  def from_millis(cls, value: int) -> "Duration":
    """Create an instance of Duration from non-negative amount of milliseconds."""
    return cls(ns=value * 1_000_000)

  @classmethod
  def from_seconds(cls, value: int) -> "Duration":
    """Create an instance of Duration from non-negative amount of seconds."""
    return cls(ns=value * 1_000_000_000)

  def to_nanos(self) -> int:
    """Return the duration as integer amount of nanoseconds."""
    return self.ns

  def to_micros(self) -> int:
    """Return the duration as integer amount of microseconds, rounding towards zero."""
    return self.ns // 1000

  def to_millis(self) -> int:
    """Return the duration as integer amount of milliseconds, rounding towards zero."""
    return self.ns // 1_000_000

  def to_seconds(self) -> int:
    """Return the duration as integer amount of seconds, rounding towards zero."""
    return self.ns // 1_000_000_000

  def to_timedelta(self) -> datetime.timedelta:
    """Return the duration as Python timedelta value, rounding towards zero."""
    return datetime.timedelta(microseconds=self.to_micros())

  def __add__(self, other: "Duration") -> "Duration":
    if not isinstance(other, Duration):
      return NotImplemented
    return Duration(ns=self.ns + other.ns)

  def __sub__(self, other: "Duration") -> "SignedDuration":
    if not isinstance(other, Duration):
      return NotImplemented
    return SignedDuration.from_nanos(self.ns - other.ns)


@dataclasses.dataclass(init=False, repr=False, order=False, frozen=True, slots=True)
class SignedDuration:
  """SignedDuration represents a fixed length of time with nanosecond precision.

  The SignedDuration values can be constructed using factory functions (from_nanos,
  from_micros, from_millis and from_seconds) or convenience helper functions
  (hours, minutes, seconds, etc.) and can be used for unit arithmetic, e.g.
  adding or subtracting from each other and to/from the Instant values.

  Do not use SignedDuration constructor directly. SignedDuration is meant as a
  union type, and may be updated in the future to prevent incorrect usage.

  Unlike Duration, the length of time can be negative. This makes it useful for
  unit arithmetic, while simultaneously preventing the user from accidentally
  using a negative duration where it does not make sense, such as timeouts.

  To extract Duration from SignedDuration, check whether your value is an
  instance of PositiveDuration or NegativeDuration. A `match` operator provides
  a concise syntax for this:

      >>> def print_duration(d: Duration) -> None:
      ...  match d:
      ...   case PositiveDuration(p):
      ...    print(f"{p.to_seconds()}s")
      ...   case NegativeDuration(n):
      ...    print(f"-{n.to_seconds()}s")
      ...
      >>> print_duration(hours(2))
      7200s
      >>> print_duration(hours(-2))
      -7200s

  Python operators (comparison, hashing, addition, subtraction) are supported
  naturally. Note that adding a SignedDuration to a Duration results in a
  SignedDuration.

  It is recommended to use this (or Duration) type in all APIs (fields, function
  signatures) instead of raw integers to avoid ambiguity. Use explicit
  conversion functions at the boundary of your code to interoperate with
  non-goodtime libraries and APIs.
  """

  absolute_value: Duration

  def __init__(self, absolute_value: Duration):
    """Use only in subclasses of SignedDuration."""
    if not isinstance(absolute_value, Duration):
      msg = f"absolute_value must be Duration, was {type(absolute_value)}"
      raise TypeError(msg)
    object.__setattr__(self, "absolute_value", absolute_value)

  @classmethod
  def from_timedelta(cls, value: datetime.timedelta) -> "SignedDuration":
    """Create an instance of SignedDuration from a Python timedelta value."""
    if not isinstance(value, datetime.timedelta):
      msg = f"value must be datetime.timedelta, was {type(value)}"
      raise TypeError(msg)
    if value.days >= 0:
      return PositiveDuration(Duration.from_micros(value // datetime.timedelta(microseconds=1)))
    return NegativeDuration(Duration.from_micros(value // datetime.timedelta(microseconds=-1)))

  @classmethod
  def from_nanos(cls, value: int) -> "SignedDuration":
    """Create an instance of SignedDuration from integer amount of nanoseconds."""
    if value > 0:
      return PositiveDuration(Duration(ns=value))
    return NegativeDuration(Duration(ns=-value))

  @classmethod
  def from_micros(cls, value: int) -> "SignedDuration":
    """Create an instance of SignedDuration from integer amount of microseconds."""
    if value > 0:
      return PositiveDuration(Duration(ns=value * 1000))
    return NegativeDuration(Duration(ns=-value * 1000))

  @classmethod
  def from_millis(cls, value: int) -> "SignedDuration":
    """Create an instance of SignedDuration from integer amount of milliseconds."""
    if value > 0:
      return PositiveDuration(Duration(ns=value * 1_000_000))
    return NegativeDuration(Duration(ns=-value * 1_000_000))

  @classmethod
  def from_seconds(cls, value: int) -> "SignedDuration":
    """Create an instance of SignedDuration from integer amount of seconds."""
    if value > 0:
      return PositiveDuration(Duration(ns=value * 1_000_000_000))
    return NegativeDuration(Duration(ns=-value * 1_000_000_000))

  def to_timedelta(self) -> datetime.timedelta:
    """Return the duration as Python timedelta value, rounding towards negative infinity."""
    raise NotImplementedError

  def __ge__(self, other: "SignedDuration|Duration") -> bool:
    return NotImplemented

  def __gt__(self, other: "SignedDuration|Duration") -> bool:
    return NotImplemented

  def __le__(self, other: "SignedDuration|Duration") -> bool:
    return NotImplemented

  def __lt__(self, other: "SignedDuration|Duration") -> bool:
    return NotImplemented


@final
class PositiveDuration(SignedDuration):
  def __repr__(self) -> str:
    return f"PositiveDuration({self.absolute_value!r})"

  @classmethod
  def from_nanos(cls, _value: int) -> SignedDuration:
    msg = "Calling PositiveDuration.from_nanos is not supported. Call SignedDuration.from_nanos instead."
    raise TypeError(msg)

  @classmethod
  def from_micros(cls, _value: int) -> SignedDuration:
    msg = "Calling PositiveDuration.from_micros is not supported. Call SignedDuration.from_micros instead."
    raise TypeError(msg)

  @classmethod
  def from_millis(cls, _value: int) -> SignedDuration:
    msg = "Calling PositiveDuration.from_millis is not supported. Call SignedDuration.from_millis instead."
    raise TypeError(msg)

  @classmethod
  def from_seconds(cls, _value: int) -> SignedDuration:
    msg = "Calling PositiveDuration.from_seconds is not supported. Call SignedDuration.from_seconds instead."
    raise TypeError(msg)

  def to_timedelta(self) -> datetime.timedelta:
    return datetime.timedelta(microseconds=self.absolute_value.to_micros())

  def __add__(self, other: SignedDuration | Duration) -> SignedDuration:
    match other:
      case Duration(ns=other_ns) | PositiveDuration(Duration(ns=other_ns)):
        return SignedDuration.from_nanos(self.absolute_value.ns + other_ns)
      case NegativeDuration(Duration(ns=other_negative_ns)):
        return SignedDuration.from_nanos(self.absolute_value.ns - other_negative_ns)
    return NotImplemented

  def __radd__(self, other: Duration) -> SignedDuration:
    return self.__add__(other)

  def __sub__(self, other: SignedDuration | Duration) -> SignedDuration:
    match other:
      case Duration(ns=other_ns) | PositiveDuration(Duration(ns=other_ns)):
        return SignedDuration.from_nanos(self.absolute_value.ns - other_ns)
      case NegativeDuration(Duration(ns=other_negative_ns)):
        return SignedDuration.from_nanos(self.absolute_value.ns + other_negative_ns)
    return NotImplemented

  def __rsub__(self, other: Duration) -> SignedDuration:
    if not isinstance(other, Duration):
      return NotImplemented
    return SignedDuration.from_nanos(other.ns - self.absolute_value.ns)

  def __le__(self, other: SignedDuration | Duration) -> bool:
    match other:
      case Duration(ns=other_ns) | PositiveDuration(Duration(ns=other_ns)):
        return self.absolute_value.ns <= other_ns
      case NegativeDuration(Duration(ns=other_negative_ns)):
        return self.absolute_value.ns <= -other_negative_ns
    return NotImplemented

  def __gt__(self, other: SignedDuration | Duration) -> bool:
    result = self.__le__(other)
    return NotImplemented if result is NotImplemented else not result

  def __lt__(self, other: SignedDuration | Duration) -> bool:
    match other:
      case Duration(ns=other_ns) | PositiveDuration(Duration(ns=other_ns)):
        return self.absolute_value.ns < other_ns
      case NegativeDuration(Duration(ns=other_negative_ns)):
        return self.absolute_value.ns < -other_negative_ns
    return NotImplemented

  def __ge__(self, other: SignedDuration | Duration) -> bool:
    result = self.__lt__(other)
    return NotImplemented if result is NotImplemented else not result


@final
class NegativeDuration(SignedDuration):
  def __repr__(self) -> str:
    return f"NegativeDuration({self.absolute_value!r})"

  @classmethod
  def from_nanos(cls, _value: int) -> SignedDuration:
    msg = "Calling NegativeDuration.from_nanos is not supported. Call SignedDuration.from_nanos instead."
    raise TypeError(msg)

  @classmethod
  def from_micros(cls, _value: int) -> SignedDuration:
    msg = "Calling NegativeDuration.from_micros is not supported. Call SignedDuration.from_micros instead."
    raise TypeError(msg)

  @classmethod
  def from_millis(cls, _value: int) -> SignedDuration:
    msg = "Calling NegativeDuration.from_millis is not supported. Call SignedDuration.from_millis instead."
    raise TypeError(msg)

  @classmethod
  def from_seconds(cls, _value: int) -> SignedDuration:
    msg = "Calling NegativeDuration.from_seconds is not supported. Call SignedDuration.from_seconds instead."
    raise TypeError(msg)

  def to_timedelta(self) -> datetime.timedelta:
    return datetime.timedelta(microseconds=-self.absolute_value.to_micros())

  def __add__(self, other: SignedDuration | Duration) -> SignedDuration:
    match other:
      case Duration(ns=other_ns) | PositiveDuration(Duration(ns=other_ns)):
        return SignedDuration.from_nanos(-self.absolute_value.ns + other_ns)
      case NegativeDuration(Duration(ns=other_negative_ns)):
        return SignedDuration.from_nanos(-self.absolute_value.ns - other_negative_ns)
    return NotImplemented

  def __radd__(self, other: Duration) -> SignedDuration:
    return self.__add__(other)

  def __sub__(self, other: SignedDuration | Duration) -> SignedDuration:
    match other:
      case Duration(ns=other_ns) | PositiveDuration(Duration(ns=other_ns)):
        return SignedDuration.from_nanos(-self.absolute_value.ns - other_ns)
      case NegativeDuration(Duration(ns=other_negative_ns)):
        return SignedDuration.from_nanos(-self.absolute_value.ns + other_negative_ns)
    return NotImplemented

  def __rsub__(self, other: Duration) -> SignedDuration:
    if not isinstance(other, Duration):
      return NotImplemented
    return SignedDuration.from_nanos(other.ns + self.absolute_value.ns)

  def __le__(self, other: SignedDuration | Duration) -> bool:
    match other:
      case Duration(ns=other_ns) | PositiveDuration(Duration(ns=other_ns)):
        return -self.absolute_value.ns <= other_ns
      case NegativeDuration(Duration(ns=other_negative_ns)):
        return -self.absolute_value.ns <= -other_negative_ns
    return NotImplemented

  def __gt__(self, other: SignedDuration | Duration) -> bool:
    result = self.__le__(other)
    return NotImplemented if result is NotImplemented else not result

  def __lt__(self, other: SignedDuration | Duration) -> bool:
    match other:
      case Duration(ns=other_ns) | PositiveDuration(Duration(ns=other_ns)):
        return -self.absolute_value.ns < other_ns
      case NegativeDuration(Duration(ns=other_negative_ns)):
        return -self.absolute_value.ns < -other_negative_ns
    return NotImplemented

  def __ge__(self, other: SignedDuration | Duration) -> bool:
    result = self.__lt__(other)
    return NotImplemented if result is NotImplemented else not result


def hours(n: int) -> SignedDuration:
  """Create an instance of SignedDuration from integer amount of hours."""
  return SignedDuration.from_seconds(n * 3600)


def minutes(n: int) -> SignedDuration:
  """Create an instance of SignedDuration from integer amount of minutes."""
  return SignedDuration.from_seconds(n * 60)


def seconds(n: int) -> SignedDuration:
  """Create an instance of SignedDuration from integer amount of seconds."""
  return SignedDuration.from_seconds(n)


def milliseconds(n: int) -> SignedDuration:
  """Create an instance of SignedDuration from integer amount of milliseconds."""
  return SignedDuration.from_millis(n)


def microseconds(n: int) -> SignedDuration:
  """Create an instance of SignedDuration from integer amount of microseconds."""
  return SignedDuration.from_micros(n)


def nanoseconds(n: int) -> SignedDuration:
  """Create an instance of SignedDuration from integer amount of nanoseconds."""
  return SignedDuration.from_nanos(n)
