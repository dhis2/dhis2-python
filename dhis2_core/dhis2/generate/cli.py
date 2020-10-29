import json
import logging

import click
from dhis2.core.inventory import resolve_one
from dhis2.core.utils import load_and_parse_schema

from .json_schema import generate_json_schema_metadata

log = logging.getLogger(__name__)


@click.group("generate")
def cli_generator():
    pass


@cli_generator.command("json_schemas")
@click.argument("id")
@click.pass_obj
def cmd_json_schemas(ctx, id: str):
    """ Generate JSON Schemas from a dhis2 instance """
    host = resolve_one(id, ctx.inventory)
    schemas = load_and_parse_schema(host)

    if schemas:
        click.echo(json.dumps(generate_json_schema_metadata(schemas), indent=2))


def register_cli(cli):
    cli.add_command(cli_generator)
