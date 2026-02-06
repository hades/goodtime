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

Converting between the two requires the knowledge of the time zone where a civil
time is observed. Time zones (represented with the Timezone type) are
geographical/political areas that share the same mapping of absolute time to
civil time. Time zone is not merely an offset from UTC, but also includes the
temporary offsets based on rules (such as daylight saving time) set by the local
civil authorities.

Truncation
----------

Operations that truncate the precision of values (e.g. Instant.to_unix_seconds
or Duration.to_seconds) will round towards infinite past or negative infinite
duration.

Leap seconds
------------

As practically any date/time library, **goodtime** has absolutely no support for
leap seconds. This means that certain real civil time (such as
2016-12-31T23:59:60) can't be represented with the types provided by this library.
Further, any duration computation for time spans that include leap seconds will
return imprecise results.

If you need to account for leap seconds in your computation, you may want to use
the TIA time zone, however, there is no proper support for it in this library
(yet).

Dates in far future or far past
-------------------------------

Global agreement on time measurement has been established relatively recently.
Time zone information is provided for dates after around 1970, any time zone
conversions before that may not be correct in the corresponding locations.

Gregorian calendar itself has been adopted at different times throughout the
world. Some countries had very tumultous transitions, making correct mapping of
civil time close to impossible.

For dates before Gregorian calendar, the tradition to use Proleptic Gregorian
calendar (which is completely fictitious) is upheld.

Dates before common era are represented with zero-based negative year numbers
(i.e. year 0 is 1 BCE, year -1 is 2 BCE, etc.).

Time zone rules are subject to change, which makes any computation of civil time
in the future liable to become incorrect at some point. While many civilised
countries exercise common courtesy to give the world time to prepare for rule
changes, there have been cases in the past when time zone rules have been
altered with less than a week's notice.

Further, due to the way time zone databases work, information on temporary time
zone offsets (such as daylight saving time) may only be available for 30-40
years in the future.
"""

__version__ = "0.4.1"

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
