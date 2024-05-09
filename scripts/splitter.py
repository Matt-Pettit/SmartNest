import cv2
import os
import time

def split_video(input_video, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the input video
    cap = cv2.VideoCapture(input_video)

    # Get the video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the number of frames per segment (30 seconds)
    frames_per_segment = int(fps * 15)

    # Loop through the frames and save segments
    segment_count = 0
    current_frame = 0
    success, frame = cap.read()

    while success:
        if current_frame % frames_per_segment == 0:
            segment_count += 1
            output_path = os.path.join(output_folder, f"segment_{segment_count}.mp4")
            out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps / 2, (frame.shape[1], frame.shape[0]))

        if current_frame % 2 == 0:  # Write every other frame
            out.write(frame)

        current_frame += 1
        success, frame = cap.read()

        if current_frame % frames_per_segment == 0:
            out.release()
            print(f"Created {output_path}")

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    input_video = "sample_footage.mp4"
    output_folder = "split"
    split_video(input_video, output_folder)