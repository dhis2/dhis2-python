import logging
from typing import List

from .inventory import HostResolved
from .http import BaseHttpRequest

log = logging.getLogger(__name__)


def inspect_host(host: HostResolved):
    req = BaseHttpRequest(host)
    data = req.get("api/system/info")

    if not data:
        return

    d = {
        "contextPath": data["contextPath"],
        "serverDate": data["serverDate"],
        "version": data["version"],
        "revision": data["revision"],
    }

    print(d)


def inspect(hosts: List[HostResolved] = []):
    for host in hosts:
        if "dhis2" != host.type:
            log.warning(f"Only 'dhis2' type is supported, ignoring host '{host.key}' with type '{host.type}'")
            continue

        inspect_host(host)
