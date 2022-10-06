from typing import List
from enum import Enum
from .enum import RobotStateEnum, RobotActionEnum, RobotBaseTypeEnum, RobotBagStatusEnum

class RobotState:
    def __init__(self, action: RobotActionEnum, state: RobotStateEnum, available_commands: List[str] = []):
        self.action = action
        self.state = state
        self.available_commands = available_commands
        self.cleaning_center = None
        self.details = None


class RobotStateDetail:
    def __init__(
        self,
        base_type: RobotBaseTypeEnum,
        charge: int,
        is_charging: bool,
        is_docked: bool,
        is_quickboost: bool,
        quickboot_estimate: int = -1
    ):
        self._base_type = base_type
        self.charge = charge
        self.is_charging = is_charging
        self.is_docked = is_docked
        self.is_quickboost = is_quickboost
        self.quickboot_estimate = quickboot_estimate


class RobotStateCleaningCenter:
    def __init__(self, bag_status: RobotBagStatusEnum, base_error: None, is_extracting: bool):
        self._bag_status = bag_status
        self.base_error = base_error
        self.is_extracting = is_extracting
