import json
from kafka import KafkaProducer
from get_data import receive_data_from_client

def send_data_to_kafka(mapped_data):
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    topic = 'output_topic'
    producer.send(topic, {'sorted_pkg_ids': list(mapped_data.keys())})
    producer.flush()
    print(f"Data sent to Kafka topic '{topic}'.")

def main():
    # Receive data from the client
    mapped_data = receive_data_from_client()

    # Load and print the mapped barcodes
    output_filename = 'data/mapped_barcodes.json'
    with open(output_filename, 'r') as file:
        mapped_data = json.load(file)
        print("Mapped Barcodes Information:")

        # Extract all IDs from the JSON data
        ids = list(mapped_data.keys())

        # Print the list of IDs
        print("List of IDs in mapped_barcodes.json:")
        print(ids)

    # Send data to Kafka
    send_data_to_kafka(mapped_data)

if __name__ == "__main__":
    main()


# # server.py
# import json
# from get_data import receive_data_from_client

# def main():
#     # Receive data from the client
#     receive_data_from_client()

#     # Load and print the mapped barcodes
#     output_filename = 'data/mapped_barcodes.json'
#     with open(output_filename, 'r') as file:
#         mapped_data = json.load(file)
#         print("Mapped Barcodes Information:")

#         # Extract all IDs from the JSON data
#         ids = list(mapped_data.keys())

#         # Print the list of IDs
#         print("List of IDs in mapped_barcodes.json:")
#         print(ids)

# if __name__ == "__main__":
#     main()
