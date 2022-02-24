# -*- coding: utf-8 -*-
from dataclasses import dataclass

from siomirai._rqpy import QRCodeState, AccountInfo

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
    account_info: AccountInfo
    too_many_sms_request:bool



@dataclass
class GroupMessageEvent(BaseEvent):
    pass
