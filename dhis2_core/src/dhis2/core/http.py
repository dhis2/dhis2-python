import json
import logging
from copy import deepcopy
from enum import Enum
from typing import Dict, Tuple, Union

import requests
from requests.models import Response  # noqa

from .inventory import HostResolved

log = logging.getLogger(__name__)


class MediaFormat(str, Enum):
    json = "application/json"
    text = "text/plain"


class BaseHttpRequest:
    def __init__(self, host: HostResolved, format: Union[MediaFormat, str] = MediaFormat.json):
        self.host = host
        self.format = format

    def get(
        self,
        path,
        params=None,
        headers=None,
    ):
        url = self._get_url(path)
        headers = self._get_headers()
        auth = self._get_auth()
        params = self._get_params(params)

        response = requests.get(
            url=url,
            headers=headers,
            params=params,
            auth=auth,
        )

        log.info(f"Finished GET request '{response.request.url}'' with status code '{response.status_code}''")

        if not response.ok:
            return self._handle_errors(response)

        data = None

        if MediaFormat.json == self.format:
            data = response.json()
        else:
            data = response.text

        return data

    def post(
        self,
        path,
        data,
        params=None,
        headers=None,
    ):
        url = self._get_url(path)
        headers = self._get_headers()
        auth = self._get_auth()
        params = self._get_params(params)

        if not isinstance(data, str):
            data = json.dumps(data)

        response = requests.post(
            url=url,
            headers=headers,
            params=params,
            auth=auth,
            data=data,
        )

        log.info(f"Finished POST request '{response.request.url}'' with status code '{response.status_code}''")

        if not response.ok:
            return self._handle_errors(response)

        if MediaFormat.json == self.format:
            data = response.json()
        else:
            data = response.text

        return data

    def _handle_errors(self, response: Response):
        if 401 == response.status_code:
            log.error(f"Invalid login credentials for '{self.host.key}''")
        if 404 == response.status_code:
            log.error(f"Invalid url '{response.request.url}', please check 'baseUrl' for '{self.host.key}'")
        else:
            log.error(f"Unhandled status code {response.status_code}={response.text}")

        return None

    def _get_auth(self) -> Union[Tuple[str], None]:
        if "http-basic" == self.host.auth.type:
            return (self.host.auth.username, self.host.auth.password)

        return None

    def _get_headers(self, headers: Dict[str, str] = {}) -> Dict[str, str]:
        headers = deepcopy(headers)

        if isinstance(self.format, MediaFormat):
            headers["Content-Type"] = self.format.value
            headers["Accept"] = self.format.value
        else:
            headers["Content-Type"] = self.format
            headers["Accept"] = self.format

        headers["X-Requested-With"] = "XMLHttpRequest"

        return headers

    def _get_params(self, params={}) -> Dict[str, str]:
        return deepcopy(params)

    def _get_url(self, path="") -> str:
        return f"{self.host.baseUrl}/{path}"
