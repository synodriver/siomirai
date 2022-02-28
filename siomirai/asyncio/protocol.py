"""
Network Layer, build on top of asyncio
"""
import asyncio
from typing import Set, Dict

from siomirai import Connection, Config
from siomirai.events import BaseEvent, TransEmpResponse
from siomirai.exceptions import ProtocolException
from siomirai.asyncio.utils import timeout


class BaseClientProtocol(asyncio.BufferedProtocol):
    """
    Supper fast using buffer protocol which support zero-copy receive
    """

    def __init__(self, config: Config):
        self.connection = Connection(config)
        self.transport = None  # type: asyncio.Transport

        self._buffer = None
        self._buffer_view = None
        self._pos = 0

        self._lock = asyncio.Lock()
        self._drain_waiter = asyncio.Event()
        self._drain_waiter.set()   # 一开始必须设置成可以发送
        self._close_waiter = asyncio.get_running_loop().create_future()
        # 还没返回的包 对应seq
        self._pkt_waiters = {}  # type: Dict[int, asyncio.Future]
        # 还在执行的回调
        self._pending_tasks = set()  # type: Set[asyncio.Task]

    def _new_buffer(self, size: int):
        """
        refresh buffer
        """
        self._buffer = bytearray(size)
        self._buffer_view = memoryview(self._buffer)
        self._pos = 0

    def get_buffer(self, sizehint: int) -> memoryview:
        """
        sizehint may be -1 for any non-zero buffer
        """
        if self._buffer is None or abs(sizehint) > len(self._buffer):
            self._new_buffer(abs(sizehint) + 1000)
        elif abs(sizehint) > len(self._buffer) - self._pos or len(self._buffer) == self._pos:
            self._pos = 0
        return self._buffer_view[self._pos:]

    def buffer_updated(self, nbytes: int) -> None:
        new_pos = self._pos + nbytes
        self._data_received(self._buffer[self._pos:new_pos])
        self._pos = new_pos

    def _data_received(self, data: bytearray):
        try:
            for event in self.connection.feed_data(data):
                try:
                    if not self._pkt_waiters[event.seq_id].done():
                        self._pkt_waiters[event.seq_id].set_result(event)
                except IndexError:
                    task = asyncio.create_task(self.on_strange_event(event))
                    self._pending_tasks.add(task)
                    task.add_done_callback(self._pending_tasks.discard)
        except ProtocolException:
            task = asyncio.create_task(self.on_protocol_error())
            self._pending_tasks.add(task)
            task.add_done_callback(self._pending_tasks.discard)
            # if isinstance(event, GroupMessageEvent):
            #     task = asyncio.create_task(self.on_group_message(event))
            #     self._pending_tasks.add(task)
            #     task.add_done_callback(self._pending_tasks.discard)
            # else:
            #     pass  # todo 增加各种event

    def connection_made(self, transport) -> None:
        self.transport = transport

    def connection_lost(self, exc) -> None:
        self.transport = None
        if exc:
            self._close_waiter.set_exception(exc)
        else:
            self._close_waiter.set_result(None)

    def pause_writing(self) -> None:
        self._drain_waiter.clear()

    def resume_writing(self) -> None:
        self._drain_waiter.set()

    async def drain(self):
        await self._drain_waiter.wait()

    async def close(self):
        self.transport.close()
        return await self.wait_closed()

    async def wait_closed(self):
        return await self._close_waiter

    @property
    def closed(self):
        return self._close_waiter.done()

    async def raw_send(self, data: bytes):
        """
        原样发送
        """
        async with self._lock:
            self.transport.write(data)
            await self.drain()

    async def send_data_with_seq_id(self, seq_id: int, data: bytes):
        assert seq_id not in self._pkt_waiters
        self._pkt_waiters[seq_id] = asyncio.get_running_loop().create_future()
        await self.raw_send(data)
        try:
            return await asyncio.wait_for(self._pkt_waiters[seq_id], self.connection.config.timeout)
        finally:
            del self._pkt_waiters[seq_id]

    # async def send(self, data: bytes):
    #     """
    #     发送4字节长度（包括自己）再发送payload
    #     """
    #     data = self.connection.send(data)
    #     await self.raw_send(data)

    # -------------公开方法--------------
    async def fetch_qrcode(self) -> TransEmpResponse:
        seq_id, data = self.connection.fetch_qrcode()
        return await self.send_data_with_seq_id(seq_id, data)

    async def query_qrcode_result(self, sig: bytes):
        seq_id, data = self.connection.query_qrcode_result(sig)
        return await self.send_data_with_seq_id(seq_id, data)

    async def login(self):
        seq_id, data = self.connection.login()
        return await self.send_data_with_seq_id(seq_id, data)

    async def qrcode_login(self, t106: bytes, t16a: bytes, t318: bytes):
        """
        见query_qrcode_result的返回值
        """
        seq_id, data = self.connection.qrcode_login(t106, t16a, t318)
        return await self.send_data_with_seq_id(seq_id, data)

    async def device_lock_login(self):
        seq_id, data = self.connection.device_lock_login()
        return await self.send_data_with_seq_id(seq_id, data)

    async def client_register(self):
        seq_id, data = self.connection.client_register()
        return await self.send_data_with_seq_id(seq_id, data)

    async def heartbeat(self):
        seq_id, data = self.connection.heartbeat()
        return await self.send_data_with_seq_id(seq_id, data)

    async def sms_code_submit(self, code: str):
        seq_id, data = self.connection.sms_code_submit(code)
        return await self.send_data_with_seq_id(seq_id, data)

    async def sms_request(self):
        seq_id, data = self.connection.sms_request()
        return await self.send_data_with_seq_id(seq_id, data)

    async def ticket_submit(self, ticket: str):
        seq_id, data = self.connection.ticket_submit(ticket)
        return await self.send_data_with_seq_id(seq_id, data)

    async def update_signature(self, signature: str):
        seq_id, data = self.connection.update_signature(signature)
        return await self.send_data_with_seq_id(seq_id, data)

    async def uni_packet(self, command_name: str, body: bytes):
        seq_id, data = self.connection.uni_packet(command_name, body)
        return await self.send_data_with_seq_id(seq_id, data)

    # ----------------子类应该实现的回调--------------------
    async def on_protocol_error(self):
        """
        解析协议出错
        """
        pass

    async def on_strange_event(self, event: BaseEvent):
        """
        来了个莫名其妙的seqid时调用
        """
        pass

    async def on_group_message(self, msg):
        pass

    async def on_private_message(self, msg):
        pass
