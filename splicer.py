#!/usr/bin/env python
# encoding: utf=8

import numpy
import time
import os, sys, os.path
import re

import echonest.audio as audio
from echonest.sorting import duration
from echonest.selection import have_pitch_max, overlap_ends_of, overlap_starts_of, fall_on_the

def keysig(audiofile):
    return audiofile.analysis.loudness

def main(username):
  auds=[]
  p = re.compile("mix")
  files = os.listdir("f")
  for file in files:
    m = p.findall(file)
    if m:
      print "processing f/"+file
      try:
        auds.append(audio.LocalAudioFile("f/"+file))
      except:
        print "failed to include "+file
  
  auds.sort(key=keysig)
  
  mixed = []
  end = None
  previous = None
  for aud in auds:
    bars = aud.analysis.bars
    try:
      if end != None and previous != None:
        mix = audio.mix(audio.getpieces(previous, [end]), audio.getpieces(aud, [bars[0]]), 0.5)
        mixed.append(mix)
      else:
        mixed.append(audio.getpieces(aud, [bars[0]]))
    except:
      print "failed to create mix bar"

    try:
      mixed.append(audio.getpieces(aud, bars[1:-5]))
      end = bars[-5]
      previous = aud
    except:
      print "unable to append bars"

  out = audio.assemble(mixed, numChannels=2)
  out.encode(username+".mp3")

if __name__=='__main__':
  main(sys.argv[1])
