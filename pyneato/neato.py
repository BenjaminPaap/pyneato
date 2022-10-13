import os
from dataclasses import dataclass
from typing import List, Union

@dataclass(init=False, frozen=True)
class Vendor:
    name: str
    friendly_name: str
    endpoint: str
    auth_endpoint: str
    mime_version: str = "application/vnd.neato.orbital-http.v1+json"

class Neato(Vendor):
    name = "neato"
    friendly_name: str = "Neato"
    endpoint = "https://orbital.neatocloud.com/"
    auth_endpoint = "https://orbital.neatocloud.com/vendors/neato/sessions"
    mime_version: str = "application/vnd.neato.orbital-http.v1+json"
