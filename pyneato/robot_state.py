from typing import List
from enum import Enum

class RobotStateEnum(Enum):
    BUSY = 'busy'
    IDLE = 'idle'

    @staticmethod
    def from_str(state: str):
        if state == 'busy':
            return RobotStateEnum.BUSY
        elif state == 'idle':
            return RobotStateEnum.IDLE
        else:
            raise NotImplementedError('RobotState %s'%state)


class RobotActionEnum(Enum):
    INVALID = 'invalid'
    CLEANING = 'cleaning'
    DOCKING = 'docking'

    @staticmethod
    def from_str(action: str):
        if action == 'invalid':
            return RobotActionEnum.INVALID
        elif action == 'cleaning':
            return RobotActionEnum.CLEANING
        elif action == 'docking':
            return RobotActionEnum.DOCKING
        else:
            raise NotImplementedError('RobotAction %s'%action)


class RobotBaseTypeEnum(Enum):
    STANDARD = 'standard'

    @staticmethod
    def from_str(type: str):
        if type == 'standard':
            return RobotBaseTypeEnum.STANDARD
        else:
            raise NotImplementedError('RobotBaseType %s'%type)


class RobotBagStatusEnum(Enum):
    BAG_OK = 'bag_ok'

    @staticmethod
    def from_str(status: str):
        if status == 'bag_ok':
            return RobotBagStatusEnum.BAG_OK
        else:
            raise NotImplementedError


class RobotState:
    def __init__(self, action: str, state: str, available_commands: List[str] = []):
        self._action = RobotActionEnum.from_str(action)
        self._state = RobotStateEnum.from_str(state)
        self.available_commands = available_commands
        self.cleaning_center = None
        self.details = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: str):
        self._state = RobotStateEnum.from_str(state)

    @property
    def action(self):
        return self._action

    @action.setter
    def state(self, action: str):
        self._action = RobotActionEnum.from_str(action)


class RobotStateDetail:
    def __init__(
        self,
        base_type: str,
        charge: int,
        is_charging: bool,
        is_docked: bool,
        is_quickboost: bool,
        quickboot_estimate: int = -1
    ):
        self._base_type = RobotBaseTypeEnum.from_str(base_type)
        self.charge = charge
        self.is_charging = is_charging
        self.is_docked = is_docked
        self.is_quickboost = is_quickboost
        self.quickboot_estimate = quickboot_estimate

    @property
    def base_type(self):
        return self._base_type

    @base_type.setter
    def state(self, base_type: str):
        self._base_type = RobotBaseTypeEnum.from_str(base_type)


class RobotStateCleaningCenter:
    def __init__(self, bag_status: str, base_error: None, is_extracting: bool):
        self._bag_status = RobotBagStatusEnum.from_str(bag_status)
        self.base_error = base_error
        self.is_extracting = is_extracting

    @property
    def bag_status(self):
        return self._bag_status

    @bag_status.setter
    def state(self, bag_status: str):
        self._bag_status = RobotBagStatusEnum.from_str(bag_status)
