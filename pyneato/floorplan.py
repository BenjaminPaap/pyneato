from .session import Session

from voluptuous import (
    ALLOW_EXTRA,
    All,
    Any,
    Extra,
    MultipleInvalid,
    Optional,
    Range,
    Required,
    Schema,
    Url,
)

class Floorplan:
    def __init__(self, session: Session, uuid: str, name: str, rank_uuid: str):
        self._session = session
        self.name = name
        self.uuid = uuid
        self.rank_uuid = rank_uuid

    def __str__(self):
        return "Name: %s, UUID: %s, RankID: %s" % (
            self.name,
            self.uuid,
            self.rank_uuid,
        )
