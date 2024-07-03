import cv2
from ultralytics import YOLO, solutions
import asyncio
from bleak import BleakClient

async def send_message_to_server(message, address):
    client = BleakClient(address)
    try:
        await client.connect()
        print(f"Connected to server at {address}")
        await client.write_gatt_char(message)
        print(f"Sent message: {message} to server at {address}")
    except Exception as e:
        print(f"Failed to send message to server: {e}")
    finally:
        await client.disconnect()

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
            asyncio.run(send_message_to_server(b'person_passed', 'XX:XX:XX:XX:XX:XX'))  # Replace 'XX:XX:XX:XX:XX:XX' with the server's Bluetooth address
            self.previous_person_count = self.person_count

        return frame

    def _is_passing_line(self, track):
        center_x = track.get('center', (0, 0))[0]
        line_x = (frame.shape[1] // 2)
        return center_x > line_x

def main(weights="yolov8n.pt", source=0, save_output=False):
    model = YOLO(weights)
    cap = cv2.VideoCapture(source)
    assert cap.isOpened(), "Error opening webcam"

    w, h, fps = [int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS)]
    line_points = [(w // 2, 0), (w // 2, h)]
    classes_to_count = [0]

    video_writer = None
    if save_output:
        video_writer = cv2.VideoWriter("webcam_object_counting_output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    counter = CustomObjectCounter(
        view_img=False,
        reg_pts=line_points,
        classes_names=model.names,
        draw_tracks=True,
        line_thickness=2,
    )

    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Failed to capture image from webcam. Exiting.")
            break

        tracks = model.track(im0, persist=True, show=False, classes=classes_to_count)
        im0 = counter.start_counting(im0, tracks)

        if save_output:
            video_writer.write(im0)

    cap.release()
    if save_output:
        video_writer.release()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Webcam Object Counting with YOLOv8")
    parser.add_argument("--weights", type=str, default="yolov8n.pt", help="Path to the YOLOv8 weights file")
    parser.add_argument("--source", type=int, default=0, help="Webcam source (default is 0)")
    parser.add_argument("--save-output", action="store_true", help="Save the output video")

    args = parser.parse_args()
    main(weights=args.weights, source=args.source, save_output=args.save_output)
