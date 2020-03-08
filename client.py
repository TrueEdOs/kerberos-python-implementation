import socket
import des

client_host = 'localhost'
client_port = 20000

as_host = 'localhost'
as_port = 20001

tgs_host = 'localhost'
tgs_port = 20002

ss_host = 'localhost'
ss_port = 20003

key_c = b'THISKEY'

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((client_host, client_port))

c = b'BTCH'
t = bytes([0, 0, 0, 0])
id_ss = bytes([33, 0, 0, 0])

print("SENDING C_ID: ", c)
socket.sendto(c, (as_host, as_port))

msg = socket.recvfrom(1024)[0]

print("RECEIVED TGT AND K_C_TGS. MSG: ", msg)

d_msg = des.decrypt_bytes(msg, key_c)

tgt, key_c_tgs = d_msg[:24], d_msg[24:-1]

print("KEY_C_TGS", key_c_tgs)

msg = tgt + des.encrypt_bytes(c + t, key_c_tgs) + id_ss

print("SENDING MSG TO TGS: ", msg)
socket.sendto(msg, (tgs_host, tgs_port))

msg = socket.recvfrom(1024)[0]
d_msg = des.decrypt_bytes(msg, key_c_tgs)

tgs, key_c_ss = d_msg[:24], d_msg[24:-1]

print("KEY_C_SS", key_c_ss)

msg = tgs + des.encrypt_bytes(c + t, key_c_tgs)

print("SENDING MSG TO SS: ", msg)
socket.sendto(msg, (ss_host, ss_port))

msg = socket.recvfrom(1024)[0]
d_msg = des.decrypt_bytes(msg, key_c_ss)

if d_msg[4:] == bytes([0, 0, 0, 1]):
    print("CONNECTION ESTABLISHED")