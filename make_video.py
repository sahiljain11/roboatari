import json
import os
import librosa
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Turn atari data into a single mp4')
parser.add_argument('--key', help="Enter the MTurk key user provided. Ex: mspacman_JE5W3X5P3T")
parser.add_argument('--gaze', default=False, type=bool, help="Specify True/False on whether or not to use a gaze directory. Default is false")

args = parser.parse_args()

num = 1
dir_list = os.listdir(os.getcwd())

if args.gaze:
    dir_name = f"{args.key}_{num}_gaze"
else:
    dir_name = f"{args.key}_{num}"

while dir_name in dir_list:
    print(f"Generating {dir_name}...")

    TRAJ_NAME = f"{args.key}_{num}"

    splitted = TRAJ_NAME.split("_")

    # get the strings for the file names
    WAV_FILE   = f"{TRAJ_NAME}.wav"
    JSON_FILE  = f"{TRAJ_NAME}.json"
    ATARI_FILE = f"{splitted[0]}_{splitted[1]}_atari_{splitted[2]}.wav"

    # calculate the number of frames
    with open(os.path.join(os.getcwd(), JSON_FILE)) as f:
        data = json.load(f)

    data = json.loads(data)
    NUM_FRAMES = len(data["time_stamp"])

    # get the number of seconds the wav file lasts so you can calculate FPS
    y, sr = librosa.load(WAV_FILE)
    SECONDS = librosa.get_duration(y=y, sr=sr)
    FPS = int(round(NUM_FRAMES / SECONDS))

    print(NUM_FRAMES)
    print(SECONDS)
    print(FPS)

    # create a shell script
    f = open(os.path.join(os.getcwd(), f'make_video.sh'), 'w')

    # turns all of the images into one video file
    #command = f'ffmpeg -r 24 -start_number 1 -i {TRAJ_NAME}/{TRAJ_NAME}_%01d.png -c:v libx264 -vf "fps={FPS},format=yuv420p" -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" out.mp4\n'
    if args.gaze:
        command = f'ffmpeg -r {FPS} -start_number 1 -i {TRAJ_NAME}_gaze/{TRAJ_NAME}_%01d.png -c:v libx264 -vf "fps={FPS},format=yuv420p" -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" out.mp4\n'
    else:
        command = f'ffmpeg -r {FPS} -start_number 1 -i {TRAJ_NAME}/{TRAJ_NAME}_%01d.png -c:v libx264 -vf "fps={FPS},format=yuv420p" -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" out.mp4\n'
    f.write(command)

    # combines the user's audio and the atari audio
    command = f'ffmpeg -i {WAV_FILE} -i {ATARI_FILE} -filter_complex "[0][1]amerge=inputs=2,pan=stereo|FL<c0+c1|FR<c2+c3[a]" -map "[a]" output.wav\n'
    f.write(command)

    # adds the audio to the video
    command = f"ffmpeg -i out.mp4 -i output.wav -c:v copy -c:a aac {TRAJ_NAME}_final.mp4\n"
    f.write(command)

    # turn mp4 into mov
    if args.gaze:
        command = f"ffmpeg -i {TRAJ_NAME}_final.mp4 -f mov {TRAJ_NAME}_gaze_final.mov\n"
    else:
        command = f"ffmpeg -i {TRAJ_NAME}_final.mp4 -f mov {TRAJ_NAME}_final.mov\n"
    f.write(command)

    command = f"rm out.mp4\n"
    f.write(command)
    command = f"rm output.wav\n"
    f.write(command)
    command = f"rm {TRAJ_NAME}_final.mp4\n"
    f.write(command)

    f.close()

    # run the shell script
    subprocess.call(['sh', './make_video.sh'])
    os.system("rm ./make_video.sh")

    num += 1
    if args.gaze:
        dir_name = f"{args.key}_{num}_gaze"
    else:
        dir_name = f"{args.key}_{num}"

    while dir_name not in dir_list:
        num += 1
        if args.gaze:
            dir_name = f"{args.key}_{num}_gaze"
        else:
            dir_name = f"{args.key}_{num}"
        if num > 100:
            break

if num == 1:
    raise Exception("No trajectories processed")