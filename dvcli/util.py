"""
(C) Copyright 2020 Forschungszentrum Jülich GmbH and others.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import logging
from typing import Callable, Any

import click

from dvcli.cli import logger

verbosity = {0: logging.ERROR, 1: logging.WARN, 2: logging.INFO, 3: logging.DEBUG}


def _set_verbosity(ctx: click.Context, param: click.Parameter, value: Any) -> None:
    """Validate and set the logging level"""
    if not value:
        return
    # Get verbosity level from mapping, default to DEBUG if given more than 3 times
    logger.setLevel(verbosity.get(value, logging.DEBUG))


def verbosity_option(f: Callable) -> Callable:
    """
    Reusable verbosity option
    """
    return click.option('--verbose', '-v', help="Increase verbosity. -v = WARN, -vv = INFO, -vvv = DEBUG",
                        default=0, count=True, expose_value=False, callback=_set_verbosity, is_eager=True)(f)
