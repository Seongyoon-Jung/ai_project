import json
from kafka import KafkaProducer

def main():
    # Kafka 프로듀서 설정
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    topic = 'input_topic'

    print("Enter the barcode info (type 'done' to finish, 'exit' to quit):")
    while True:
        user_input = input("Enter barcode ID (1-88): ").strip()
        if user_input.lower() in {'done', 'exit'}:
            break
        try:
            barcode_id = int(user_input)
            if barcode_id < 1 or barcode_id > 88:
                print("ID must be between 1 and 88.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        # Kafka로 데이터 전송
        producer.send(topic, {'barcode_id': barcode_id})
        producer.flush()
        print(f"Sent barcode ID {barcode_id} to Kafka.")

    producer.close()
    print("Client exiting...")

if __name__ == "__main__":
    main()
