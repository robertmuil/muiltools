# create a synthetic 'sine wave' wave file with
# set frequency and length
# tested with Python 2.5.4 and Python 3.1.1 by vegaseat

import math
import wave
import struct
import matplotlib.pyplot as plt
import numpy as np
import sys


"""
create a synthetic 'sine wave' wave file with frequency freq
file fname has a length of about data_size * 2
"""

srate = 44100.0  # samplerate as a float
amp = 8000.0     # multiplier for amplitude
freq = 100.0     # cycles per second
fname = "WaveTest2.wav" # write the synthetic wave file to ...
fname = None

PlotWave=False
SingleCycle=True

if len(sys.argv) > 1:
	srate=float(sys.argv[1])

if SingleCycle:
	data_size=int(math.ceil(srate/freq))
	print 'single cycle = ' + str(srate/freq) + ' ('+str(data_size)+') samples'
else:
	#data enough for single second
	data_size = math.ceil(srate) # data size in samples (file size will be about 2 times this)
	print 'single second = ' + str(data_size) +' samples'

# make a sine list ...
sine_list = []
s = range(data_size);
for x in s:
	sine_list.append(math.sin(2*math.pi*freq*(x/srate)))

print 'end error='+str(sine_list[-1])
t=np.array(s)/srate
if PlotWave:
	plt.figure()
	plt.plot(t,sine_list)
	plt.show()

# get ready for the wave file to be saved ...
if fname != None:
	wav_file = wave.open(fname, "w")
	# give required parameters
	nchannels = 1
	sampwidth = 2
	framerate = int(frate)
	nframes = data_size
	comptype = "NONE"
	compname = "not compressed"
	# set all the parameters at once
	wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
	# now write out the file ...
	print( "may take a moment ..." )
	for s in sine_list:
		# write the audio frames to file
		wav_file.writeframes(struct.pack('h', int(s*amp/2)))
	wav_file.close()
	print( "%s written" % fname )
