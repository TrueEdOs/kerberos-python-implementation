import socket
import des

client_host = 'localhost'
client_port = 20000

ss_host = 'localhost'
ss_port = 20003

key_tgs_ss = b'TGSSKEY'

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind((ss_host, ss_port))

msg = socket.recvfrom(1024)[0]
print("RECEIVING TGS AND K_C_SS. MSG: ", msg)

tgs, auth2 = msg[:24], msg[24:]
e_tgs = des.decrypt_bytes(tgs, key_tgs_ss)[:-1]

c, key_c_ss = e_tgs[:4], e_tgs[16:]
print("KEY C_SS: ", key_c_ss)

msg = des.encrypt_bytes(c + bytes([0, 0, 0, 1]), key_c_ss)
socket.sendto(msg, (client_host, client_port))
