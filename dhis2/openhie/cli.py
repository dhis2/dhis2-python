import logging

import click
import dhis2.openhie.mcsd as mcsd
import dhis2.openhie.svcm as svcm
from dhis2.core.utils import parse_file

log = logging.getLogger(__name__)


@click.group("openhie")
def cli_openhie():
    pass


@cli_openhie.command("mcsd")
@click.argument("config")
@click.pass_obj
def cmd_openhie_mcsd(ctx, config: str):
    """ Mobile Care Services Discovery (mCSD) """
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
    mcsd.run(mcsd.MCSDConfig(**mcsd_config), ctx.inventory)


@cli_openhie.command("svcm")
@click.argument("config")
@click.pass_obj
def cmd_openhie_svcm(ctx, config: str):
    """ Sharing Valuesets, Codes, and Maps (SVCM) """
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
    svcm.run(svcm.SVCMConfig(**svcm_config), ctx.inventory)


def register_cli(cli):
    cli.add_command(cli_openhie)
