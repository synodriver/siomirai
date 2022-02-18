# -*- coding: utf-8 -*-
from dataclasses import dataclass

from siomirai._rqpy import QRCodeState

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
class GroupMessageEvent(BaseEvent):
    pass
