from enum import Enum, auto
from typing import List
from io import BytesIO

from .config import Config
from .exceptions import ProtocolException
from .events import BaseEvent, RawData

__version__ = "0.0.1"


class ParserState(Enum):
    read_length = auto()
    read_payload = auto()


class Connection:
    """基于有限状态机的协议解析器"""

    def __init__(self, conf: Config):
        self.config = conf
        self.state = ParserState.read_length
        self._buffer = bytearray()
        self._current_len = 0  # payload only

    def feed_data(self, data: bytes) -> List[BaseEvent]:
        assert data, "No data at all"
        self._buffer.extend(data)
        ret = []
        while True:
            if self.state == ParserState.read_length:
                if len(self._buffer) > 4:
                    self._current_len = int.from_bytes(self._buffer[:4], "big") - 4
                    self.state = ParserState.read_payload
                    self._buffer = self._buffer[4:]
                else:
                    break
            if self.state == ParserState.read_payload:
                if len(self._buffer) > self._current_len:
                    ret.append(RawData(data=self._buffer[:self._current_len]))
                    self.state = ParserState.read_length
                    self._buffer = self._buffer[self._current_len:]
                else:
                    break
            if not self._buffer:
                break
        return ret

    def send(self, data: bytes) -> bytes:
        buffer = BytesIO()
        buffer.write((len(data) + 4).to_bytes(4, "big"))
        buffer.write(data)
        return buffer.getvalue()
