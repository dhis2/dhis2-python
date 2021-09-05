import logging
from typing import List

from lxml.builder import E

from .e2b_resources import build_messageheader, build_safetyreport, print_root
from .models.e2b import TrackedEntity

log = logging.getLogger(__name__)


def run(
    tracked_entities: List[TrackedEntity],
    *,
    sender_id: str,
    receiver_id: str,
    country: str,
    receiverorganization: str,
    receivercountrycode: str,
):
    root = E.ichicsr(lang="en")
    build_messageheader(root, sender_id, receiver_id)

    for te in tracked_entities:
        build_safetyreport(
            root,
            te,
            te.enrollments[0],
            country,
            receiverorganization,
            receivercountrycode,
        )

    print_root(root)
