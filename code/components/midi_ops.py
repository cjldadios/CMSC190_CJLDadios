#!/usr/bin/env python

import os

from midiutil import MIDIFile
from midi2audio import FluidSynth


from global_ops import *

# def classCodeToInstument(number, legend):
#     hitClass = legend[str(int(number))]
#     instruments = hitClass.split("_")
#     return instruments


def convert_to_midi(input_dict_list, bpm, filename):
    print("\nConverting predictions to midi...")
    
    midi_mapping = {
        "bass": 36,                     # C2
        "stick": 37,                    # C#2
        "snare": 38,                    # D2
        "floor": 41,                    # F2
        "hihat": 42,                    # F#2
        "hihatp": 44, # pedal           # G#2
        "hihat-open": 46,               # A#2  
        "tom": 47,                      # B2     
        "crash": 49,                    # D#3
        "ride": 51,                     # E#3
        "bell": 53                      # F3
    }

    # volume_mapping = {
    #     "bass": 120,
    #     "stick": 115,
    #     "snare": 105,
    #     "floor": 110,
    #     "tom": 110,
    #     "hihat": 100,
    #     "hihat-open": 100,
    #     "hihatp": 105, # pedal
    #     "crash": 100,
    #     "ride": 100,
    #     "bell": 100,
    #     "rest": 0,
    # }

    volume_mapping = {
        "bass": 127,
        "stick": 127,
        "snare": 127,
        "floor": 127,
        "tom": 127,
        "hihat": 127,
        "hihat-open": 127,
        "hihatp": 127, # pedal
        "crash": 127,
        "ride": 127,
        "bell": 127,
        "rest": 0,
    }


    # degrees  = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
    track    = 0
    channel  = 10
    time     = 0   # In beats
    # duration = 1   # In beats
    duration = 1/4   # In beats
    tempo    = bpm  # In BPM
    volume   = 115 # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                         # automatically created)
    if bpm==0:
        tempo = 1 # prevent division by zero
    
    MyMIDI.addTempo(track,time, tempo)

    # for pitch in degrees:
    #     MyMIDI.addNote(track, channel, pitch, time, duration, volume)
    #     time = time + 1


    """
        Try to add multiple notes at a time: Loop addNote
        while instruments identified by the name are not exhausted
        
        To use foot hihat, if there are already four instruments, use "hihatp"
    """

    # input_dict_list is a list of dictionaries
    # The dictionaries have keys "1", "e", "&", "a"
    # where the values are class names, eg. "bass tom hihat ride"

    rhythm_start_time_dict = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        # "5": 0,
        "e": 1/16,
        "&": 1/8,
        "a": 3/16
    }

    print("\nInside midi_ops...")
    for quarter_dict in input_dict_list:
        for key, val in quarter_dict.items():
            print("{}: {}".format(key, val))

    # halt()

    for quarter_dict in input_dict_list:
        prev_key = "0 1" # initialization of previous rhythm

        for key, val in quarter_dict.items():

            # Advance the time depending on the rhythm, identified by the key
            # prev_rhy = rhythm_start_time_dict[prev_key]
            # curr_rhy = rhythm_start_time_dict[key]
            # time = time + curr_rhy - prev_rhy

            split_key = key.split()
            # split_prev_key = prev_key.split()

            # curr_time = int(split_key[0]) + rhythm_start_time_dict[split_key[1]]
            # prev_time = int(split_prev_key[0]) \
                # + rhythm_start_time_dict[split_prev_key[1]]
            # time += curr_time - prev_time

            quarter_id = split_key[0] # e.g. "0"
            sixteenth_id = split_key[1] # e.g. "a"

            time = (int(quarter_id) * 0.25 \
                + rhythm_start_time_dict[sixteenth_id]) * 4

            prev_key = key # update prev_key

            has_hihat = False # add the hihat last
            has_hihat_open = False
            has_bass = False
            four_hits_at_a_time = False
            hit_count = 0

            for instrument in val.split():
                volume = volume_mapping[instrument]

                if instrument == "hihat":
                    has_hihat = True
                elif instrument == "hihat-open":
                    has_hihat_open = True
                elif instrument == "rest":
                    hit_count += 1
                else:
                    if instrument == "bass":
                        has_bass = True

                    pitch = midi_mapping[instrument]
                    MyMIDI.addNote(track, channel, pitch, 
                                    time, duration, volume)
                    hit_count += 1
            # End for every instrument hit per rhythm

            # Add hihat last if there's hihat
            if has_hihat_open or has_hihat:
                if hit_count == 3: # If there's a limb available
                    pitch = midi_mapping["hihatp"] # No other hihat option
                    MyMIDI.addNote(track, channel, pitch, 
                                    time, duration, volume)
                elif hit_count == 2: # If two limbs were occupied
                    if has_bass: # but one of that limb is a bass
                        # A hand is available, so option if open is available
                        if has_hihat_open:
                            pitch = midi_mapping["hihat-open"]
                            MyMIDI.addNote(track, channel, pitch, 
                                    time, duration, volume)
                        else: # Closed hihat
                            pitch = midi_mapping["hihat"]
                            MyMIDI.addNote(track, channel, pitch, 
                                    time, duration, volume)
                    else: # If two instruments were hit, and not one of them
                        # is a bass. It means that both hands were already
                        # used. Therefore, we can only use the left foot
                        # to play the hihat.
                        pitch = midi_mapping["hihatp"] # No other hihat option
                        MyMIDI.addNote(track, channel, pitch, 
                                                    time, duration, volume)
                else: # At most one limb will be occupied.
                    # Therefore, at least one limb (required) will be able
                    # to play the hihat.
                    if has_hihat_open:
                        pitch = midi_mapping["hihat-open"]
                        MyMIDI.addNote(track, channel, pitch, 
                                time, duration, volume)
                    else: # Closed hihat
                        pitch = midi_mapping["hihat"]
                        MyMIDI.addNote(track, channel, pitch, 
                                time, duration, volume)

            # End adding hihat
        # End for each rhythm
    # End for all the hits on each rhythm

    with open(filename + ".mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)


def convert_midi_to_audio(midi_input_file):
    midi_input_filename = os.path.basename(midi_input_file) # Eg. "solo.wav"
    midi_input_file_wo_ext = os.path.splitext(midi_input_filename)[0]
    output_audio_filename = midi_input_filename + "_audio_from_midi" + ".wav"
    fs = FluidSynth("./Files/Yamaha_RX7_Drums.sf2")
    fs.midi_to_audio(midi_input_file, output_audio_filename)