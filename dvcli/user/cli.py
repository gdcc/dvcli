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

from . import upload


# Handler to register our command group, called from main cli.
# DO NOT REMOVE (or command group will be unusable)
def register(cli):
    # cli.add_command(dataset.dataset) - not in use for now
    # cli.add_command(collection.collection) - not in use for now
    cli.add_command(upload.upload)
