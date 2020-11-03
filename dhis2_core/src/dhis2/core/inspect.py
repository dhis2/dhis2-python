import logging
from typing import List

from .http import BaseHttpRequest
from .inventory import HostResolved
from .metadata.models.system_info import SystemInfo

log = logging.getLogger(__name__)


def inspect_host(host: HostResolved):
    req = BaseHttpRequest(host)
    data = req.get("api/system/info")

    if not data:
        return

    info = SystemInfo(**data)

    log.info(info)


def inspect(hosts: List[HostResolved] = []):
    for host in hosts:
        if "dhis2" != host.type:
            log.warning(f"Only 'dhis2' type is supported, ignoring host '{host.key}' with type '{host.type}'")
            continue

        inspect_host(host)
