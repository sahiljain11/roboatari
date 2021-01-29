import json
import os

TRAJ_NAME = "spaceinvaders_5VXL2UBKOT_1"

with open(os.path.join(os.getcwd(), TRAJ_NAME + ".json")) as f:
    data = json.load(f)

data = json.loads(data)
time_array = data["time_stamp:"]

f = open(os.path.join(os.getcwd(), 'images/make_video.sh'), 'w')

#for i in range(1, len(time_array)):
for i in range(1, len(time_array)):
    duration = (time_array[i] - time_array[i-1]) / 1000 # convert from milliseconds to seconds
    #image_name = f"{TRAJ_NAME}_{i}"
    #command = f'ffmpeg -loop 1 -i {image_name}.png -c:v libx264 -t {duration} -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" {image_name}.mp4\n'
    #f.write(command)

    # CONSTANT FRAME RATE USE THIS ONE
    #ffmpeg -r 24 -start_number 1 -i spaceinvaders_5VXL2UBKOT_1_%01d.png -c:v libx264 -vf "fps=25,format=yuv420p" -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" out.mp4

    #input_file = "blank.mp4" if i == 1 else f"{TRAJ_NAME}_final_{i-1}.mp4"
    ##command = f'ffmpeg -i "concat:{input_file}|{image_name}.mp4" -c copy {TRAJ_NAME}_final_{i}.mp4\n'
    ##command = f'ffmpeg -f concat -i <(printf "file \'%s\'\\n" {input_file} {image_name}.mp4) -c copy {TRAJ_NAME}_final_{i}.mp4\n'
    #if i != 1:
    #    command = f'ffmpeg -f concat -i \'{input_file}\' \'{image_name}.mp4\' -c copy {TRAJ_NAME}_final_{i}.mp4\n'
    #else:
    #    command = f'cp {image_name}.mp4 ./{TRAJ_NAME}_final_{i}.mp4'
    #f.write(command)

    #if i != 1:
    #    f.write(f"rm {input_file}\n")
    #    f.write(f"rm {image_name}.mp4\n")

f.close()
