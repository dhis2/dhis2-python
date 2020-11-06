import json
import logging
import sys

import click
from dhis2.core.inventory import resolve_one
from dhis2.core.utils import load_and_parse_schema

from .icd11 import fetch_icd11_dhis2_option_sets
from .json_schema import generate_json_schema_metadata

log = logging.getLogger(__name__)


@click.group("generate")
def cli_generator():
    pass


@cli_generator.command("json_schemas")
@click.argument("host-id")
@click.pass_obj
def cmd_json_schemas(ctx, host_id: str):
    """ Generate JSON Schemas from a dhis2 instance """
    host = resolve_one(host_id, ctx.inventory)
    schemas = load_and_parse_schema(host)

    if schemas:
        click.echo(json.dumps(generate_json_schema_metadata(schemas), indent=2))


@cli_generator.command("icd11")
@click.argument("host-id")
@click.option("--linearizationname", default="mms")
@click.option("--release-id", default="2020-09")
@click.option("--language", default="en")
@click.option("--root-id", required=True)
@click.pass_obj
def cmd_icd11(
    ctx,
    host_id: str,
    linearizationname: str,
    release_id: str,
    language: str,
    root_id: str,
):
    """ Generate dhis2 option sets from icd11 source """
    host = resolve_one(host_id, ctx.inventory)

    if not "icd11" == host.type:
        log.error(f"Invalid source type '{host.type}', only 'icd11' sources are allowed")
        sys.exit(-1)

    option_sets = fetch_icd11_dhis2_option_sets(
        host,
        linearizationname=linearizationname,
        release_id=release_id,
        language=language,
        root_id=root_id,
    )

    if option_sets:
        click.echo(json.dumps(option_sets, indent=2))


def register_cli(cli):
    cli.add_command(cli_generator)
