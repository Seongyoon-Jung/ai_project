import json
from get_data import receive_data_from_client

def main():
    # Receive data from the client
    receive_data_from_client()

    # Load and print the mapped barcodes
    output_filename = './mapped_barcodes.json'
    with open(output_filename, 'r') as file:
        mapped_data = json.load(file)
        print("Mapped Barcodes Information:")
        print(json.dumps(mapped_data, indent=4))

if __name__ == "__main__":
    main()
