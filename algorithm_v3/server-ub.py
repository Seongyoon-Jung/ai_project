import json
from get_data import receive_data_from_client

def batch_process_keys(data, batch_size):
    """
    Generator function to yield keys in batches.
    """
    keys = list(data.keys())
    for i in range(0, len(keys), batch_size):
        yield keys[i:i + batch_size]

def process_batch(keys, data):
    """
    Process a batch of keys and print their corresponding values.
    """
    batch_data = {key: data[key] for key in keys}
    print("Processing batch:")
    print(json.dumps(batch_data, indent=4))

def main():
    # Receive data from the client
    receive_data_from_client()

    # Load and print the mapped barcodes
    output_filename = './mapped_barcodes.json'
    with open(output_filename, 'r') as file:
        mapped_data = json.load(file)
        print("Mapped Barcodes Information:")

        # Batch size for processing
        batch_size = 2

        # Batch process the keys
        for batch_keys in batch_process_keys(mapped_data, batch_size):
            process_batch(batch_keys, mapped_data)

if __name__ == "__main__":
    main()
