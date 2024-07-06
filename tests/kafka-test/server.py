from kafka import KafkaConsumer
import json
from get_data import map_barcodes_to_info, load_json_file, save_json_file, send_data_to_kafka

def main():
    json_filename = 'data/generated_boxes.json'
    json_data = load_json_file(json_filename)

    # Kafka 컨슈머 설정
    consumer = KafkaConsumer(
        'input_topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        barcode_data = message.value['barcode_id']
        print(f"Received barcode data: {barcode_data}")
        # 바코드 데이터를 처리
        barcode_input = [barcode_data]  # 단일 바코드 데이터 처리 예시
        mapped_info = map_barcodes_to_info(barcode_input, json_data)
        save_json_file('data/mapped_barcodes.json', mapped_info)
        send_data_to_kafka(mapped_info)
        print("Processed and sent data to Kafka.")

if __name__ == "__main__":
    main()
