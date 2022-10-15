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

import pathlib
from typing import Tuple

import click
from pyDataverse.api import NativeApi
from pyDataverse.models import Datafile
from pyDataverse.exceptions import DataverseError

from dvcli.cli import logger
from dvcli.util import api_token_option, verbosity_option
from .util import validate_dataset_url, find_files_in_dir, remove_files_from_dataset


@click.group()
@click.pass_context
def upload(ctx):
    """
    Basic upload tasks.
    """
    # ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)


@upload.command(name="via-api")
@click.pass_context
#
@api_token_option(required=True)
@click.option("--purge", "-P", help="Purge files from dataset before uploading new files.", is_flag=True,
              envvar="DATAVERSE_PURGE", show_envvar=True)
@click.option("--ignore", "-i", help="Globbing pattern of files and folders to ignore. Repeatable.",
              multiple=True, envvar="DATAVERSE_IGNORE", show_envvar=True)
@click.option("--ignorefile", "-I", help="Path to file with glob patterns of files and directories to ignore.",
              default=".dvignore", envvar="DATAVERSE_IGNORE_FILE", show_envvar=True,
              type=click.Path(allow_dash=False, path_type=pathlib.Path))
@click.option("--non-recursive", "-R", help="Do not scan subdirectories.", is_flag=True)
@verbosity_option
#
@click.argument("path", nargs=1,
                type=click.Path(exists=True, readable=True,
                                allow_dash=False, path_type=pathlib.Path))
@click.argument("dataset_url", nargs=1, callback=validate_dataset_url)
def via_api(ctx: click.Context,
            api_token: str, purge: bool, ignore: Tuple[str], ignorefile: pathlib.Path, non_recursive: bool,
            path: pathlib.Path, dataset_url: Tuple[str, str]) -> None:
    """
    Upload local files and folders via the Dataverse Files API.

    *PATH* expresses as relative or absolute path a source directory (or file). A source directory will be scanned
    for deposit-able files recursively by default.
    Examples: "." or "data/" or "/abs/path/to/dir"

    *DATASET_URL* is an HTTP/S URL to a Dataverse dataset to deposit into.
    Example: "https://data.example.org/dataset.xhtml?persistentId=doi:..."

    Remember to enclose paths and URLs in quotes to avoid shell conflicts.
    """

    logger.debug("Source: " + click.format_filename(path))

    # Read ignorefile if exists via pathlib and add to set of patterns
    ignore = set(ignore)
    if ignorefile.exists():
        lines = ignorefile.read_text().splitlines()
        patterns = set(filter(lambda l: (not l.startswith('#') and not l.isspace()), lines))
        ignore.update(patterns)

    logger.debug("Provided ignore patterns: " + str(ignore))
    logger.info("Scanning '{}'...".format(click.format_filename(path)))

    files = list()
    # Search for files in a directory source - note: if symlink, resolve first
    if path.resolve().is_dir():
        files.extend(find_files_in_dir(path, filter=ignore, recurse=(not non_recursive)))
    elif path.resolve().is_file():
        files.append(path)

    logger.info("Found {} files.".format(len(files)))
    for (idx, f) in enumerate(files):
        logger.debug("{}: ".format(idx) + click.format_filename(f))

    # Retrieve the parsed & validated target data
    (host, datasetPid) = dataset_url

    logger.debug("Host: " + host)
    logger.debug("Dataset PID: " + datasetPid)
    # logger.debug("API Token: " + api_token) - should not be printed for security reasons

    logger.info("Verifying API connection with " + host + ".")
    api = None
    dataset_files = list()

    # Create an API object to interact with (plus verify URL and API token work and the dataset can be accessed)
    try:
        api = NativeApi(host, api_token)

        # Retrieve all json objects (dict) of files present in the dataset, so they can be purged
        for file_json in api.get_datafiles_metadata(datasetPid).json()["data"]:
            dataset_files.append(file_json["dataFile"])
    except DataverseError as dve:
        logger.error(dve)
        ctx.exit(10)

    # Purge files before upload when requested
    if purge:
        # TODO: add dry-run option
        if not remove_files_from_dataset(host, api_token, dataset_files):
            # When deletion failed, exit now.
            ctx.exit(10)

    # Iterate all the files and upload them, print nice progress bar
    with click.progressbar(files, label="Uploading {} files".format(len(files))) as bar:
        for file in bar:
            df = Datafile()
            df.set({
                "pid": datasetPid,
                "filename": click.format_filename(file.name),
                "directoryLabel": click.format_filename(file.parent),
                "description": "Uploaded with dvcli."
            })
            logger.debug(df.json())

            # TODO: add dry-run option, skipping the actual upload & dataset lock check
            api.upload_datafile(datasetPid, file.resolve(), df.json())
            # TODO: add check for response status, catch exceptions, print errors
            # TODO: check for dataset lock to prevent some timing errors

    # TODO: publish when the user wants it (option!)
    #       how does this API behave with regards to "submitting" when not having permission to publish?
