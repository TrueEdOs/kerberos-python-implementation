import socket
import des

client_host = 'localhost'
client_port = 20000

as_host = 'localhost'
as_port = 20001

key_c = b'THISKEY'
key_c_tgs = b'CTGSKEY'
key_as_tgs = b'ASTGSKY'

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((as_host, as_port))

t = bytes([0, 0, 0, 0])
p = bytes([255, 255, 255, 255])
tgs = bytes([1, 1, 1, 1])

c = (socket.recvfrom(1024)[0])

if c != b'BTCH':
    print("ID WRONG")
    exit(0)

print("RECEIVED C_ID: ", c)

tgt = c + tgs + t + p + key_c_tgs
print("TGT IS ", tgt)
msg = des.encrypt_bytes(des.encrypt_bytes(tgt, key_as_tgs) + key_c_tgs, key_c)

print("SENDING TGT TO K_C_TGS. MSG: ", msg)
socket.sendto(msg, (client_host, client_port))

