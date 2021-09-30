from pkg_resources import iter_entry_points

import click
import confuse
import sys
import os
from click_plugins import with_plugins

# Importing commands from submodules
import dvcli.user.cli as user_group

configuration = confuse.LazyConfig('dvcli', __name__)


@with_plugins(iter_entry_points('dvcli.plugins'))
@click.group()
@click.option('--config',
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
            click.echo('Error: could not read configuration file (' + os.path.abspath(config) + '). Cowardly aborting.',
                       err=True)
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
