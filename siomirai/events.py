# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional

from siomirai._rqpy import QRCodeState, LoginSuccess


@dataclass
class BaseEvent:
    seq_id: int


@dataclass
class TransEmpResponse(BaseEvent):
    command_name: str
    uin: int
    packet_type: int
    message: str
    encrypt_type: int
    resp: QRCodeState


@dataclass
class LoginResponse(BaseEvent):
    account_frozen: bool
    device_lock_login: bool
    success: Optional[LoginSuccess]
    too_many_sms_request: bool


@dataclass
class GroupMessageEvent(BaseEvent):
    pass
