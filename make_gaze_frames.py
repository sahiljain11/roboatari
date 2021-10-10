import os
import argparse
import json
import librosa
from generate_gaze import CreateGaze
from make_annotation_frames import write_annotation
from progress.bar import Bar

parser = argparse.ArgumentParser(description='Turn atari frames to have heat map gaze information')
parser.add_argument('--key',   help="Enter the MTurk key user provided. Ex: mspacman_JE5W3X5P3T")
parser.add_argument('--dim1',  help="Enter the first dimension of the output", type=int, default=213)
parser.add_argument('--dim2',  help="Enter the first dimension of the output", type=int, default=160)
parser.add_argument('--words', help="Enter T/F for json annotations to be written to the frame", type=bool, default=True)

args = parser.parse_args()

num = 1
dir_list = os.listdir(os.getcwd())

dir_name = f"{args.key}_{num}"
ROM = args.key.split('_')[0]

create_gaze = CreateGaze(ROM, args.dim1, args.dim2)

while dir_name in dir_list:
    print(f"Generating gaze data for {dir_name}...")

    GAZE_DIR_NAME = f"{args.key}_{num}_gaze"
    ANNOTATIONS   = f"{args.key}_{num}_annotations.json"
    WAV_FILE      = f"{args.key}_{num}.wav"

    full_dir_path  = os.path.join(os.getcwd(), dir_name)
    full_gaze_path = os.path.join(os.getcwd(), GAZE_DIR_NAME)
    full_ann_path  = os.path.join(os.getcwd(), ANNOTATIONS)
    frames = sorted(os.listdir(full_dir_path))

    try:
        os.mkdir(full_gaze_path)
    except:
        pass

    n = len(frames)
    frames = [None] * n
    for i in range(1, n+1):
        frames[i-1] = f"{args.key}_{num}_{i}.png"

    y, sr = librosa.load(WAV_FILE, sr=48000)
    SECONDS = librosa.get_duration(y=y, sr=sr)
    annotations = json.load(open(full_ann_path, "r"))

    for key in annotations.keys():
        annotations[key][0] = int((annotations[key][0] / SECONDS) * n)
        annotations[key][1] = int((annotations[key][1] / SECONDS) * n)
        #print("annotations: " + str(annotations[key]))

    bar = Bar(f'Processing {dir_name}', max=n)
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

        if args.words:
            for key in annotations.keys():
                start = annotations[key][0]
                end   = annotations[key][1]
                word  = annotations[key][2]
                conf  = annotations[key][3]

                if start <= i and i < end:
                    input_path  = os.path.join(full_dir_path, FRAME_FILE)
                    if conf > 0.8:
                        write_annotation(output_path, word)
        bar.next()
    bar.finish()

    num += 1
    dir_name = f"{args.key}_{num}"
    while dir_name not in dir_list:
        num += 1
        dir_name = f"{args.key}_{num}"
        if num > 100:
            break

if num == 1:
    raise Exception("No trajectories processed")