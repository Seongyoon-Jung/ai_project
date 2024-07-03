# bluetooth_client.py
import cv2
from ultralytics import YOLO, solutions
import bluetooth

def send_message_to_server(message, address, port):
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((address, port))
        sock.send(message)
        sock.close()
        print(f"Sent message: {message} to server at {address}:{port}")
    except Exception as e:
        print(f"Failed to send message to server: {e}")

class CustomObjectCounter(solutions.ObjectCounter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.person_count = 0
        self.previous_person_count = 0

    def start_counting(self, frame, tracks):
        frame = super().start_counting(frame, tracks)

        for track in tracks:
            if isinstance(track, dict) and 'class' in track:
                if track['class'] == 0:  # Assuming class ID 0 is for 'person'
                    if self._is_passing_line(track):
                        self.person_count += 1

        if self.person_count > self.previous_person_count:
            send_message_to_server('person_passed', 'XX:XX:XX:XX:XX:XX', 1)  # Replace 'XX:XX:XX:XX:XX:XX' with the server's Bluetooth address
"counting_client.py" 90 lines, 3311 bytes