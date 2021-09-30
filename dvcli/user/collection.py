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

import click


@click.group()
@click.pass_context
def collection(ctx):
    """
    Basic Dataverse collection tasks.
    """
    # ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)

# @collection.command(name="list-all")
# def list_all():
#    """
#    List all dataverse accessible to you.
#    """
