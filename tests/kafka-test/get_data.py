import json
from kafka import KafkaProducer
import socket

def load_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def map_barcodes_to_info(barcode_input, json_data):
    mapped_info = {}
    for barcode_id in barcode_input:
        if barcode_id in json_data:
            mapped_info[barcode_id] = json_data[barcode_id]
    return mapped_info

def save_json_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def send_data_to_kafka(mapped_data):
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    topic = 'output_topic'
    producer.send(topic, {'sorted_pkg_ids': list(mapped_data.keys())})
    producer.flush()
    print(f"Data sent to Kafka topic '{topic}'.")

def handle_client_connection(conn, json_data):
    barcode_input = []
    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                continue
            if data.lower() == 'done':
                print("Received 'done'. Processing data...")
                mapped_info = map_barcodes_to_info(barcode_input, json_data)
                save_json_file('data/mapped_barcodes.json', mapped_info)
                send_data_to_kafka(mapped_info)
                barcode_input = []  # Reset for next round of inputs
                conn.sendall(b"Processing done. Continue entering barcode IDs.")
                continue
            if data.lower() == 'exit':
                print("Client requested exit. Closing connection.")
                break
            print(f"Received data: {data}")
            try:
                barcode_id = int(data)
                if barcode_id < 1 or barcode_id > 88:
                    conn.sendall(b"ID must be between 1 and 88.")
                    continue
                barcode_input.append(str(barcode_id))
            except ValueError:
                conn.sendall(b"Please enter a valid number.")
                continue
            conn.sendall(b"Barcode received.")
        except BrokenPipeError:
            print("BrokenPipeError: Connection was closed by the client.")
            break
