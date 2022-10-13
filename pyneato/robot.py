import re
import logging
import requests

from voluptuous import (
    ALLOW_EXTRA,
    All,
    Any,
    Extra,
    MultipleInvalid,
    Range,
    Required,
    Schema,
    Coerce,
    Equal
)
from enum import Enum

from .neato import Neato
from .enum import CleaningModeEnum, NavigationModeEnum, RobotAbilityEnum, RobotBaseTypeEnum, RobotBagStatusEnum, RobotActionEnum, RobotStateEnum
from .floorplan import Floorplan, Track
from .robot_state import RobotState, RobotStateDetail, RobotStateCleaningCenter
from .exception import MyNeatoRobotException

_LOGGER = logging.getLogger(__name__)

RUN_SCHEMA = Schema(
    {
        "map": {
            "nogo_enabled": bool,
            "rank_id": str,
            "track_id": Any(str, None)
        },
        "settings": {
            "mode": str,
            "navigation_mode": Coerce(CleaningModeEnum)
        }
    }
)

CLEANING_SCHEMA = Schema(
    {
        "ability": str,
        "force_floorplan": bool,
        "runs": [RUN_SCHEMA]
    }
)

ABILITY_SCHEMA = Schema(
    {
        'ability': str,
    }
)

STATE_SCHEMA = Schema(
    {
        Required('ability'): Equal(RobotAbilityEnum.STATE_SHOW),
        'action': str,
        'autonomy_states': {
            'active_cleaning_after_suspended': int,
            'active_cleaning_session': int,
            'cleaning_start': int,
            'docking': int,
            'docking_for_suspended': int,
            'docking_successful': int,
            'docking_successful_suspended': int,
            'docking_verify_base': int,
            'started_on_base': bool,
            'suspended_charging_start': int,
            'undocking': int,
            'undocking_after_suspended': int
        },
        'available_commands': {
            'cancel': bool,
            'pause': bool,
            'resume': bool,
            'return_to_base': bool,
            'start': bool
        },
        'cleaning_center': {
            'bag_status': str,
            'base_error': Any(str, None),
            'is_extracting': bool
        },
        'details': {
            'base_type': str,
            'charge': int,
            'is_charging': bool,
            'is_docked': bool,
            'is_quickboost': bool,
            'quickboost_estimate': int
        },
        'errors': Any(None),
        'state': str
    }
)

ROBOT_INFO_SCHEMA = Schema(
    {
        'ability': str,
        'firmware': str,
        'serial_number': str,
    }
)

