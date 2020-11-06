import logging

import click
from dhis2.core.utils import parse_file

from . import mcsd

log = logging.getLogger(__name__)


@click.group("facility-list")
def cli_facility_list():
    """ Various commands for facility-list data exchange """
    pass


@cli_facility_list.command("mcsd")
@click.argument("config")
@click.option("--last-updated")
@click.pass_obj
def cmd_openhie_mcsd(ctx, config: str, last_updated: str):
    """ OpenHIE Mobile Care Services Discovery (mCSD) """
    mcsd_config = {
        "source": {},
        "target": {
            "id": "log://",
        },
    }

    config_dict = parse_file(config)

    if not config_dict:
        log.error(f"Invalid SVCM config file '{config}'")
        return

    mcsd_config.update(config_dict)

    if last_updated:
        mcsd_config["source"]["lastUpdated"] = last_updated

    mcsd.run(mcsd.MCSDConfig(**mcsd_config), ctx.inventory)


def register_cli(cli):
    cli.add_command(cli_facility_list)
