# Correctly configure ArduPilot for your vehicles on your first attempt

<!--
SPDX-FileCopyrightText: 2024-2025 Amilcar do Carmo Lucas <amilcar.lucas@iav.de>

SPDX-License-Identifier: GPL-3.0-or-later
-->

| Lint | Quality | Test | Deploy | Maintain |
| ---- | ------- | ---- | ------ | -------- |
| [![Pylint](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/pylint.yml/badge.svg)](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/pylint.yml) | [![Codacy Badge](https://app.codacy.com/project/badge/Grade/720794ed54014c58b9eaf7a097a4e98e)](https://app.codacy.com/gh/amilcarlucas/MethodicConfigurator/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade) | [![Python unit-tests](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/unit-tests.yml) | [![pages-build-deployment](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/pages/pages-build-deployment) | [![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/ArduPilot/MethodicConfigurator.svg)](http://isitmaintained.com/project/ArduPilot/MethodicConfigurator) |
| [![test Python cleanliness](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/ruff.yml/badge.svg)](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/ruff.yml) | [![OpenSSF Best Practices](https://www.bestpractices.dev/projects/9101/badge)](https://www.bestpractices.dev/projects/9101) | [![Pytest unittests](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/pytest.yml/badge.svg)](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/pytest.yml) | [![Upload MethodicConfigurator Package](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/python-publish.yml/badge.svg)](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/python-publish.yml) | [![Percentage of issues still open](http://isitmaintained.com/badge/open/ArduPilot/MethodicConfigurator.svg)](http://isitmaintained.com/project/ArduPilot/MethodicConfigurator) |
| [![mypy](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/mypy.yml/badge.svg)](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/mypy.yml) | [![Known Vulnerabilities](https://snyk.io/test/github/amilcarlucas/MethodicConfigurator/badge.svg)](https://app.snyk.io/org/amilcarlucas/project/c8fd6e29-715b-4949-b828-64eff84f5fe1) | [![codecov](https://codecov.io/github/amilcarlucas/MethodicConfigurator/graph/badge.svg?token=76P928EOL2)](https://codecov.io/github/amilcarlucas/MethodicConfigurator) | [![Windows Build](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/windows_build.yml/badge.svg)](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/windows_build.yml) | |
| [![markdown](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/markdown-lint.yml) | [![Code Climate](https://codeclimate.com/github/amilcarlucas/MethodicConfigurator.png)](https://codeclimate.com/github/amilcarlucas/MethodicConfigurator) | [![Coverity Scan Build Status](https://scan.coverity.com/projects/30346/badge.svg)](https://scan.coverity.com/projects/ardupilot-methodic-configurator) | | |
| [![md-link-check](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/markdown-link-check.yml/badge.svg)](https://github.com/ArduPilot/MethodicConfigurator/actions/workflows/markdown-link-check.yml) | | | | |

*ArduPilot Methodic Configurator* is a software, developed by ArduPilot developers, that semi-automates a
[clear, proven and safe configuration sequence](https://ardupilot.github.io/MethodicConfigurator/TUNING_GUIDE_ArduCopter) for ArduCopter drones.
We are working on extending it to [ArduPlane](https://ardupilot.github.io/MethodicConfigurator/TUNING_GUIDE_ArduPlane),
[Heli](https://ardupilot.github.io/MethodicConfigurator/TUNING_GUIDE_Heli) and
[Rover](https://ardupilot.github.io/MethodicConfigurator/TUNING_GUIDE_Rover) vehicles.
But for those it is still very incomplete.

- **clear**: the sequence is linear, executed one step at the time with no hidden complex dependencies
- **proven**: the software has been used by hundreds of ArduPilot developers and users. From beginners to advanced. On big and small vehicles.
- **safe**: the sequence reduces trial-and-error and reduces the amount of flights required to configure the vehicle

Let's compare it with the traditional tool used to configure ArduPilot: a generalistic Ground Control Station (GCS) software.

| Feature | Mission Planner, QGroundControl, ... etc | ArduPilot Methodic Configurator |
| ------- | ---------------------------------------- | ------------------------------- |
| configuration type | manual [^1]  | semi-automated [^2] |
| explains what to do | :-1: | :+1:  |
| explains when to do something | :-1: leaves you lost | :+1: explains the path |
| explains why do something | :-1: | :+1: |
| configuration method | a different menu for each task, some taks have no menu, so you need to dig into the 1200 parameters | each task only presents you a relevant subset of parameters |
| parameter documentation | :+1: only on the full-parameter tree view | :+1: |
| displays relevant documentation | :-1: | :+1: |
| makes sure you do not forget a step | :-1: | :+1: |
| checks that parameters get correctly uploaded | :-1: | :+1: |
| reuse params in other vehicles | :-1: unless you hand edit files | :+1: out-of-the-box |
| documents why you changed each parameter | :-1: | :+1: |

[^1]: you need to know what/when/why you are doing
[^2]: it explains what you should do, when you should do it and why

![When to use ArduPilot Methodic Configurator](https://github.com/ArduPilot/MethodicConfigurator/blob/master/images/when_to_use_amc.png?raw=true)

It's graphical user interface (GUI) manages and visualizes ArduPilot parameters, parameter files and documentation.

![Application Screenshot](https://github.com/ArduPilot/MethodicConfigurator/blob/master/images/App_screenshot1.png?raw=true)

## Usage

There is a [Quick-start guide](https://ardupilot.github.io/MethodicConfigurator/QUICKSTART.html) and a more detailed [Usermanual](https://ardupilot.github.io/MethodicConfigurator/USERMANUAL.html).
Most [common usecases are also documented in detail](https://ardupilot.github.io/MethodicConfigurator/USECASES.html).

## Install

See the [install instructions](https://ardupilot.github.io/MethodicConfigurator/INSTALL.html)

## Support

Need [help or support](https://ardupilot.github.io/MethodicConfigurator/SUPPORT.html)

## Contributing

Want [to help us and contribute](https://github.com/ArduPilot/MethodicConfigurator/blob/master/CONTRIBUTING.md)?

## Software design and development

To meet the [Software requirements](https://ardupilot.github.io/MethodicConfigurator/ARCHITECTURE.html#software-requirements) a
[software architecture](https://ardupilot.github.io/MethodicConfigurator/ARCHITECTURE.html#the-software-architecture) was designed and implemented.

## Code of conduct

To use and develop this software you must obey the [ArduPilot Methodic Configurator Code of Conduct](https://github.com/ArduPilot/MethodicConfigurator/blob/master/CODE_OF_CONDUCT.md).

## License

This software is cost free.
This project is licensed under the [GNU General Public License v3.0](https://github.com/ArduPilot/MethodicConfigurator/blob/master/LICENSE.md).

## Credits

It builds upon other [open-source software packages](https://ardupilot.github.io/MethodicConfigurator/credits/CREDITS.html)
