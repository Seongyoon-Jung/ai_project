import socket

# 컴퓨터(서버)의 IP 주소와 포트 번호
HOST = '컴퓨터의_IP주소'  # 예: '192.168.0.10'
PORT = 65432              # 서버에서 사용한 동일한 포트 번호

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("보낼 메시지: ")
        s.sendall(message.encode())
        if message.lower() == 'exit':
            break
