import logging

from lxml.builder import E

from .e2b_resources import build_messageheader, build_safetyreport, print_root
from .models.e2b import TrackedEntity

log = logging.getLogger(__name__)


def run(te: TrackedEntity, *, country: str, sender_id: str, receiver_id: str):
    root = E.ichicsr(lang="en")
    build_messageheader(root, sender_id, receiver_id)

    build_safetyreport(root, te, te.enrollments[0], country)

    print_root(root)
