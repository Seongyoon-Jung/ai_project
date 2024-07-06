import socket

# 서버(컴퓨터)의 IP 주소와 포트 번호
HOST = '141.223.108.158' # 서버의 IP 주소
PORT = 65432           # 서버에서 사용한 동일한 포트 번호

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("보낼 메시지: ")
        s.sendall(message.encode())
        if message.lower() == 'exit':
            break