class Robot:
    """Data and methods for interacting with a Neato vacuum robot"""

    def __init__(
        self,
        session,
        serial,
        id,
        user_id,
        name,
        endpoint,
        vendor_code,
        vendor=Neato,
    ):
        self._session = session
        self.name = name
        self.vendor = vendor
        self._vendor_code = vendor_code
        self.serial = serial
        self.id = id
        self.user_id = user_id
        self.endpoint = endpoint
        self.model_name = None
        self.firmware = None
        self.timezone = None
        self.birth_date = None

        self._url = "{endpoint}/vendors/{vendor_code}/robots/{serial}/messages".format(
            endpoint=re.sub(":\d+", "", endpoint.rstrip('/')),
            vendor_code=vendor_code,
            serial=self.serial,
        )
        self._headers = session.headers
        self._headers["Accept"] = vendor.mime_version

    def __str__(self):
        return "Name: %s, Serial: %s, ID: %s UserID: %s" % (
            self.name,
            self.serial,
            self.id,
            self.user_id,
        )

    def _message(self, message: str, json: dict, schema: Schema):
        """
        Sends message to robot with data from parameter 'json'
        :param json: dict containing data to send
        :return: server response
        """

        _LOGGER.debug(json)

        try:
            response = requests.post(
                self._url + "?ability=%s"%message,
                json=json,
                headers=self._headers,
            )
            response.raise_for_status()
            schema(response.json())
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
        ) as ex:
            _LOGGER.warning("Unable to communicate with robot: %s"%(
                ex
            ))
            raise MyNeatoRobotException("Unable to communicate with robot") from ex
        except MultipleInvalid as ex:
            _LOGGER.warning(
                "Invalid response from %s: %s. Got: %s", self._url, ex, response.json()
            )

        return response

    def start_cleaning(
        self, floorplan: Floorplan, tracks: list[Track] = None, cleaning_mode = CleaningModeEnum.MAX, nogo_enabled = True
    ):
        ability_name = "cleaning.start"
        runs = []

        if tracks == None:
            runs.append({
                "map": {
                    "nogo_enabled": True,
                    "rank_id": floorplan.rank_uuid,
                    "track_id": None
                },
                "settings": {
                    "mode": cleaning_mode.value,
                    "navigation_mode": NavigationModeEnum.NORMAL.value
                }
            })
        else:
            for track in tracks:
                runs.append({
                    "map": {
                        "nogo_enabled": True,
                        "rank_id": floorplan.rank_uuid,
                        "track_id": track.uuid
                    },
                    "settings": {
                        "mode": track.cleaning_mode.value if track.cleaning_mode != None else None,
                        "navigation_mode": NavigationModeEnum.NORMAL.value
                    }
                })

        json = {
            "ability": ability_name,
            "force_floorplan": False,
            "runs": runs
        }

        response = self._message(ability_name, json, CLEANING_SCHEMA)
        result = response.json().get("ability", None)
        if result != ability_name:
            _LOGGER.warning(
                "Result of robot.%s is not ok: %s", ability_name, result
            )

        return {
            result: result == ability_name,
            response: response
        }

    def _base_message(self, message: str, schema: Schema):
        ability_name = message
        json = {
            "ability": message,
        }

        response = self._message(message, json, schema)
        result = response.json().get("ability", None)
        if result != message:
            _LOGGER.warning(
                "Result of robot.%s is not ok: %s, alert: %s", message, result
            )

        return {
            "success": result == ability_name,
            "response": response
        }

    def pause_cleaning(self) -> bool:
        result = self._base_message("cleaning.pause", ABILITY_SCHEMA)

        return result.success

    def get_state(self) -> RobotState:
        result = self._base_message(RobotAbilityEnum.STATE_SHOW.value, STATE_SCHEMA)
        response = result["response"]

        json = response.json()

        state = RobotState(
            RobotActionEnum(json["action"]),
            RobotStateEnum(json["state"]),
        )

        state.cleaning_center = RobotStateCleaningCenter(
            RobotBagStatusEnum(json["cleaning_center"]["bag_status"]),
            json["cleaning_center"]["base_error"],
            json["cleaning_center"]["is_extracting"],
        )

        state.details = RobotStateDetail(
            RobotBaseTypeEnum(json["details"]["base_type"]),
            json["details"]["charge"],
            json["details"]["is_charging"],
            json["details"]["is_docked"],
            json["details"]["is_quickboost"],
            json["details"]["quickboost_estimate"],
        )

        for command, available in json["available_commands"].items():
            if available:
                state.available_commands.append(command)

        return state

    def info_robot(self):
        result = self._base_message("info.robot", ROBOT_INFO_SCHEMA)
        response = result["response"]

        _LOGGER.debug(response.json())

        return response.json()

    def resume_cleaning(self) -> bool:
        result = self._base_message("cleaning.resume", ABILITY_SCHEMA)

        return result.success

    def cancel_cleaning(self) -> bool:
        pause_result = self.pause_cleaning()
        return_to_base_result = self.return_to_base()

        return pause_result.success and return_to_base_result.success

    def return_to_base(self):
        return self._base_message("navigation.return_to_base", ABILITY_SCHEMA)

    @property
    def state(self):
        return self.get_state()
