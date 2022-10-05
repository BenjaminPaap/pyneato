import logging
import os
import shutil

import requests
from .session import Session
from .robot import Robot
from .floorplan import Floorplan

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

_LOGGER = logging.getLogger(__name__)

ROBOT_SCHEMA = Schema(
    {
        Required("id"): str,
        Required("user_id"): str,
        Required("serial"): str,
        Required("name"): str,
        "model_name": Any(str, None),
        "firmware": Any(str, None),
        "timezone": Any(str, None),
        "mac_address": Any(str, None),
        "birth_date": Any(str, None),
        "vendor": Any(str, None),
    },
    extra=ALLOW_EXTRA,
)

FLOORPLAN_SCHEMA = Schema(
    {
        Required("floorplan_uuid"): str,
        Required("rank_uuid"): str,
        Required("name"): str,
        "map_versions_count": int,
    },
    extra=ALLOW_EXTRA,
)

class Account:
    def __init__(self, session: Session):
        """Initialize the account data."""
        self._robots = set()
        self._floorplans = set()
        self._session = session

    @property
    def robots(self):
        """
        Return set of robots for logged in account.

        :return:
        """
        if not self._robots:
            self.refresh_robots()

        return self._robots

    @property
    def floorplans(self):
        """
        Return set of floorplans for logged in account.
        """
        if not self._floorplans:
            self.refresh_floorplans()

        return self._floorplans

    def refresh_robots(self):
        """
        Get information about robots connected to account.

        :return:
        """

        resp = self._session.get("users/me/robots")

        for robot in resp.json():
            _LOGGER.debug("Create Robot: %s", robot)
            try:
                ROBOT_SCHEMA(robot)
                robot_object = Robot(
                    session=self._session,
                    serial=robot["serial"],
                    id=robot["id"],
                    user_id=robot["user_id"],
                    name=robot["name"],
                    endpoint=self._session.endpoint,
                    vendor_code=robot["vendor"],
                    vendor=self._session.vendor,
                )
                self._robots.add(robot_object)
            except MultipleInvalid as ex:
                # Robot was not described accordingly by neato
                _LOGGER.warning(
                    "Bad response from robots endpoint: %s. Got: %s", ex, robot
                )
                continue
            except NeatoUnsupportedDevice:
                # Robot does not support home_cleaning service
                _LOGGER.warning("Your robot %s is unsupported.", robot["name"])
                continue
            except NeatoRobotException:
                # The state of the robot could not be received
                _LOGGER.warning("Your robot %s is offline.", robot["name"])
                continue

    def refresh_floorplans(self):
        _LOGGER.debug("Getting floorplans")

        for robot in self.robots:
            self.get_floorplan(robot)

    def get_floorplan(self, robot: Robot):
        _LOGGER.debug("Getting floorplan for %s", robot.name)

        resp = self._session.get("/robots/%s/floorplans"%robot.id)

        for floorplan in resp.json():
            FLOORPLAN_SCHEMA(floorplan)
            floorplan_object = Floorplan(
                session = self._session,
                uuid = floorplan["floorplan_uuid"],
                name = floorplan["name"],
                rank_uuid = floorplan["rank_uuid"],
            )
            self._floorplans.add(floorplan_object)
