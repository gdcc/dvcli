import sys
import os
import logging
from importlib import metadata

import click
import click_log
import confuse

# Global variables
configuration = confuse.LazyConfig('dvcli', __name__)
logger = logging.getLogger(__name__)

# Logging config
click_log.basic_config(logger)


@click.group()
@click.option('--config', '-c',
              help='Custom path to config. Trying ' + configuration.user_config_path() + ' by default.',
              type=click.Path())
def cli(config):
    """
    Dataverse Command Line Interface.

    Use and manage a Dataverse installation from your terminal.
    """

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
    This function is called from the entrypoint script installed by poetry.
    It enables using environment variables like DVCLI_CONFIG as options.
    """

    # Find all plugins and register from the entrypoint group
    for group in metadata.entry_points()["dvcli.plugins"]:
        # Load function from entrypoint
        function = group.load()
        # Execute function with the main CLI group parameter
        function(cli)

    # Invoke CLI
    cli(auto_envvar_prefix='DVCLI')


# Allow running this file as standalone app without setuptools wrappers
if __name__ == '__main__':
    main()
