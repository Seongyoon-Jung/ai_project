import socket
import json

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

def main():
    json_filename = './generated_boxes.json'
    output_filename = './mapped_barcodes.json'

    # Load the existing JSON file
    json_data = load_json_file(json_filename)

    # Setup server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('141.223.108.158', 65432))
    server_socket.listen(1)
    print("Server is listening on port 65432...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    barcode_input = []
    
    while True:
        data = conn.recv(1024).decode()
        if data.lower() == 'done':
            break
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

    mapped_info = map_barcodes_to_info(barcode_input, json_data)
    save_json_file(output_filename, mapped_info)
    print(f"Mapped information saved to {output_filename}")

    conn.close()

if __name__ == "__main__":
    main()
