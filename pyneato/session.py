import binascii
import json
import os
import os.path
import requests
from typing import Callable, Dict, Optional

from .neato import Vendor, Neato
from .exception import MyNeatoException, MyNeatoLoginException, MyNeatoRobotException

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

class Session:
    def __init__(self, vendor: Vendor):
        """Initialize the session."""
        self.vendor = vendor
        self.endpoint = vendor.endpoint
        self.headers = {"Accept": vendor.mime_version}
        self.access_token = ""

    def get(self, path, **kwargs):
        """Send a GET request to the specified path."""
        raise NotImplementedError

    def urljoin(self, path):
        return urljoin(self.endpoint, path)

    def generate_headers(
        self, custom_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        """Merge self.headers with custom headers if necessary."""
        if not custom_headers:
            return self.headers

        return {**self.headers, **custom_headers}


class OrbitalPasswordSession(Session):
    def __init__(self, email: str, password: str, vendor: Vendor = Neato()):
        super().__init__(vendor=vendor)
        self._login(email, password)

    def _login(self, email: str, password: str):
        """
        Login to your myneato account
        """

        try:
            response = requests.post(
                urljoin(self.endpoint, "vendors/neato/sessions"),
                json={
                    "email": email,
                    "password": password,
                },
                headers=self.headers,
            )

            response.raise_for_status()
            self.access_token = response.json()["token"]

            self.headers["Authorization"] = "Token %s" % self.access_token
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.Timeout,
        ) as ex:
            if (
                isinstance(ex, requests.exceptions.HTTPError)
                and ex.response.status_code == 403
            ):
                raise MyNeatoLoginException(
                    "Unable to login to myneato account. check account credentials."
                ) from ex
            raise MyNeatoRobotException("Unable to connect to Neato API.") from ex

    def get(self, path, **kwargs):
        url = self.urljoin(path)
        headers = self.generate_headers(kwargs.pop("headers", None))
        try:
            response = requests.get(url, headers=headers, **kwargs)
            response.raise_for_status()
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.Timeout,
        ) as ex:
            raise MyNeatoException("Unable to connect to myneato servers.") from ex
        return response
