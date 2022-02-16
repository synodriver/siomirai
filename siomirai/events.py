# -*- coding: utf-8 -*-
from dataclasses import dataclass

@dataclass
class BaseEvent:
    pass


@dataclass
class RawData(BaseEvent):
    data:bytes