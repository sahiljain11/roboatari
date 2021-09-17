import os
import argparse

from generate_gaze import CreateGaze

parser = argparse.ArgumentParser(description='Turn atari frames to have heat map gaze information')
parser.add_argument('--key', help="Enter the MTurk key user provided. Ex: mspacman_JE5W3X5P3T")
parser.add_argument('--dim1', help="Enter the first dimension of the output", type=int, default=213)
parser.add_argument('--dim2', help="Enter the first dimension of the output", type=int, default=160)

args = parser.parse_args()

num = 1
dir_list = os.listdir(os.getcwd())

dir_name = f"{args.key}_{num}"
ROM = args.key.split('_')[0]

create_gaze = CreateGaze(ROM, args.dim1, args.dim2)

while dir_name in dir_list:
    print(f"Generating gaze data for {dir_name}...")

    GAZE_DIR_NAME = f"{args.key}_{num}_gaze"

    full_dir_path  = os.path.join(os.getcwd(), dir_name)
    full_gaze_path = os.path.join(os.getcwd(), GAZE_DIR_NAME)
    frames = os.listdir(full_dir_path)

    os.mkdir(full_gaze_path)

    n = len(frames)

    for i in range(0, n):

        FRAME_FILE = frames[i]
        frame_paths = []

        for j in range(i - 3, i + 1):
            if j < 0:
                input_path  = os.path.join(full_dir_path, frames[0])
                frame_paths.append(input_path)
            else:
                input_path  = os.path.join(full_dir_path, frames[j])
                frame_paths.append(input_path)

        # pass complete path to gaze model to create a new image
        output_path = os.path.join(full_gaze_path, FRAME_FILE)
        create_gaze.create_gaze_frame(frame_paths, output_path, ROM)

    num += 1
    dir_name = f"{args.key}_{num}"
    while dir_name not in dir_list:
        num += 1
        dir_name = f"{args.key}_{num}"
        if num > 100:
            break

if num == 1:
    raise Exception("No trajectories processed")