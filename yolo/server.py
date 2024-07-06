#server.py
import socket

# 서버의 IP 주소와 포트 번호
HOST = '0.0.0.0'  # 모든 IP 주소에서 연결을 허용합니다.
PORT = 65432      # 사용할 포트 번호

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"서버가 {PORT} 포트에서 대기 중입니다...")
    conn, addr = s.accept()
    with conn:
        print('연결됨:', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('받은 데이터:', data.decode())
