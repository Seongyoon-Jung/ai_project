import json
from kafka import KafkaProducer
from get_data import receive_data_from_client, map_barcodes_to_info, load_json_file, save_json_file
import socket

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

def main():
    json_filename = 'data/generated_boxes.json'
    json_data = load_json_file(json_filename)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('141.223.108.158', 65432))
    server_socket.listen(1)
    print("Server is listening on port 65432...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        handle_client_connection(conn, json_data)
        conn.close()

if __name__ == "__main__":
    main()


# import json
# from kafka import KafkaProducer
# from get_data import receive_data_from_client, map_barcodes_to_info, load_json_file, save_json_file
# import socket

# def send_data_to_kafka(mapped_data):
#     producer = KafkaProducer(bootstrap_servers='localhost:9092',
#                              value_serializer=lambda v: json.dumps(v).encode('utf-8'))
#     topic = 'output_topic'
#     producer.send(topic, {'sorted_pkg_ids': list(mapped_data.keys())})
#     producer.flush()
#     print(f"Data sent to Kafka topic '{topic}'.")

# def handle_client_connection(conn, json_data):
#     barcode_input = []
#     while True:
#         try:
#             data = conn.recv(1024).decode().strip()
#             if not data:
#                 continue
#             if data.lower() == 'done':
#                 print("Received 'done'. Processing data...")
#                 mapped_info = map_barcodes_to_info(barcode_input, json_data)
#                 save_json_file('data/mapped_barcodes.json', mapped_info)
#                 send_data_to_kafka(mapped_info)
#                 barcode_input = []  # Reset for next round of inputs
#                 conn.sendall(b"Processing done. Continue entering barcode IDs.")
#                 continue
#             if data.lower() == 'exit':
#                 print("Client requested exit. Closing connection.")
#                 break
#             print(f"Received data: {data}")
#             try:
#                 barcode_id = int(data)
#                 if barcode_id < 1 or barcode_id > 88:
#                     conn.sendall(b"ID must be between 1 and 88.")
#                     continue
#                 barcode_input.append(str(barcode_id))
#             except ValueError:
#                 conn.sendall(b"Please enter a valid number.")
#                 continue
#             conn.sendall(b"Barcode received.")
#         except BrokenPipeError:
#             print("BrokenPipeError: Connection was closed by the client.")
#             break

# def main():
#     json_filename = 'data/generated_boxes.json'
#     json_data = load_json_file(json_filename)

#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(('141.223.108.158', 65432))
#     server_socket.listen(1)
#     print("Server is listening on port 65432...")

#     while True:
#         conn, addr = server_socket.accept()
#         print(f"Connected by {addr}")
#         handle_client_connection(conn, json_data)
#         conn.close()

# if __name__ == "__main__":
#     main()
