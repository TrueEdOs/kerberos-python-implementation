import socket
import des

client_host = 'localhost'
client_port = 20000

tgs_host = 'localhost'
tgs_port = 20002

t = bytes([0, 0, 0, 0])
p = bytes([255, 255, 255, 255])

key_as_tgs = b'ASTGSKY'
key_tgs_ss = b'TGSSKEY'
key_c_ss = b'CSS_KEY'

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((tgs_host, tgs_port))

msg = socket.recvfrom(1024)[0]
print("RECEIVING TGT TO K_C_TGS. MSG: ", msg)

tgt, auth1, id_ss = msg[:24], msg[24:32], msg[32:]

e_tgt = des.decrypt_bytes(tgt, key_as_tgs)[:-1]
c, key_c_tgs = e_tgt[:4], e_tgt[16:]

print("TGT IS ", e_tgt)
tgs = c + id_ss + t + p + key_c_ss

msg = des.encrypt_bytes(des.encrypt_bytes(tgs, key_tgs_ss) + key_c_ss, key_c_tgs)
socket.sendto(msg, (client_host, client_port))