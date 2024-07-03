# wifi_server.py
import socket

def start_server(host='192.168.0.52', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            print(f"Received message: {message}")
            if message == 'person_passed':
                print('passed')
    except OSError:
        pass

    print("Disconnected.")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
