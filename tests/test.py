import time

from siomirai import Device, Engine

device = Device.random()
print(str(device))
engine = Engine(device, 1)

# 如果发了很多 req，应该等待相同 seq_id 的 response 这里可以使用callback
# 因为这里只发一个 pkt，所以忽略 seq_id

HOST = '42.81.176.211'  # The server's hostname or IP address
PORT = 443  # The port used by the server
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    pkt = engine.build_qrcode_fetch_request_packet()
    b = engine.encode_packet(pkt)
    s.sendall((len(b) + 4).to_bytes(4, byteorder='big'))
    s.sendall(b)

    length = int.from_bytes(s.recv(4), 'big')
    data = s.recv(length - 4)
    resp_pkt = engine.decode_packet(data)
    resp = engine.decode_trans_emp_response(resp_pkt.body)

    with open("qrcode.png", "wb") as f:
        f.write(resp.image_fetch.image)
    print("qrcode.png")

    sig = resp.image_fetch.sig
    while True:
        pkt = engine.build_qrcode_result_query_request_packet(sig)
        b = engine.encode_packet(pkt)
        s.sendall((len(b) + 4).to_bytes(4, byteorder='big'))
        s.sendall(b)
        length = int.from_bytes(s.recv(4), 'big')
        data = s.recv(length - 4)
        resp_pkt = engine.decode_packet(data)
        resp = engine.decode_trans_emp_response(resp_pkt.body)
        if resp.waiting_for_scan:
            print("waiting_for_scan")
        if resp.waiting_for_confirm:
            print("waiting_for_confirm")
        if resp.timeout:
            print("timeout")
        if resp.canceled:
            print("canceled")
        if resp.confirmed:
            print("confirmed")
            pkt = engine.build_qrcode_login_packet(
                resp.confirmed.tmp_pwd,
                resp.confirmed.tmp_no_pic_sig,
                resp.confirmed.tgt_qr
            )
            b = engine.encode_packet(pkt)
            s.sendall((len(b) + 4).to_bytes(4, byteorder='big'))
            s.sendall(b)
            length = int.from_bytes(s.recv(4), 'big')
            data = s.recv(length - 4)
            resp_pkt = engine.decode_packet(data)
            resp = engine.decode_login_response(resp_pkt.body)
            if resp.device_lock_login:
                pkt = engine.build_device_lock_login_packet()
                b = engine.encode_packet(pkt)
                s.sendall((len(b) + 4).to_bytes(4, byteorder='big'))
                s.sendall(b)
                length = int.from_bytes(s.recv(4), 'big')
                data = s.recv(length - 4)
                resp_pkt = engine.decode_packet(data)
                resp = engine.decode_login_response(resp_pkt.body)
                pass

            print(resp.success.account_info.nick)
            print(resp.success.account_info.age)
            print(resp.success.account_info.gender)

        time.sleep(2)