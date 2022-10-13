import logging
import os
import shutil
from typing import List

import requests

from .exception import MyNeatoRobotException, MyNeatoUnsupportedDevice
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

USERDATA_SCHEMA = Schema(
    {
      Required("country_code"): str,
      Required("email"): str,
      Required("id"): str,
      Required("locale"): str,
      Required("first_name"): str,
      Required("last_name"): str,
      "newsletter": bool,
      "state_region": Any(str, None),
      "vendor": str,
      "verified_at": Any(str, None)
    },
    extra=ALLOW_EXTRA,
)

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
        self._session = session
        self._robots = []
        self._floorplans = []
        self._userdata = set()

    @property
    def robots(self) -> List[Robot]:
        """
        Return set of robots for logged in account.

        :return:
        """
        if not self._robots:
            self.refresh_robots()

        return self._robots

    @property
    def floorplans(self) -> List[Floorplan]:
        """
        Return set of floorplans for logged in account.
        """
        if not self._floorplans:
            self.refresh_floorplans()

        return self._floorplans

    @property
    def userdata(self):
        """
        Return the user
        """
        if not self._userdata:
            self.get_userdata()

        return self._userdata

    def refresh_robots(self):
        """
        Get information about robots connected to account.

        :return:
        """

        resp = self._session.get("users/me/robots")

        self._robots = []
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
                robot_object.birth_date = robot['birth_date']
                robot_object.firmware = robot['firmware']
                robot_object.model_name = robot['model_name']
                robot_object.timezone = robot['timezone']

                self._robots.append(robot_object)
            except MultipleInvalid as ex:
                # Robot was not described accordingly by neato
                _LOGGER.warning(
                    "Bad response from robots endpoint: %s. Got: %s", ex, robot
                )
                continue
            except MyNeatoUnsupportedDevice:
                # Robot does not support home_cleaning service
                _LOGGER.warning("Your robot %s is unsupported.", robot["name"])
                continue
            except MyNeatoRobotException:
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

        self._floorplans = []
        for floorplan in resp.json():
            FLOORPLAN_SCHEMA(floorplan)
            floorplan_object = Floorplan(
                session = self._session,
                uuid = floorplan["floorplan_uuid"],
                name = floorplan["name"],
                rank_uuid = floorplan["rank_uuid"],
            )
            self._floorplans.append(floorplan_object)

    def get_userdata(self):
        resp = self._session.get("/users/me")

        json = resp.json()
        USERDATA_SCHEMA(json)
        self._userdata = json
