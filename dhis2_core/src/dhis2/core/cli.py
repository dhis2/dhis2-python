import os

import click
import dhis2.code_list.cli as cli_code_list
import dhis2.facility_list.cli as cli_facility_list
import dhis2.generate.cli as cli_generator
import dhis2.e2b.cli as cli_e2b
from pkg_resources import iter_entry_points

from .inspect import inspect
from .inventory import Inventory, parse_file, parse_obj, resolve

defaultInventory = {"hosts": {}, "groups": {}}


class CliContext(object):
    def __init__(self, inventory=None, debug=False):
        if inventory:
            self.inventory: Inventory = parse_file(os.path.abspath(inventory))
        else:
            self.inventory: Inventory = parse_obj(defaultInventory)

        self.debug = debug


@click.group()
@click.version_option()
@click.option("-i", "--inventory", metavar="INVENTORY")
@click.option("-d", "--debug", is_flag=True)
@click.pass_context
def cli(ctx, inventory, debug):
    """ DHIS2 Tool for helping with import/export of various formats. """
    ctx.obj = CliContext(inventory, debug)


@cli.command("inspect")
@click.argument("id")
@click.pass_obj
def cmd_inspect(ctx, id):
    """ Display basic dhis2 instance information """
    hosts = resolve(id, ctx.inventory)
    inspect(hosts)


@cli.group("inventory")
def cli_inventory():
    """ Various commands for working with the inventory format """
    pass


@cli_inventory.command("schema")
def cmd_inventory_schema():
    """ Generate json schema for the inventory format """
    click.echo(Inventory.schema_json(indent=2))


@cli_inventory.command("resolve-id")
@click.argument("id")
@click.pass_obj
def cmd_inventory_resolve(ctx, id):
    """ Resolve and print a inventory dsn """
    hosts = resolve(id, ctx.inventory)

    for host in hosts:
        click.echo(host.json())


cli_code_list.register_cli(cli)  # register "code-list" plugin
cli_facility_list.register_cli(cli)  # register "facility-list" plugin
cli_generator.register_cli(cli)  # register "generator" plugin
cli_e2b.register_cli(cli)  # register "e2b" plugin

# register additional plugins
for entry_point in iter_entry_points(group="dhis2.plugin", name=None):
    entry_point.load()(cli)  # check for valid function
