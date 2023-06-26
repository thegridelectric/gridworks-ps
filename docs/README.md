# Gridworks Price Service

[![PyPI](https://img.shields.io/pypi/v/gridworks-atn.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/gridworks-atn.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/gridworks-atn)][python version]
[![License](https://img.shields.io/pypi/l/gridworks-atn)][license]

[![Read the documentation at https://gridworks-atn.readthedocs.io/](https://img.shields.io/readthedocs/gridworks/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/thegridelectric/gridworks-atn/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/thegridelectric/gridworks-atn/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/gridworks-atn/
[status]: https://pypi.org/project/gridworks-atn/
[python version]: https://pypi.org/project/gridworks-atn
[read the docs]: https://gridworks-atn.readthedocs.io/
[tests]: https://github.com/thegridelectric/gridworks-atn/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/thegridelectric/gridworks-atn
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

This is the [GridWorks](https://gridworks.readthedocs.io/) repository for a simple open-source
[PriceService](https://gridworks.readthedocs.io/en/latest/price-service.html) - that is, a service
for providing forecasts for various electricity markets. This includes wholesale markets for electrical
energy and ancillary services run by grid operators like [Iso-ne](https://www.iso-ne.com/isoexpress/web/charts) (The US New England
grid operator) and [Miso](https://www.misoenergy.org/markets-and-operations/real-time--market-data/markets-displays/)
(The US MidWest grid operator). As GridWorks [MarketMakers](https://gridworks.readthedocs.io/en/latest/market-maker.html)
begin providing market clearing for lower voltage constraints, this repo will also provide a some simple
template forecasting mechanisms for these new markets.

To explore the rest of GridWorks, visit the [GridWorks docs](https://gridworks.readthedocs.io/en/latest/).

## License

Distributed under the terms of the [MIT license][license],
**Gridworks Atn** is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/thegridelectric/gridworks-atn/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/thegridelectric/gridworks-atn/blob/main/LICENSE
[contributor guide]: https://github.com/thegridelectric/gridworks-atn/blob/main/CONTRIBUTING.md
[command-line reference]: https://gridworks-atn.readthedocs.io/en/latest/usage.html
