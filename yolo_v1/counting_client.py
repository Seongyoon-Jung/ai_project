import cv2
from ultralytics import YOLO, solutions
import time
import socket

# Load the pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")

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
classes_to_count = [0, 2]  # Class IDs for person and car

# Initialize the Object Counter with visualization options and other parameters
counter = solutions.ObjectCounter(
    view_img=True,  # Display the image during processing
    reg_pts=line_points,  # Region of interest points
    classes_names=model.names,  # Class names from the YOLO model
    draw_tracks=True,  # Draw tracking lines for objects
    line_thickness=2,  # Thickness of the lines drawn
    view_in_counts=True,
    view_out_counts=True,
)

# Initialize the log file
log_file = "object_count_log.txt"
with open(log_file, "w") as f:
    f.write("Timestamp, Class, IN, OUT\n")

# Previous IN and OUT counts to detect changes
previous_counts = {model.names[class_id]: {"IN": 0, "OUT": 0} for class_id in classes_to_count}

# 서버의 IP 주소와 포트 번호
SERVER_HOST = '192.168.0.42'  # 서버의 IP 주소
SERVER_PORT = 65433        # 서버의 포트 번호

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

    # Perform object tracking on the current frame, filtering by specified classes
    results = model.track(im0, persist=True, show=False, classes=classes_to_count)

    # Use the Object Counter to count objects in the frame and get the annotated image
    im0 = counter.start_counting(im0, results)

    # Check for IN and OUT count changes and log them
    for class_id in classes_to_count:
        class_name = model.names[class_id]
        current_in_count = counter.class_wise_count.get(class_name, {}).get("IN", 0)
        current_out_count = counter.class_wise_count.get(class_name, {}).get("OUT", 0)
        if current_in_count > previous_counts[class_name]["IN"] or current_out_count > previous_counts[class_name]["OUT"]:
            with open(log_file, "a") as f:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp}, {class_name}, {current_in_count}, {current_out_count}\n")
                
            # Check for IN count changes to send message to server
            if current_in_count > previous_counts[class_name]["IN"]:
                sock.sendall(b"passed")
            
            previous_counts[class_name]["IN"] = current_in_count
            previous_counts[class_name]["OUT"] = current_out_count

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
