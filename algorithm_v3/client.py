# client.py
import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('141.223.108.158', 65432))

    print("Enter the barcode info (type 'done' to finish):")
    while True:
        user_input = input("Enter barcode ID (1-88): ")
        client_socket.sendall(user_input.encode())
        if user_input.lower() == 'done':
            break
        data = client_socket.recv(1024)
        print(f"Server: {data.decode()}")

    client_socket.close()

if __name__ == "__main__":
    main()
