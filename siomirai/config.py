# -*- coding: utf-8 -*-
from typing import Union
from dataclasses import dataclass
from enum import IntEnum

from siomirai._rqpy import Device


class Protocol(IntEnum):
    AndroidPhone = 1
    AndroidWatch = 2
    MacOS = 3
    QiDian = 4
    IPad = 5


@dataclass
class Config:
    timeout: Union[float, int]
    device: Device
    protocol: Protocol = Protocol.AndroidPhone
    uin: int = 0
    password: str = ""
