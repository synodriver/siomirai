# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Optional

from siomirai._rqpy import QRCodeState, LoginSuccess, Packet, LoginDeviceLocked, LoginNeedCaptcha


@dataclass
class BaseEvent:
    seq_id: int


@dataclass
class PacketReceived(BaseEvent):
    command_name: str
    uin: int
    packet_type: int
    message: str
    encrypt_type: int
    body: Optional[bytes] = field(default=None, init=False)


@dataclass
class TransEmpResponse(PacketReceived):
    resp: QRCodeState  # 假装是enum的东西


@dataclass
class LoginResponse(PacketReceived):
    account_frozen: bool
    device_lock_login: bool
    device_locked: Optional[LoginDeviceLocked]
    need_captcha: Optional[LoginNeedCaptcha]
    success: Optional[LoginSuccess]
    too_many_sms_request: bool
    unknown_status: bool


@dataclass
class UpdateSignatureResponse(PacketReceived):
    pass


@dataclass
class ClientRegisterResponse(PacketReceived):
    pass


@dataclass
class HeartBeatEvent(PacketReceived):
    pass


@dataclass
class GroupMessageEvent(BaseEvent):
    pass
