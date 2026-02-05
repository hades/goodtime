Welcome to **goodtime**, a Python date/time library that prioritises safety and correctness.

```python
>>> from goodtime import *
>>> Instant.now()
Instant(unix_timestamp_ns=1770029789026987530)
>>> Instant.now() + hours(1)
Instant(unix_timestamp_ns=1770033404038049963)
>>> Instant.now().to_unix_seconds()
1770029824
>>> Instant.from_unix_seconds(1770029824)
Instant(unix_timestamp_ns=1770029824000000000)
```

Handling of timestamps, durations and human-readable dates and times is
notoriously error-prone due to issues with time zones, ambiguous arithmetic,
ambiguous units, etc. This is especially true in distributed systems, where
interacting systems may be written by multiple teams that did not have shared
assumptions about date/time semantics.

The goal of **goodtime** is to minimise the potential for errors by:

* using types that have well-defined semantics,
* preventing ambiguous conversions (e.g. timestamp to integer),
* providing explicit interfaces to interoperate with non-goodtime code.

See package documentation for more information on provided types, operations,
and best practices.

## Getting Started

Install **goodtime** from PyPI using your favourite Python package manager:

```console
$ python -m pip install goodtime
$ poetry add goodtime
$ uv add goodtime
```

## Contributing

We are open to feedback and contributions under the terms of the MIT license.
Feel free to open a Github issue or a pull request.
