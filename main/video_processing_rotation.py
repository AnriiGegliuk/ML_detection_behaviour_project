############################### Importing all necessary libraries ###############################
import numpy as np
import cv2
import os
import json
import ffmpeg
import shutil

############################### Defining a function for video analysis ###############################
def process_video(video_file_path, num_frames=100):
    # Open the video file
    cap = cv2.VideoCapture(video_file_path)

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Generate random frame indices to process
    frame_indices = np.random.randint(0, total_frames, num_frames)

    # Get the height and width of the video as a NumPy array
    frame_dimensions = np.array([int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                                  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))])

    # Calculate the midpoint of the frame width
    width_half = frame_dimensions[1] // 2

    # Initialize the average brightness values for the left and right halves of the frames
    left_half_avg = 0
    right_half_avg = 0

    # Process each randomly selected frame
    for idx in frame_indices:
        # Set the current frame to be read
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        # Read the frame from the video
        ret, frame = cap.read()
        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Update the average brightness of the left and right halves of the frames
        left_half_avg += np.sum(gray_frame[:, :width_half]) / (frame_dimensions[0] * width_half)
        right_half_avg += np.sum(gray_frame[:, width_half:]) / (frame_dimensions[0] * width_half)

    # Close the video file
    cap.release()

    # Calculate the final average brightness values for the left and right halves of the frames
    left_half_avg /= num_frames
    right_half_avg /= num_frames

    # Determine if the video is flipped based on the average brightness of the halves
    is_flipped = right_half_avg < left_half_avg

    # Return whether the video is flipped
    return is_flipped



############################### Flip the input video horizontally ############################### 
def flip_video(video_file_path):

    # Generate the flipped video's file path by appending "_flipped.avi" to the input video's name

    flipped_video_file_path = os.path.splitext(video_file_path)[0] + "_flipped.avi"

    # # Creating a new ffmpeg stream to read the input video
    stream = ffmpeg.input(video_file_path)
    # Apply horizontal flip to the stream
    stream = ffmpeg.hflip(stream)
    # Save the flipped video to a new file in .avi format and h264_nvenc options
    stream = ffmpeg.output(stream, flipped_video_file_path, format="avi", vcodec="h264_nvenc", qscale=0)
    ffmpeg.run(stream)
    return flipped_video_file_path  # Add this line

############################### Create a JSON file ###############################
def create_json_file(file_path, data):
    # Open the file for writing and dump the data to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

############################### Path to the folder for analysis ############################### 
root_dir = r'C:\Users\andri\PycharmProjects\video_code_test'
        


###############################  Iterate through all subdirectories in the root directory ###############################      
for dirpath, dirnames, filenames in os.walk(root_dir):
    if 'raw_video' in dirnames:
        # Set the path to the 'raw_video' folder
        raw_video_dir = os.path.join(dirpath, 'raw_video')
        for filename in os.listdir(raw_video_dir):
            # Check if the current file has an '.avi' extension
            if filename.endswith('.avi'):
                video_file_path = os.path.join(raw_video_dir, filename)
                try:
                    # Analyze the video to determine if it is flipped
                    is_flipped = process_video(video_file_path)

                    # Cast numpy boolean to native Python boolean
                    is_flipped = bool(is_flipped)
                    json_data = {"is_flipped": is_flipped}
                    
                    # If the video is flipped
                    if is_flipped:
                        print(f'{filename} is flipped')
                        # Flip the video and save it to a new file
                        flipped_video_file_path = flip_video(video_file_path)

                        # Create an 'original_video' folder and move the original video there
                        original_video_dir = os.path.join(raw_video_dir, "original_video")
                        os.makedirs(original_video_dir, exist_ok=True)
                        shutil.move(video_file_path, os.path.join(original_video_dir, filename))

                        # Rename the flipped video to the original file name
                        shutil.move(flipped_video_file_path, video_file_path)
                    else:
                        print(f'{filename} is not flipped')

                    # Create a JSON file 
                    json_file_path = os.path.join(raw_video_dir, os.path.splitext(filename)[0] + '.json')
                    create_json_file(json_file_path, json_data)

                except Exception as e:
                    if isinstance(e, (FileNotFoundError, OSError, IOError)):
                        print(f"{filename} does not contain any frames for analysis. Please check the video. Error: {e}")
                    else:
                        print(f"An error occurred while processing {filename}. Error: {e}")
                    
print('Analysis completed')



