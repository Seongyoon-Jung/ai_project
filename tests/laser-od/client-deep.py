import cv2
from ultralytics import YOLO
import time
import socket
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load the pre-trained YOLOv8 model
model = YOLO("best.pt")

# Open the webcam (usually 0 is the default webcam)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error opening webcam")
    exit()

# Get video properties: width, height, and frames per second (fps)
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Define points for a line or region of interest in the middle of the frame
line_points = [(w // 2, 0), (w // 2, h)]  # Vertical line coordinates in the middle

# Specify classes to count, for example: person (0) and car (2)
classes_to_count = [0]  # Class IDs for box

# Initialize DeepSORT tracker
deepsort = DeepSort(max_age=30, n_init=3, nn_budget=100)

# 서버의 IP 주소와 포트 번호
SERVER_HOST = '192.168.0.25'  # 서버의 IP 주소 (실습실: '192.168.0.42', 시연장:192.168.0.25)
SERVER_PORT = 65433  # 서버의 포트 번호

# 서버에 연결
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_HOST, SERVER_PORT))

# Process video frames in a loop
frame_count = 0
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    # Perform object detection on the current frame
    results = model(im0)
    
    # Extract bounding boxes and confidences
    bboxes = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].numpy().astype(int)
            width, height = x2 - x1, y2 - y1
            conf = box.conf.item()
            cls = box.cls.item()
            if int(cls) in classes_to_count and conf > 0.3:  # Only consider specified classes with confidence >= 0.3
                bboxes.append([x1, y1, width, height, conf])

    # Perform object tracking using DeepSORT
    tracks = deepsort.update_tracks(bboxes, frame=im0)
    
    for track in tracks:
        if not track.is_confirmed() or track.time_since_update > 1:
            continue
        
        track_id = track.track_id
        bbox = track.to_tlbr()  # Get the bounding box in (x1, y1, x2, y2) format
        
        # Draw the bounding box and label
        x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        class_id = int(track.class_id)
        label = f"{model.names[class_id]} {track_id}"
        cv2.rectangle(im0, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(im0, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Check if the object crosses the center line
        center_x = (x1 + x2) // 2
        if center_x > line_points[0][0]:
            count += 1
            print(f"Box count: {count}")

            # Check for IN count changes to send message to server
            sock.sendall(b"passed")
    
    # Draw the center line
    cv2.line(im0, line_points[0], line_points[1], (0, 255, 0), 2)
    
    # Display the frame
    cv2.imshow('Webcam Object Counting', im0)
    
    # Print frame processing status
    frame_count += 1
    if frame_count % 10 == 0:
        print(f"Processed {frame_count} frames")

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()

# Close the socket
sock.close()
