import json
import logging
import sys

import click
from dhis2.core.inventory import resolve_one
from dhis2.core.utils import parse_file

from . import svcm
from .icd11 import fetch_icd11_dhis2_option_sets
from .icd10 import fetch_icd10_dhis2_option_sets

log = logging.getLogger(__name__)


@click.group("code-list")
def cli_code_list():
    """ Various commands for code-list data exchange """
    pass


@cli_code_list.command("icd11")
@click.argument("host-id")
@click.option("--linearizationname", default="mms")
@click.option("--release-id", default="2020-09")
@click.option("--language", default="en")
@click.option("--root-id", required=True)
@click.pass_obj
def cmd_code_list_icd11(
    ctx,
    host_id: str,
    linearizationname: str,
    release_id: str,
    language: str,
    root_id: str,
):
    """ Generate dhis2 option sets from icd11 source **experimental** """
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


@cli_code_list.command("icd10")
@click.argument("host-id")
@click.option("--release-id", default="2016")
@click.option("--language", default="en")
@click.option("--root-id")
@click.pass_obj
def cmd_code_list_icd10(
    ctx,
    host_id: str,
    release_id: str,
    language: str,
    root_id: str,
):
    """ Generate dhis2 option sets from icd10 source **experimental** """
    host = resolve_one(host_id, ctx.inventory)

    if not "icd10" == host.type:
        log.error(f"Invalid source type '{host.type}', only 'icd10' sources are allowed")
        sys.exit(-1)

    option_sets = fetch_icd10_dhis2_option_sets(
        host,
        release_id=release_id,
        language=language,
        root_id=root_id,
    )

    if option_sets:
        click.echo(json.dumps(option_sets, indent=2))


@cli_code_list.command("svcm")
@click.argument("config")
@click.option("--last-updated")
@click.pass_obj
def cmd_openhie_svcm(ctx, config: str, last_updated: str):
    """ OpenHIE Sharing Valuesets, Codes, and Maps (SVCM) """
    svcm_config = {
        "source": {},
        "target": {
            "id": "log://",
        },
    }

    config_dict = parse_file(config)

    if not config_dict:
        log.error(f"Invalid SVCM config file '{config}'")
        return

    svcm_config.update(config_dict)

    if last_updated:
        svcm_config["source"]["lastUpdated"] = last_updated

    svcm.run(svcm.SVCMConfig(**svcm_config), ctx.inventory)


def register_cli(cli):
    cli.add_command(cli_code_list)
