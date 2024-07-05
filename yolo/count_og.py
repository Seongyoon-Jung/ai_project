import cv2
from ultralytics import YOLO, solutions

def main(weights="yolov8n.pt", source=0, save_output=False):
    # Load the pre-trained YOLOv8 model
    model = YOLO(weights)

    # Open the webcam (usually 0 is the default webcam)
    cap = cv2.VideoCapture(source)
    assert cap.isOpened(), "Error opening webcam"

    # Get video properties: width, height, and frames per second (fps)
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    # Define points for a line or region of interest in the middle of the frame
    line_points = [(w // 2, 0), (w // 2, h)]  # Vertical line coordinates in the middle

    # Specify classes to count, for example: person (0) and car (2)
    classes_to_count = [0]  # Class IDs for person and car

    # Initialize the video writer to save the output video
    video_writer = None
    if save_output:
        video_writer = cv2.VideoWriter("webcam_object_counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    # Initialize the Object Counter with visualization options and other parameters
    counter = solutions.ObjectCounter(
        view_img=True,  # Display the image during processing
        reg_pts=line_points,  # Region of interest points
        classes_names=model.names,  # Class names from the YOLO model
        draw_tracks=True,  # Draw tracking lines for objects
        line_thickness=2,  # Thickness of the lines drawn
    )

    # Process video frames in a loop
    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Failed to capture image from webcam. Exiting.")
            break

        # Perform object tracking on the current frame, filtering by specified classes
        tracks = model.track(im0, persist=True, show=False, classes=classes_to_count)

        # Use the Object Counter to count objects in the frame and get the annotated image
        im0 = counter.start_counting(im0, tracks)

        # Write the annotated frame to the output video
        if save_output:
            video_writer.write(im0)

        # Display the resulting frame
        cv2.imshow("Webcam Object Counting", im0)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and writer objects
    cap.release()
    if save_output:
        video_writer.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Webcam Object Counting with YOLOv8")
    parser.add_argument("--weights", type=str, default="yolov8n.pt", help="Path to the YOLOv8 weights file")
    parser.add_argument("--source", type=int, default=0, help="Webcam source (default is 0)")
    parser.add_argument("--save-output", action="store_true", help="Save the output video")

    args = parser.parse_args()
    main(weights=args.weights, source=args.source, save_output=args.save_output)

