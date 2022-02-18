from rqpy import Device, Engine

device = Device.random()
print(device.__str__())
engine = Engine(device, 1)

pkt = engine.build_qrcode_fetch_request_packet()
# 如果发了很多 req，应该等待相同 seq_id 的 response 这里可以使用callback
# 因为这里只发一个 pkt，所以忽略 seq_id
print(pkt.seq_id)
print(pkt)
b = engine.encode_packet(pkt)

HOST = '42.81.176.211'  # The server's hostname or IP address
PORT = 443  # The port used by the server
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall((len(b) + 4).to_bytes(4, byteorder='big'))
    s.sendall(b)
    length = int.from_bytes(s.recv(4), 'big')
    data = s.recv(length - 4)
    resp_pkt = engine.decode_packet(data)
    print(resp_pkt.seq_id)
    resp = engine.decode_trans_emp_response(resp_pkt.body)
    with open("qrcode.png", "wb") as f:
        f.write(resp.image_fetch.image)
        print("qrcode.png")
