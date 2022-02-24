import asyncio
from typing import cast

from siomirai.asyncio.protocol import BaseClientProtocol
from siomirai.config import Config, Protocol
from siomirai import Device


async def main():
    loop = asyncio.get_running_loop()
    _, protocol = await loop.create_connection(lambda: BaseClientProtocol(Config(timeout=10, device=Device.random())),
                                               '42.81.176.211',
                                               443)
    protocol = cast(BaseClientProtocol, protocol)
    event = await protocol.fetch_qrcode()
    with open("qrcode.png", "wb") as f:
        f.write(event.resp.image_fetch.image)
        sig = event.resp.image_fetch.sig
    # while True:
    #     event = await protocol.query_qrcode_result(sig)
    #     await asyncio.sleep(1)
    await protocol.login_qrcode()
    pass

asyncio.run(main())