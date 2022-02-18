"""
Network Layer, build on top of asyncio
"""
import asyncio
from typing import Set, Dict

from siomirai import Connection, Config
from siomirai.events import TransEmpResponse
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
        self._pause_waiter = asyncio.Event()
        self._pause_waiter.set()
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
        if self._buffer is None or sizehint > len(self._buffer):
            self._new_buffer(abs(sizehint) + 1000)
        elif sizehint > len(self._buffer) - self._pos or len(self._buffer) == self._pos:
            self._pos = 0
        return self._buffer_view[self._pos:]

    def buffer_updated(self, nbytes: int) -> None:
        new_pos = self._pos + nbytes
        self._data_received(self._buffer[self._pos:new_pos])
        self._pos = new_pos

    def _data_received(self, data: bytearray):
        for event in self.connection.feed_data(data):
            self._pkt_waiters[event.seq_id].set_result(event)
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
        self._pause_waiter.clear()

    def resume_writing(self) -> None:
        self._pause_waiter.set()

    async def drain(self):
        await self._pause_waiter.wait()

    async def close(self):
        self.transport.close()
        await self.wait_closed()

    async def wait_closed(self):
        return await self._close_waiter

    async def raw_send(self, data: bytes):
        """
        原样发送
        """
        async with self._lock:
            self.transport.write(data)
            await self.drain()

    async def send(self, data: bytes):
        """
        发送4字节长度（包括自己）再发送payload
        """
        data = self.connection.send(data)
        await self.raw_send(data)

    async def _fetch_qrcode(self) -> TransEmpResponse:
        seq_id, data = self.connection.fetch_qrcode()
        self._pkt_waiters[seq_id] = asyncio.get_running_loop().create_future()
        await self.raw_send(data)
        try:
            return await self._pkt_waiters[seq_id]
        finally:
            del self._pkt_waiters[seq_id]

    # -------------公开方法--------------
    async def fetch_qrcode(self):
        return await timeout(self.connection.config.timeout)(self._fetch_qrcode)()

    # ----------------子类应该实现的回调--------------------
    async def on_group_message(self, msg):
        pass

    async def on_private_message(self, msg):
        pass
