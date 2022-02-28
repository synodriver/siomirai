import sys

sys.path.append("../")
sys.path.append("../asyncio/")

import asyncio
from typing import cast

from siomirai.asyncio import BaseClientProtocol
from siomirai.config import Config, Protocol
from siomirai import Device
from siomirai.events import LoginResponse


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
    while True:
        event = await protocol.query_qrcode_result(sig)
        if event.resp.waiting_for_scan:
            print("waiting_for_scan")
        if event.resp.waiting_for_confirm:
            print("waiting_for_confirm")
        if event.resp.timeout:
            print("timeout")
        if event.resp.canceled:
            print("canceled")
        if event.resp.confirmed:
            print("confirmed")
            break
        await asyncio.sleep(2)
    resp: LoginResponse = await protocol.qrcode_login(event.resp.confirmed.tmp_pwd,
                                                      event.resp.confirmed.tmp_no_pic_sig,
                                                      event.resp.confirmed.tgt_qr)
    if resp.device_lock_login:
        resp = await protocol.device_lock_login()

    print(resp.success.account_info.nick)
    print(resp.success.account_info.age)
    print(resp.success.account_info.gender)
    ev = await protocol.client_register()
    print(ev)
    ev = await protocol.update_signature("test signature")
    print(ev)


asyncio.run(main())
