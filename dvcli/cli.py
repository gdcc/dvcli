from pkg_resources import iter_entry_points

import click
import click_log
import confuse
import sys
import os
import logging
from click_plugins import with_plugins

# Importing commands from submodules
import dvcli.user.cli as user_group

# Global variables
configuration = confuse.LazyConfig('dvcli', __name__)
logger = logging.getLogger(__name__)

# Logging config
click_log.basic_config(logger)
verbosity = {0: logging.ERROR, 1: logging.WARN, 2: logging.INFO, 3: logging.DEBUG}


@with_plugins(iter_entry_points('dvcli.plugins'))
@click.group()
@click.option('--config', '-c',
              help='Custom path to config. Trying ' + configuration.user_config_path() + ' by default.',
              type=click.Path())
@click.option('--verbose', '-v', count=True, help="Increase verbosity. -v = WARN, -vv = INFO, -vvv = DEBUG")
@click.option('--quiet', '-q', default=False, is_flag=True, help="Print no logs, not even errors.")
def cli(config, verbose, quiet):
    """
    Dataverse Command Line Interface.

    Use and manage a Dataverse installation from your terminal.
    """

    if verbose > 0 and quiet:
        logger.critical('Cannot use --quiet and --verbose at the same time.')
        sys.exit(10)
    # Get verbosity level from mapping, default to DEBUG if given more than 3 times
    logger.setLevel(verbosity.get(verbose, logging.DEBUG))
    # Forcing quiet if given
    if quiet:
        logger.setLevel(logging.CRITICAL)

    # Load config file from cmdline as config source at highest priority
    # (and load it at once - no more lazy...)
    if config is not None:
        try:
            configuration.set_file(config)
        except confuse.ConfigReadError:
            logger.error('Could not read configuration file (' + os.path.abspath(config) + ')')
            sys.exit(10)

    # pass other args from cmdline to configuration
    # example: configuration.set_args({'url': url})


def main():
    """
    Start the cli interface.
    This function is called from the entrypoint script installed by setuptools.
    It enables using environment variables like DVCLI_CONFIG as options.
    """
    user_group.register(cli)
    cli(auto_envvar_prefix='DVCLI')


# Allow running this file as standalone app without setuptools wrappers
if __name__ == '__main__':
    main()
