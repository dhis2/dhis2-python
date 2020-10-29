import os

import click
import dhis2.openhie.cli as cli_openhie
from pkg_resources import iter_entry_points

from .inspect import inspect
from .inventory import Inventory, parse_file, parse_obj, resolve, resolve_one
from .utils import load_and_parse_schema

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
@click.option("-i", "--inventory")
@click.option("-d", "--debug", is_flag=True)
@click.pass_context
def cli(ctx, inventory, debug):
    ctx.obj = CliContext(inventory, debug)


@cli.command("inspect")
@click.argument("id")
@click.pass_obj
def cmd_inspect(ctx, id):
    hosts = resolve(id, ctx.inventory)
    inspect(hosts)


@cli.command("schemas")
@click.argument("id")
@click.pass_obj
def cmd_schemas(ctx, id):  # TODO remove me, probably of no real use for anyone
    """ Load and parse dhis2 schema endpoint """
    host = resolve_one(id, ctx.inventory)
    schemas = load_and_parse_schema(host)

    if schemas:
        click.echo(schemas.json(indent=2))


@cli.group("inventory")
def cli_inventory():
    pass


@cli_inventory.command("schema")
def cmd_inventory_schema():
    click.echo(Inventory.schema_json(indent=2))


@cli_inventory.command("resolve-id")
@click.argument("id")
@click.pass_obj
def cmd_inventory_resolve(ctx, id):
    hosts = resolve(id, ctx.inventory)

    for host in hosts:
        print(host.json())


cli_openhie.register_cli(cli)  # register "fhir" plugin

# register additional plugins
for entry_point in iter_entry_points(group="dhis2.plugin", name=None):
    entry_point.load()(cli)  # check for valid function
