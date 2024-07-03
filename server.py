# bluetooth_server.py
import bluetooth

def start_server():
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = bluetooth.PORT_ANY
    server_socket.bind(("", port))
    server_socket.listen(1)

    port = server_socket.getsockname()[1]
    bluetooth.advertise_service(server_socket, "SampleServer",
                                service_id=str(port),
                                service_classes=[bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE])

    print(f"Waiting for connection on RFCOMM channel {port}")

    client_socket, client_info = server_socket.accept()
    print(f"Accepted connection from {client_info}")

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
