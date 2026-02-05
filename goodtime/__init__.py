"""A time library that prioritises clean and safe APIs.

Please read this documentation carefully to understand what **goodtime** types
and functions do, and how to prevent most common date/time errors.

The core types are Instant (representing a fixed absolute point in time on
Earth), Duration (representing a length of time) and CivilTime (representing
local time as used by humans).

Design
------

The first thing to understand about how **goodtime** handles time is that the
"absolute time" and "civil time" are explicitly treated as completely different
(and, generally-speaking, incompatible) concepts.

**Absolute time** (represented with the Instant type) is the underlying basis of
measurement of time, as currently agreed upon practically everywhere on Earth.
Any instantaneous event (keypress, rocket lift-off, log message) will have a
unique absolute time as defined by the International Telecommunication Union. It
is therefore very convenient to avoid ambiguity, and is commonly used in
computing, communications, aviation, etc.

**Civil time**, or **local time** is a measurement of time as regulated by
civilian authorities, and is a tuple of six fields: year, month, day, hour,
minute, second. The same tuple can have different meaning depending on the
jurisdiction where it is interpreted. As such, it is inconvenient for
communication and computing, but there is no way to avoid it, as most humans
understand their civil time much better than global absolute time, and mostly
use civil time to organise their life.

Truncation
----------

Operations that truncate the precision of values (e.g. Instant.to_unix_seconds
or Duration.to_seconds) will round towards infinite past or negative infinite
duration.
"""

__version__ = "0.4.0"

from ._civil_time import CivilSecond, CivilTime
from ._duration import (
  Duration,
  NegativeDuration,
  PositiveDuration,
  SignedDuration,
  hours,
  microseconds,
  milliseconds,
  minutes,
  nanoseconds,
  seconds,
)
from ._instant import Instant
from ._timezone import (
  CivilTimeInstant,
  RepeatedCivilTimeInstant,
  SkippedCivilTimeInstant,
  Timezone,
  UniqueCivilTimeInstant,
)

__all__ = [
  "CivilSecond",
  "CivilTime",
  "CivilTimeInstant",
  "Duration",
  "Instant",
  "NegativeDuration",
  "PositiveDuration",
  "RepeatedCivilTimeInstant",
  "SignedDuration",
  "SkippedCivilTimeInstant",
  "Timezone",
  "UniqueCivilTimeInstant",
  "hours",
  "microseconds",
  "milliseconds",
  "minutes",
  "nanoseconds",
  "seconds",
]
