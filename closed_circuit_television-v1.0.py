import cv2 as cv
import numpy as np
import csv
import os
from datetime import datetime, timedelta

# Paths to the model files
humanProto = "MobileNetSSD_deploy.prototxt"
humanModel = "MobileNetSSD_deploy.caffemodel"
# Load human detection model
humanNet = cv.dnn.readNetFromCaffe(humanProto, humanModel)

def analyze_frame(frame, csv_writer, person_count, captured_frames):
    # Prepare the frame for human detection
    blob = cv.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

    # Set the input for humanNet
    humanNet.setInput(blob)
    # Perform human detection
    detections = humanNet.forward()

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Process each detected human
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        # Filter out weak detections
        if confidence > 0.5:
            print("Human detected!")
            # Get the coordinates of the detected human
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")

            # Ensure the coordinates are within the frame boundaries
            if startX < 0: startX = 0
            if startY < 0: startY = 0
            if endX > frame.shape[1]: endX = frame.shape[1]
            if endY > frame.shape[0]: endY = frame.shape[0]

            # Extract the human ROI
            human = frame[startY:endY, startX:endX]

            # Ensure the ROI is not empty before saving
            if human.size > 0 and captured_frames < 10:
                # Save the frame as an image
                filename = f"person_{timestamp}_{person_count}.jpg"
                cv.imwrite(filename, human)
                print(f"Saved {filename}")

                # Write the output to CSV file
                csv_writer.writerow([timestamp, filename, startX, startY, endX, endY])

                # Draw the bounding box on the frame
                cv.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv.putText(frame, f"Person detected at: {timestamp}", (startX, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                captured_frames += 1

    return frame, captured_frames

def analyze_video():
    # Initialize video capture from the default camera (usually 0)
    cap = cv.VideoCapture(0)

    # Create a CSV file and writer
    with open('human_detection.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Timestamp', 'Filename'])
        person_count = 0

        # Process frames continuously
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture frame")
                break

            captured_frames = 0

            # Capture images for 2 seconds whenever a person is detected
            end_time = datetime.now() + timedelta(seconds=2)
            while datetime.now() < end_time:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame")
                    break
                frame_with_info, captured_frames = analyze_frame(frame, csv_writer, person_count, captured_frames)
                cv.imshow('Frame', frame_with_info)
                if cv.waitKey(1) == ord('q'):
                    break

            person_count += 1

            # Display the resulting frame
            cv.imshow('Frame', frame_with_info)
            if cv.waitKey(1) == ord('q'):
                break

    # Release the capture
    cap.release()
    cv.destroyAllWindows()

# Start video analysis
analyze_video()
