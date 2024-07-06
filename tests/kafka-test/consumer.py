from kafka import KafkaConsumer
import json

# 브로커의 외부 IP와 포트를 설정합니다.
broker_address = '141.223.108.158:9092'  # 브로커의 외부 IP와 포트로 변경하세요.
topic_name = 'quickstart-events'

# KafkaConsumer 생성
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[broker_address],
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# 메시지 소비
for message in consumer:
    print(f"Message received: {message.value}")

