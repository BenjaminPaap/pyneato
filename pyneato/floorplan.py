import base64
import logging
import io

import PIL.Image as Image

from .session import Session
from .enum import TrackTypeEnum, CleaningModeEnum

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
    Coerce,
)

_LOGGER = logging.getLogger(__name__)

TRACK_SCHEMA = Schema(
    Any(
        {
            "track_uuid": str,
            "name": Any(str, None),
            "icon_id": Any(str, None),
            "type": Coerce(TrackTypeEnum),
            "binary": str,
            "cleaning_mode": Any(Coerce(CleaningModeEnum), None),
            "inserted_at": str,
            "updated_at": str,
        },
        extra=ALLOW_EXTRA,
    ),
    extra=ALLOW_EXTRA,
)

class Floorplan:
    def __init__(
        self,
        session: Session,
        uuid: str,
        name: str | None,
        rank_uuid: str,
        rank_binary,
    ):
        self._session = session
        self.name = name
        self.uuid = uuid
        self.rank_uuid = rank_uuid
        self._tracks = set()

        self._rank_binary = rank_binary

    @property
    def rank_image(self) -> Image:
        """
        Get the image of the floorplan

        :return: The image of the floorplan
        """
        img_str = base64.b64decode(self._rank_binary)
        pil_image = Image.open(io.BytesIO(bytearray(img_str)))
        image_grey = pil_image.split()[0]
        color_conversion = {0: 228, 1: 169, 2: 255}
        image_color = image_grey.point(lambda p: color_conversion[p])
        return image_color.convert("RGB")

    @property
    def tracks(self):
        """
        Return set of tracks for this floorplan

        :return:
        """
        if not self._tracks:
            self.refresh_tracks()

        return self._tracks

    def __str__(self):
        return "Name: %s, UUID: %s, RankID: %s" % (
            self.name,
            self.uuid,
            self.rank_uuid,
        )

    def refresh_tracks(self):
        resp = self._session.get("maps/floorplans/%s/tracks"%(self.uuid))

        for track in resp.json():
            if track["name"] == None:
                continue

            try:
                cleaning_mode = None
                if None != track["cleaning_mode"]:
                    cleaning_mode = CleaningModeEnum(track["cleaning_mode"])

                TRACK_SCHEMA(track)
                track_object = Track(
                    floorplan=self,
                    uuid=track["track_uuid"],
                    name=track["name"],
                    type=track["type"],
                    cleaning_mode=cleaning_mode
                )

                self._tracks.add(track_object)
            except MultipleInvalid as ex:
                _LOGGER.warning(
                    "Bad response from tracks endpoint: %s. Got: %s", ex, track
                )
                continue


class Track:
    def __init__(self, floorplan: Floorplan, uuid: str, name: str, type: str, cleaning_mode: CleaningModeEnum):
        """"""
        self.floorplan = Floorplan
        self.uuid = uuid
        self.name = name
        self.type = type
        self.cleaning_mode = cleaning_mode
