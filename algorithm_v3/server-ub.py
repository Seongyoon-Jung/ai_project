import json
from get_data import receive_data_from_client

def main():
    # Receive data from the client
    receive_data_from_client()

    # Load and print the mapped barcodes
    output_filename = './generated_boxes.json'
    with open(output_filename, 'r') as file:
        mapped_data = json.load(file)
        print("Generated Barcodes Information:")

        # Extract all IDs from the JSON data
        ids = list(mapped_data.keys())

        # Print the list of IDs
        print("List of IDs in generated_barcodes.json:")
        print(ids)

if __name__ == "__main__":
    main()
