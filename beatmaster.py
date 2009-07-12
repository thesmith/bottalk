#!/usr/bin/env python
# encoding: utf=8

import numpy
import sys
import time

import echonest.audio as audio
from echonest.sorting import duration
from echonest.selection import have_pitch_max, overlap_ends_of, overlap_starts_of, fall_on_the

def main(fileOne, fileTwo, outBeat, outMaster):
  audioOne = audio.LocalAudioFile(fileOne)
  master = audio.AudioQuantum(start=0.0, duration=20.0, source=audioOne)
  master.encode(outMaster)

  audioTwo = audio.LocalAudioFile(fileTwo)

  sample_rate = audioOne.sampleRate
  num_channels = audioOne.numChannels
  out_shape = (len(audioOne)+100000,num_channels)

  tonic = audioOne.analysis.key['value']
  chunks = audioTwo.analysis.__getattribute__("beats")
  segs = audioTwo.analysis.segments.that(have_pitch_max(tonic)).that(overlap_starts_of(chunks))
  outchunks = chunks.that(overlap_ends_of(segs))

  out = outchunks.render()
  out.encode(outBeat)

if __name__ == '__main__':
  main(sys.argv[-4], sys.argv[-3], sys.argv[-2], sys.argv[-1])
