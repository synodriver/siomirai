from enum import Enum, auto
from typing import List, Union, Tuple
from io import BytesIO

from siomirai.config import Config
from siomirai.exceptions import ProtocolException
from siomirai.events import PacketReceived, TransEmpResponse, LoginResponse, UpdateSignatureResponse, \
    ClientRegisterResponse, HeartBeatEvent
from siomirai._rqpy import Device, Engine, Packet

__version__ = "0.0.1"


class ParserState(Enum):
    read_length = auto()
    read_payload = auto()


class Connection:
    """基于有限状态机的协议解析器"""

    def __init__(self, conf: Config):
        self.config = conf
        self._parser_state = ParserState.read_length
        self._buffer = bytearray()
        self._current_len = 0  # payload only
        self._engine = Engine(conf.device, conf.protocol)

        self.state = {}  # 客户端的状态，群信息 自己信息之类的

    def feed_data(self, data: Union[bytes, bytearray]) -> List[PacketReceived]:
        assert data, "No data at all"
        self._buffer.extend(data)
        packets = []  # type: List[Packet]
        while True:
            if self._parser_state == ParserState.read_length:
                if len(self._buffer) >= 4:
                    self._current_len = int.from_bytes(self._buffer[:4], "big") - 4
                    self._parser_state = ParserState.read_payload
                    self._buffer = self._buffer[4:]
                else:
                    break
            if self._parser_state == ParserState.read_payload:
                if len(self._buffer) >= self._current_len:
                    packets.append(self._engine.decode_packet(bytes(self._buffer[:self._current_len])))
                    self._parser_state = ParserState.read_length
                    self._buffer = self._buffer[self._current_len:]
                else:
                    break
            if not self._buffer:
                break
        # docede packet
        events = []  # type: List[PacketReceived]
        for pkt in packets:
            if pkt.command_name == "wtlogin.trans_emp":
                resp = self._engine.decode_trans_emp_response(pkt.body)
                events.append(TransEmpResponse(seq_id=pkt.seq_id,
                                               command_name=pkt.command_name,
                                               uin=pkt.uin,
                                               packet_type=pkt.packet_type,
                                               message=pkt.message,
                                               encrypt_type=pkt.encrypt_type,

                                               resp=resp))
            elif pkt.command_name == "wtlogin.login":
                resp = self._engine.decode_login_response(pkt.body)
                events.append(LoginResponse(seq_id=pkt.seq_id,
                                            command_name=pkt.command_name,
                                            uin=pkt.uin,
                                            packet_type=pkt.packet_type,
                                            message=pkt.message,
                                            encrypt_type=pkt.encrypt_type,

                                            account_frozen=resp.account_frozen,
                                            device_lock_login=resp.device_lock_login,
                                            device_locked=resp.device_locked,
                                            need_captcha=resp.need_captcha,
                                            success=resp.success,
                                            too_many_sms_request=resp.too_many_sms_request,
                                            unknown_status=resp.unknown_status))
            elif pkt.command_name == "Signature.auth":
                e = UpdateSignatureResponse(seq_id=pkt.seq_id,
                                            command_name=pkt.command_name,
                                            uin=pkt.uin,
                                            packet_type=pkt.packet_type,
                                            message=pkt.message,
                                            encrypt_type=pkt.encrypt_type)
                e.body = pkt.body
                events.append(e)

            elif pkt.command_name == "StatSvc.register":
                e = ClientRegisterResponse(seq_id=pkt.seq_id,
                                           command_name=pkt.command_name,
                                           uin=pkt.uin,
                                           packet_type=pkt.packet_type,
                                           message=pkt.message,
                                           encrypt_type=pkt.encrypt_type)
                e.body = pkt.body
                events.append(e)

            elif pkt.command_name == "Heartbeat.Alive":
                e = HeartBeatEvent(seq_id=pkt.seq_id,
                                   command_name=pkt.command_name,
                                   uin=pkt.uin,
                                   packet_type=pkt.packet_type,
                                   message=pkt.message,
                                   encrypt_type=pkt.encrypt_type)
                e.body = pkt.body
                events.append(e)

            else:
                e = PacketReceived(seq_id=pkt.seq_id,
                                   command_name=pkt.command_name,
                                   uin=pkt.uin,
                                   packet_type=pkt.packet_type,
                                   message=pkt.message,
                                   encrypt_type=pkt.encrypt_type)  # todo 更多种类 这个兜底的
                e.body = pkt.body
                events.append(e)

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

    def qrcode_login(self, t106: bytes, t16a: bytes, t318: bytes) -> Tuple[int, bytes]:
        pkt = self._engine.build_qrcode_login_packet(t106, t16a, t318)
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)

    def device_lock_login(self) -> Tuple[int, bytes]:
        pkt = self._engine.build_device_lock_login_packet()
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)

    def login(self, password_md5: bytes) -> Tuple[int, bytes]:
        pkt = self._engine.build_login_packet(password_md5)
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)

    def client_register(self) -> Tuple[int, bytes]:
        pkt = self._engine.build_client_register_packet()
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)

    def heartbeat(self) -> Tuple[int, bytes]:
        pkt = self._engine.build_heartbeat_packet()
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)

    def sms_code_submit(self, code: str) -> Tuple[int, bytes]:
        pkt = self._engine.build_sms_code_submit_packet(code)
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)

    def sms_request(self) -> Tuple[int, bytes]:
        pkt = self._engine.build_sms_request_packet()
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)

    def ticket_submit(self, ticket: str) -> Tuple[int, bytes]:
        pkt = self._engine.build_ticket_submit_packet(ticket)
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)

    def update_signature(self, signature: str) -> Tuple[int, bytes]:
        """
        修改自己的签名
        """
        pkt = self._engine.build_update_signature_packet(signature)
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)

    def uni_packet(self, command_name: str, body: bytes) -> Tuple[int, bytes]:
        pkt = self._engine.uni_packet(command_name, body)
        data = self._engine.encode_packet(pkt)
        return pkt.seq_id, self.send(data)
