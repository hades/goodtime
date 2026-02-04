"""Instants represent fixed points in time."""

import dataclasses
import time
from typing import final, overload

from ._duration import Duration, NegativeDuration, PositiveDuration, SignedDuration


@final
@dataclasses.dataclass(init=False, repr=True, order=True, frozen=True, slots=True)
class Instant:
  """Instant represents a specific absolute instant in time on Earth.

  Values can be created using the now() function or the factory functions
  (from_unix_nanos, from_unix_micros, from_unix_millis, from_unix_seconds).

  Instant has absolutely no understanding of leap seconds. If your system does
  not implement leap second smearing, you may encounter "jumps" or "skips" in
  the value of Instant that can lead to errors. Additionally, calculating the
  length of time between two Instants does not represent the real physical
  amount of time passed whenever leap seconds have been inserted or removed.

  It is recommended to use the values of Instant type everywhere in your code,
  including fields and function signatures. Use explicit conversion functions at
  the boundary of your code to interoperate with non-goodtime libraries and
  APIs.
  """

  unix_timestamp_ns: int

  def __init__(self, *, unix_timestamp_ns: int):
    """Construct a value of Instant from UNIX timestamp in nanoseconds.

    For readability it is recommended to use the explicit factory functions
    (from_unix_nanos, from_unix_micros, from_unix_millis, from_unix_seconds)
    instead.
    """
    if not isinstance(unix_timestamp_ns, int):
      msg = f"unix_timestamp_ns must be int, was {type(unix_timestamp_ns)}"
      raise TypeError(msg)
    object.__setattr__(self, "unix_timestamp_ns", unix_timestamp_ns)

  @classmethod
  def from_unix_nanos(cls, value: int) -> "Instant":
    """Create an Instant value from UNIX timestamp in nanoseconds."""
    return cls(unix_timestamp_ns=value)

  @classmethod
  def from_unix_micros(cls, value: int) -> "Instant":
    """Create an Instant value from UNIX timestamp in microseconds."""
    return cls(unix_timestamp_ns=value * 1000)

  @classmethod
  def from_unix_millis(cls, value: int) -> "Instant":
    """Create an Instant value from UNIX timestamp in milliseconds."""
    return cls(unix_timestamp_ns=value * 1_000_000)

  @classmethod
  def from_unix_seconds(cls, value: int) -> "Instant":
    """Create an Instant value from UNIX timestamp in seconds."""
    return cls(unix_timestamp_ns=value * 1_000_000_000)

  @classmethod
  def now(cls) -> "Instant":
    """Create an Instant representing the current time."""
    return cls(unix_timestamp_ns=time.time_ns())

  def to_unix_nanos(self) -> int:
    """Return the value of this Instant as UNIX timestamp in nanoseconds."""
    return self.unix_timestamp_ns

  def to_unix_micros(self) -> int:
    """Return the value of this Instant as UNIX timestamp in microseconds, rounding towards infinite past."""
    return self.unix_timestamp_ns // 1000

  def to_unix_millis(self) -> int:
    """Return the value of this Instant as UNIX timestamp in milliseconds, rounding towards infinite past."""
    return self.unix_timestamp_ns // 1_000_000

  def to_unix_seconds(self) -> int:
    """Return the value of this Instant as UNIX timestamp in seconds, rounding towards infinite past."""
    return self.unix_timestamp_ns // 1_000_000_000

  def __add__(self, other: Duration | SignedDuration) -> "Instant":
    match other:
      case Duration(ns=delta) | PositiveDuration(Duration(ns=delta)):
        return Instant.from_unix_nanos(self.unix_timestamp_ns + delta)
      case NegativeDuration(Duration(ns=negative_delta)):
        return Instant.from_unix_nanos(self.unix_timestamp_ns - negative_delta)
    return NotImplemented

  def __radd__(self, other: Duration | SignedDuration) -> "Instant":
    return self.__add__(other)

  @overload
  def __sub__(self, other: "Instant") -> SignedDuration: ...

  @overload
  def __sub__(self, other: Duration | SignedDuration) -> "Instant": ...

  def __sub__(self, other: "Instant|Duration|SignedDuration") -> "Instant|SignedDuration":
    match other:
      case Duration(ns=delta) | PositiveDuration(Duration(ns=delta)):
        return Instant.from_unix_nanos(self.unix_timestamp_ns - delta)
      case NegativeDuration(Duration(ns=negative_delta)):
        return Instant.from_unix_nanos(self.unix_timestamp_ns + negative_delta)
      case Instant(unix_timestamp_ns=other_timestamp_ns):
        return SignedDuration.from_nanos(self.unix_timestamp_ns - other_timestamp_ns)
    return NotImplemented
