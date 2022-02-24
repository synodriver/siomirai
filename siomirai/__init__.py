from enum import Enum, auto
from typing import List, Union, Tuple
from io import BytesIO

from siomirai.config import Config
from siomirai.exceptions import ProtocolException
from siomirai.events import BaseEvent, TransEmpResponse
from siomirai._rqpy import Device, Engine, Packet

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
        self._engine = Engine(conf.device, conf.protocol)

    def feed_data(self, data: Union[bytes, bytearray]) -> List[BaseEvent]:
        assert data, "No data at all"
        self._buffer.extend(data)
        packets = []  # type: List[Packet]
        while True:
            if self.state == ParserState.read_length:
                if len(self._buffer) >= 4:
                    self._current_len = int.from_bytes(self._buffer[:4], "big") - 4
                    self.state = ParserState.read_payload
                    self._buffer = self._buffer[4:]
                else:
                    break
            if self.state == ParserState.read_payload:
                if len(self._buffer) >= self._current_len:
                    packets.append(self._engine.decode_packet(bytes(self._buffer[:self._current_len])))
                    self.state = ParserState.read_length
                    self._buffer = self._buffer[self._current_len:]
                else:
                    break
            if not self._buffer:
                break
        # docede packet
        events = []
        for pkt in packets:
            if pkt.command_name == "wtlogin.trans_emp":
                resp = self._engine.decode_trans_emp_response(pkt.body)
                events.append(TransEmpResponse(seq_id=pkt.seq_id,
                                               command_name=pkt.command_name,
                                               uin=pkt.uin,
                                               packet_type=pkt.packet_type,
                                               message=pkt.message,
                                               encrypt_type=pkt.encrypt_type,
                                               resp=resp))  # todo 更多种类
            elif pkt.command_name == "wtlogin.login":
                resp = self._engine.decode_login_response(pkt.body)
        return events

    def send(self, data: bytes) -> bytes:
        buffer = BytesIO()
        buffer.write((len(data) + 4).to_bytes(4, "big"))
        buffer.write(data)
        return buffer.getvalue()

    def fetch_qrcode(self) -> Tuple[int, bytes]:
        """
        已经包括自己长度了
        """
        pkt = self._engine.build_qrcode_fetch_request_packet()
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)

    def query_qrcode_result(self, sig: bytes) -> Tuple[int, bytes]:
        pkt = self._engine.build_qrcode_result_query_request_packet(sig)
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)

    def login_qrcode(self, t106: bytes, t16a: bytes, t318: bytes):
        pkt = self._engine.build_qrcode_login_packet(t106, t16a, t318)
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)
