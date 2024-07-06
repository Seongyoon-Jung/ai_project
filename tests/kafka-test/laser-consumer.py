# laser-consumer.py

from kafka import KafkaConsumer
import json
import time
import serial

# 블루투스 모듈의 시리얼 포트와 속도 설정
ser = serial.Serial('/dev/tty.HC-05', 9600)  # 'tty.HC-05'를 실제 블루투스 포트로 변경
time.sleep(2)  # 연결 대기

def send_number_to_arduino(number):
    ser.write(f"{number}\n".encode())
    print(f"Sent number to Arduino: {number}")

def main():
    consumer = KafkaConsumer('output_topic',
                             bootstrap_servers='141.223.108.158:9092',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                             group_id='laser_consumer_group')

    print("Waiting for processed messages...")
    sorted_pkg_ids = []

    for message in consumer:
        data = message.value
        sorted_pkg_ids = data['sorted_pkg_ids']
        print(f"Received sorted pkg_ids: {sorted_pkg_ids}")

        while sorted_pkg_ids:
            input("Press Enter to send the next number...")
            num = sorted_pkg_ids.pop(0)
            send_number_to_arduino(num)
            time.sleep(1)  # 아두이노로 데이터를 전송한 후 잠시 대기

if __name__ == "__main__":
    main()
