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

import re
from pathlib import Path
from typing import Tuple, Set, List, Dict
from xml.etree import ElementTree as ET

import click
import requests

from dvcli.util import logger


def validate_dataset_url(ctx: click.Context, param: click.Parameter, value: str) -> Tuple[str, str]:
    """Validate the URL to the target dataset, extract PID and Dataverse FQDN"""

    logger.debug("Dataset URL: " + value)

    match = re.search(r'^(https?://.+)/dataset.xhtml\\?\?persistentId\\?=([a-z]+:.+?)(&.+)?$', value)
    if match:
        return match.group(1), match.group(2)
    else:
        raise click.BadParameter('Invalid dataset URL')


def find_files_in_dir(dir: Path, filter: Set[str] = (), recurse: bool = True) -> List[Path]:
    """Find files in a given directory and filter by glob patterns. Recursive by default."""

    files = list()

    # If path exists, is a dir and is not filtered, operate on content.
    if dir.exists() and dir.is_dir() and (dir.name not in filter) and (not any(map(lambda f: dir.match(f), filter))):
        # Iterate content of dir
        for entry in dir.glob("*"):
            # filter entries by name and glob patterns
            if (entry.name in filter) or any(map(lambda f: entry.match(f), filter)):
                continue
            # files simple get added to the list
            if entry.is_file():
                files.append(entry)
            # directories get search when recursion is enabled and results added to the files list
            if entry.is_dir() and recurse:
                files.extend(find_files_in_dir(entry, filter, recurse))

    # Might be empty if dir was not operated on
    return files


def remove_files_from_dataset(host: str, token: str, files: List[Dict]) -> bool:
    """Remove a list of files, referenced by their internal ID number via SWORD API"""

    # Using SWORD API to delete file, as no Native API available
    delete_api_prefix = host + "/dvn/api/data-deposit/v1.1/swordv2/edit-media/file/"

    # Prepare the XML parser to read the sword responses
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    ET.register_namespace("", ns["atom"])

    # Iterate all the file ids and delete them, print nice progress bar
    # Will keep going, as the unsuccessful deletion doesn't do much - we will save the error state for the
    # calling method
    responses = list()
    with click.progressbar(files, label="Deleting {} files".format(len(files))) as bar:
        for file in bar:
            resp = requests.delete(delete_api_prefix + str(file["id"]), auth=(token, ""))

            # When not successful, format message and log full to debug
            if resp.status_code >= 400:
                logger.debug("Status code: " + str(resp.status_code))
                logger.debug(resp.text)

                msg = file["directoryLabel"] + "/" if "directoryLabel" in file else ""
                msg += file["filename"] + ": "
                msg += ET.fromstring(resp.text).find("atom:summary", namespaces=ns).text
                responses.append(msg)

    # In case of errors, print log messages and return false
    if len(responses):
        for resp in responses:
            logger.error(resp)
        return False

    return True
