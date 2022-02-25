from typing import Any, ClassVar, Optional


class AccountInfo:
    age: int = ...
    gender: int = ...
    nick: str = ...

    @classmethod
    def __init__(self, *args, **kwargs) -> None: ...


class Device:
    @classmethod
    def __init__(self, *args, **kwargs) -> None: ...

    def ksid(self) -> bytes: ...

    @staticmethod
    def random() -> Device: ...


class Engine:
    @classmethod
    def __init__(self, *args, **kwargs) -> None: ...

    def build_device_lock_login_packet(self) -> Packet: ...

    def build_qrcode_fetch_request_packet(self) -> Packet: ...

    def build_qrcode_login_packet(self, t106: bytes, t16a: bytes, t318: bytes) -> Packet: ...

    def build_qrcode_result_query_request_packet(self, sig: bytes) -> Packet: ...

    def decode_login_response(self, payload: bytes) -> LoginResponse: ...

    def decode_packet(self, payload: bytes) -> Packet: ...

    def decode_trans_emp_response(self, payload: bytes) -> QRCodeState: ...

    def encode_packet(self, pkt: Packet) -> bytes: ...


class LoginResponse:
    account_frozen: Optional[bool] = ...
    device_lock_login: Optional[bool] = ...
    success: Optional[LoginSuccess] = ...
    too_many_sms_request: Optional[bool] = ...

    @classmethod
    def __init__(self, *args, **kwargs) -> None: ...


class LoginSuccess:
    account_info: Optional[AccountInfo] = ...

    @classmethod
    def __init__(self, *args, **kwargs) -> None: ...


class Packet:
    body: bytes = ...
    command_name: str = ...
    encrypt_type: int = ...
    message: ClassVar[getset_descriptor] = ...
    packet_type: int = ...
    seq_id: int = ...
    uin: int = ...

    @classmethod
    def __init__(self, *args, **kwargs) -> None: ...


class QRCodeConfirmed:
    tgt_qr: bytes = ...
    tmp_no_pic_sig: bytes = ...
    tmp_pwd: bytes = ...
    uin: int = ...

    @classmethod
    def __init__(self, *args, **kwargs) -> None: ...


class QRCodeImageFetch:
    image: bytes = ...
    sig: bytes = ...

    @classmethod
    def __init__(self, *args, **kwargs) -> None: ...


class QRCodeState:
    canceled: Optional[bool] = ...
    confirmed: Optional[QRCodeConfirmed] = ...
    image_fetch: Optional[QRCodeImageFetch] = ...
    timeout: Optional[bool] = ...
    waiting_for_confirm: Optional[bool] = ...
    waiting_for_scan: Optional[bool] = ...

    @classmethod
    def __init__(self, *args, **kwargs) -> None: ...


def sum_as_string(a: int, b: int) -> str: ...