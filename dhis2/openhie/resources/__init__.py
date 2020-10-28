import logging

import click
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
    config_file = parse_file(config)

    if not config_file:
        log.error(f"Invalid SVCM config file '{config}'")
        return

    print(ctx)
    print(config)


@cli_openhie.command("svcm")
@click.argument("config")
@click.pass_obj
def cmd_openhie_svcm(ctx, config: str):
    """ Sharing Valuesets, Codes, and Maps (SVCM) """
    config_file = parse_file(config)

    if not config_file:
        log.error(f"Invalid SVCM config file '{config}'")
        return

    print(ctx)
    print(config)


def register_cli(cli):
    cli.add_command(cli_openhie)
