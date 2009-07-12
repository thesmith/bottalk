#!/usr/bin/env python
# encoding: utf=8

import numpy
import time
import os, sys, os.path

import echonest.audio as audio
from echonest.sorting import duration
from echonest.selection import have_pitch_max, overlap_ends_of, overlap_starts_of, fall_on_the

def keysig(audiofile):
    return int(audiofile.analysis.key['value'])

auds=[]
files = os.listdir("mp3")
for file in files:
  print "processing mp3/"+file
  try:
    auds.append(audio.LocalAudioFile("mp3/"+file))
  except:
    print "failed to include "+file

auds.sort(key=keysig)
numfiles = len(auds)
for i in range(numfiles-1):
  try:
    audioOne = auds[i]
    #audioOne = audio.LocalAudioFile("mp3/"+files[i])
    master = audio.AudioQuantum(start=15.0, duration=45.0, source=audioOne)
    print "Building master mp3 "+str(i)
    master.encode("f/"+str(i)+".mp3")
  
    audioTwo = auds[i+1]
    #audioTwo = audio.LocalAudioFile("mp3/"+files[i+1])
  
    sample_rate = audioOne.sampleRate
    num_channels = audioOne.numChannels
    out_shape = (len(audioOne)+100000,num_channels)
  
    tonic = audioOne.analysis.key['value']
    chunks = audioTwo.analysis.__getattribute__("beats")
    segs = audioTwo.analysis.segments.that(have_pitch_max(tonic)).that(overlap_starts_of(chunks))
    outchunks = chunks.that(overlap_ends_of(segs))
  
    out = outchunks.render()
    print "Building beat mp3 "+str(i)
    out.encode("f/"+str(i)+".beat.mp3")
  
    os.system("python drums.py f/"+str(i)+".mp3 f/"+str(i)+".beat.mp3 f/"+str(i)+".mix.mp3 64 4 0.2")
  except:
    print "Failed to build "+str(i)+": "+sys.exc_info()[0]



