import json
import os

TRAJ_NAME = "spaceinvaders_5VXL2UBKOT_1"
FRAMES = 5169
SECONDS = 87

f = open(os.path.join(os.getcwd(), 'images/make_video.sh'), 'w')

# CONSTANT FRAME RATE USE THIS ONE
# ffmpeg -r 24 -start_number 1 -i spaceinvaders_5VXL2UBKOT_1_%01d.png -c:v libx264 -vf "fps=25,format=yuv420p" -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" out.mp4


# merges sound but one sound per headphone
# ffmpeg -i spaceinvaders_K5RL6KT4MK_1.wav -i spaceinvaders_K5RL6KT4MK_atari_1.wav -filter_complex "[0][1]amerge=inputs=2,pan=stereo|FL<c0+c1|FR<c2+c3[a]" -map "[a]" output.wav

# one that actually mixes sound together
# ffmpeg -i spaceinvaders_K5RL6KT4MK_1.wav -i spaceinvaders_K5RL6KT4MK_atari_1.wav -filter_complex amix=inputs=2:duration=longest output_mix.wav


# merges video and audio files
# ffmpeg -i out.mp4 -i output.wav -c:v copy -c:a aac final.mp4


#with open(os.path.join(os.getcwd(), TRAJ_NAME + ".json")) as f:
#    data = json.load(f)
#
#data = json.loads(data)
#time_array = data["time_stamp:"]
#
#
##for i in range(1, len(time_array)):
#for i in range(1, len(time_array)):
#    duration = (time_array[i] - time_array[i-1]) / 1000 # convert from milliseconds to seconds
#    #image_name = f"{TRAJ_NAME}_{i}"
#    #command = f'ffmpeg -loop 1 -i {image_name}.png -c:v libx264 -t {duration} -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" {image_name}.mp4\n'
#    #f.write(command)
#
#
#    #input_file = "blank.mp4" if i == 1 else f"{TRAJ_NAME}_final_{i-1}.mp4"
#    ##command = f'ffmpeg -i "concat:{input_file}|{image_name}.mp4" -c copy {TRAJ_NAME}_final_{i}.mp4\n'
#    ##command = f'ffmpeg -f concat -i <(printf "file \'%s\'\\n" {input_file} {image_name}.mp4) -c copy {TRAJ_NAME}_final_{i}.mp4\n'
#    #if i != 1:
#    #    command = f'ffmpeg -f concat -i \'{input_file}\' \'{image_name}.mp4\' -c copy {TRAJ_NAME}_final_{i}.mp4\n'
#    #else:
#    #    command = f'cp {image_name}.mp4 ./{TRAJ_NAME}_final_{i}.mp4'
#    #f.write(command)
#
#    #if i != 1:
#    #    f.write(f"rm {input_file}\n")
#    #    f.write(f"rm {image_name}.mp4\n")

f.close()
