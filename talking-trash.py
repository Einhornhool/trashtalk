#!/usr/bin/env python

import msa301
import time
import simpleaudio as sa
import os
import random

# Create a list of all available audio files in the directory 'audio'
audiofiles = [os.path.join(r,fi) for r,d,f in os.walk('/home/pi/trash_talk/audio/random') for fi in f]

# Create a list of WaveObjects from the available audiofiles
audio_obj = [sa.WaveObject.from_wave_file(f) for f in audiofiles]
audio_len = len(audio_obj)

biowaste_obj = sa.WaveObject.from_wave_file('audio/TTF_Biowaste.wav')

accel = msa301.MSA301()
accel.reset()
accel.set_power_mode('normal')
accel.enable_interrupt([
    'x_active_interrupt',
    'z_active_interrupt'])

open_val = 0.1
close_val = 0.9
last_z = close_val

opened = False

def lid_closed():
    print("Lid closed, Curr: {0}".format(curr_z))
    # Get random audio object to play
    rand_obj = audio_obj[random.randint(0, audio_len-1)]
    play_obj = rand_obj.play()
    play_obj.wait_done()

def lid_opened():
    print("Lid opened, Curr: {0}".format(curr_z))
    play_obj = biowaste_obj.play()
    play_obj.wait_done()


try:
    while (True):
        # Wait until movement is detected and get current measurements        
        accel.wait_for_interrupt('active_interrupt')
        curr_x, curr_y, curr_z = accel.get_measurements()
        #print("X: {0}, Y: {1}, Z: {2}".format(curr_z, curr_y, curr_z))
       
        if (last_z < curr_z) and (curr_z >= close_val) and opened:
            lid_closed()
            opened = False
        if (last_z > curr_z) and (curr_z < open_val) and not opened:
            lid_opened()
            opened = True

        last_z = curr_z

except KeyboardInterrupt:
    pass
