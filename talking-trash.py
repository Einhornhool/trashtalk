#!/usr/bin/env python

import msa301
import time
import simpleaudio as sa
import os
import random

# Create a list of all available audio files in the directory 'audio'
audiofiles = []
for r,d,f in os.walk('/home/pi/trash_talk/audio'):
    for fi in f:
        audiofiles.append(os.path.join(r, fi))

# Create a list of WaveObjects from the available audiofiles
audio_obj = [sa.WaveObject.from_wave_file(f) for f in audiofiles]
audio_len = len(audio_obj)

accel = msa301.MSA301()
accel.reset()
accel.set_power_mode('normal')
accel.enable_interrupt([
    'y_active_interrupt',
    'z_active_interrupt'])

# Get base value (should be 0, but you never know)
base_x, base_y, base_z = accel.get_measurements()

# When closing the lid, the last value will rarely be exactly 0. For this particular sensor it's always below 0.1, though.
# May not apply to all sensors
tolerance = 0.1

last_z = base_z

try:
    while (True):
        # Wait until movement is detected and get current measurements        
        accel.wait_for_interrupt('active_interrupt')
        curr_x, curr_y, curr_z = accel.get_measurements()
       
        if (last_z > curr_z) and (curr_z <= (base_z + tolerance)):
            print("Lid closed, Curr: {0}".format(curr_z))
            # Get random audio object to play
            rand_obj = audio_obj[random.randint(0, audio_len-1)]
            play_obj = rand_obj.play()
            play_obj.wait_done()

        last_z = curr_z

except KeyboardInterrupt:
    pass
