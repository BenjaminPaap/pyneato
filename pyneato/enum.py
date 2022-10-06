from enum import Enum

class RobotAbilityEnum(str, Enum):
    STATE_SHOW = "state.show"


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


class BaseTypeEnum(str, Enum):
    STANDARD = "standard"

    @staticmethod
    def from_str(type: str):
        if type == 'standard':
            return TrackTypeEnum.STANDARD
        else:
            raise NotImplementedError('BaseType %s'%type)


class TrackTypeEnum(str, Enum):
    CLEANING = "cleaning"
    NOGO = "no-go"

    @staticmethod
    def from_str(type: str):
        if type == 'cleaning':
            return TrackTypeEnum.CLEANING
        if type == 'no-go':
            return TrackTypeEnum.NOGO
        else:
            raise NotImplementedError('TrackType %s'%type)


class CleaningModeEnum(str, Enum):
    ECO = "eco"
    MAX = "max"
    TURBO = "turbo"

    @staticmethod
    def from_str(mode: str):
        if mode == 'eco':
            return CleaningModeEnum.ECO
        elif mode == 'max':
            return CleaningModeEnum.MAX
        elif mode == 'turbo':
            return CleaningModeEnum.TURBO
        else:
            raise NotImplementedError('CleaningMode %s'%mode)


class NavigationModeEnum(str, Enum):
    NORMAL = "normal"

    @staticmethod
    def from_str(mode: str):
        if mode == 'normal':
            return NavigationModeEnum.NORMAL
        else:
            raise NotImplementedError('NavigationMode %s'%mode)
