#!/usr/bin/env python

from typing import Dict

import click
import dhis2.e2b.r2 as r2
from dhis2.core.http import BaseHttpRequest
from dhis2.core.inventory import HostResolved, resolve_one

from .models.e2b import AttributeValue, EventDataValue, TrackedEntity


def require_program(host: HostResolved, pr: str) -> None:
    request = BaseHttpRequest(host)
    request.get(f"api/programs/{pr}")


def get_aefi_patient(host: HostResolved, pr: str, te: str) -> TrackedEntity:
    require_program(host, pr)
    request = BaseHttpRequest(host)
    response = request.get(
        f"api/trackedEntityInstances/{te}",
        params={
            "fields": "*",
            "program": pr,
        },
    )

    te = TrackedEntity(**response)

    attributes: Dict[str, AttributeValue] = {}

    for av in te.attributes:
        attributes[av.attribute] = av

    for en in te.enrollments:
        for av in en.attributes:
            attributes[av.attribute] = av

        del en.attributes

        events = {}

        for ev in en.events:
            dataValues: Dict[str, EventDataValue] = {}

            for dv in ev.dataValues:
                dataValues[dv.dataElement] = dv

            events[ev.programStage] = ev
            ev.dataValues = dataValues

        en.events = events

    te.attributes = attributes

    return te


@click.command("e2b")
@click.argument("host-id")
@click.option("--country", default="unknown")
@click.option("--sender-id", default="unknown")
@click.option("--receiver-id", default="unknown")
@click.option("--tracked-entity", default="zAt1I8i6c83")
@click.pass_obj
def cmd_e2b(ctx, host_id: str, country: str, sender_id: str, receiver_id: str, tracked_entity: str):
    """ Individual Case Safety Reports E2B (R2) """
    host = resolve_one(host_id, ctx.inventory)
    te = get_aefi_patient(host, "EZkN8vYZwjR", tracked_entity)

    r2.run(
        [te],
        country=country,
        sender_id=sender_id,
        receiver_id=receiver_id,
    )


def register_cli(cli):
    cli.add_command(cmd_e2b)
