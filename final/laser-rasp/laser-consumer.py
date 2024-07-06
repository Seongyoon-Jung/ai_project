import socket
import time
import serial
from kafka import KafkaConsumer
import json

# 블루투스 모듈의 시리얼 포트와 속도 설정
ser = serial.Serial('/dev/tty.HC-05', 9600)  # 'tty.HC-05'를 실제 블루투스 포트로 변경
time.sleep(2)  # 연결 대기

def send_number_to_arduino(number):
    ser.write(f"{number}\n".encode())
    print(f"Sent number to Arduino: {number}")

def main():
    # 서버의 IP 주소와 포트 번호
    SERVER_HOST = '192.168.0.42'  # 서버의 IP 주소
    SERVER_PORT = 65433        # 서버의 포트 번호

    # 서버 소켓 생성 및 바인드
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    
    print(f"Listening for connections on {SERVER_HOST}:{SERVER_PORT}...")

    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # 카프카 컨슈머 설정
    consumer = KafkaConsumer('output_topic',
                             bootstrap_servers='141.223.108.158:9092',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                             group_id='laser_consumer_group')

    print("Waiting for processed messages...")
    sorted_pkg_ids = []

    # 카프카에서 데이터를 받아와 sorted_pkg_ids 리스트 채우기
    for message in consumer:
        data = message.value
        sorted_pkg_ids = data['sorted_pkg_ids']
        print(f"Received sorted pkg_ids: {sorted_pkg_ids}")

        # 클라이언트로부터 passed 메시지를 수신하여 처리
        while sorted_pkg_ids:
            data = client_socket.recv(1024).decode()
            if data == 'passed':
                print("Received 'passed' message")
                if sorted_pkg_ids:
                    num = sorted_pkg_ids.pop(0)
                    send_number_to_arduino(num)
                    time.sleep(1)  # 아두이노로 데이터를 전송한 후 잠시 대기
                else:
                    print("No sorted package IDs available to send")

if __name__ == "__main__":
    main()
