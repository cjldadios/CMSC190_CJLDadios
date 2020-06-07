
""" input_ops.py """

import os
import sys
import math
import shutil

import numpy
import librosa
from pydub import AudioSegment # imports file audio

from global_vars import *
from global_ops import *
from folder_ops import *
from feature_ops import *


def process_input(input_dir, tempo=None):

    print("\nProccessing input...\n")

    # load as audio in memory
    y, sr = librosa.load(input_dir)

    # print("y.shape: {}".format(y.shape))
    # print("removed zeros: {}".format(numpy.trim_zeros(y).shape))

    # # Extending with a silence, no matter what

    # https://librosa.github.io/librosa/generated/librosa.beat.beat_track.html
    # Estimate tempo (bpm) and beat location as array of frame indices
    # tempo, beat_frame_arr = librosa.beat.beat_track(y=y, sr=sr, units="samples")
    # Convert frames array to times array
    # # Create a silent audio with a fixed lenth
    # y_silent = numpy.zeros(20)

    # # Create a silent audio with a varying length
    # # Sample the first two beats to get the difference between beats.
    # if len(beat_frame_arr) >= 2:
    #     beat_diff = beat_frame_arr[1] - beat_frame_arr[0]

    #     # Create a silent audio using the length of beat_diff
    #     y_silent = numpy.zeros(beat_diff)

    #     # print("\ny_silent: {}".format(y_silent))
    #     # print("len(y_silent): {}".format(len(y_silent)))

    # # Extend the beginning of the input audio with silence
    # y = numpy.append([y_silent], y)
    # # print(y)

    # librosa.output.write_wav("extended.wav", y, sr)
    # librosa.output.write_wav("silence.wav", y_silent, sr)
    

    # sound1 = AudioSegment.from_wav("/path/to/file1.wav")
    # sound2 = AudioSegment.from_wav("/path/to/file2.wav")

    # combined_sounds = sound1 + sound2
    # combined_sounds.export("/output/path.wav", format="wav")

    # Recompute beat_track with the extended with an initial silence.
    beat_tempo, beat_frame_arr = librosa.beat.beat_track(y=y, sr=sr)
    # Convert frames array to times array


    # Sometimes the tempo is doubled because of loud 1/8 beats
    if tempo is None:
        tempo = beat_tempo
    else:
        print("tempo: {}".format(tempo))
        print("beat_tempo: {}".format(beat_tempo))
        print("tempo * 1.8: {}".format(tempo * 1.8))
        print("beat_tempo > tempo * 1.8: {}".format(beat_tempo > tempo * 1.8))
        print("tempo * 2.2: {}".format(tempo * 2.2))
        print("beat_tempo < tempo * 2.2: {}".format(beat_tempo < tempo * 2.2))
        # Compare the automatic tempo vs the input tempo
        if beat_tempo > tempo * 1.8 and beat_tempo < tempo * 2.2:
            # If the automatic tempo is more or less twice the original tempo,
            # remove even beat_frame_array elements
            print("before beat_frame_arr: {}".format(beat_frame_arr))
            # Remove even, because the first identified onset should be odd.
            print("py main.py my_drum_demo2.wav tempo 70 " 
                + "whitelist bass snare hihat blacklist hihat")
            # beat_frame_arr = numpy.arange([frame 
                # for i, frame in enumerate(beat_frame_arr) if i % 2 == 1])
            new_beat_frame_arr = []
            for i, frame in enumerate(beat_frame_arr):
                if i % 2 == 0:
                    new_beat_frame_arr.append(frame)
            # print("new_beat_frame_arr: {}".format(new_beat_frame_arr))
            beat_frame_arr = numpy.array(new_beat_frame_arr)
            print("after beat_frame_arr: {}".format(beat_frame_arr))
        elif beat_tempo > tempo * 0.8 and beat_tempo < tempo * 1.2:
            # beat_tempo is accurate enough
            #tempo = beat_tempo
            pass
        else:
            if beat_tempo > tempo * 1.5: # predicted tempo is too fast
                pass # maintain given tempo

            else:
                # Still not accept predicted tempo
                #tempo = beat_tempo
                # tempo is the indicated tempo
                pass

    # Just adding the audio beginning and the end
    # to assume that beat occured at both ends
    # beat_frame_arr \
    #           = numpy.append([0], beat_frame_arr)
    # beat_frame_arr \
    #           = numpy.append(beat_frame_arr, len(y)-1)
    # This is wrong implementation.

    print("before beat_frame_arr:")
    print(beat_frame_arr)

    if len(beat_frame_arr) == 0:
        print("Invalid: No beat detected")
        system.exit()

    beat_frame_arr_front_extension = numpy.zeros(1)

    # Adding more quarter note slice at the beginning and the end
    # Getting the average beat length
    if len(beat_frame_arr) >= 2:
        starts = beat_frame_arr[:-1]
        ends = beat_frame_arr[1:]
        diffs = ends - starts
        beat_interval = numpy.mean(diffs)
        beat_interval = int(beat_interval)
     
        max_front_quarter_note_extension_count = 4 # 4 To follow 4/4 time.

        is_front_extended = False

        """ Option """
        # to_extend_quarter_slice_forward = False
        to_extend_quarter_slice_forward = True

        if to_extend_quarter_slice_forward:
            # Stepping backward from the beginning...   
            step_back = beat_frame_arr[0] - beat_interval
            if step_back < 0:
                # The extension forward will be too short.

                # The step back exceeds the 0.0 audio time.
                # What about 80%?
                step_back = beat_frame_arr[0] - beat_interval * 0.8
                if step_back < 0:
                    # It doesn't fit.
                    # pass # Let it be.
                    print("Beginning, not fit...")
                    # What about 50%
                    step_back = beat_frame_arr[0] - beat_interval * 0.5
                    if step_back < 0:
                        # pass
                        # The remaining time before 0.0 from first index is
                        # Less than half a beat length
                        # So, Just extend the first beat to 0.0 by replacing
                        # the first element with 0.0.
                        beat_frame_arr = numpy.append([0], beat_frame_arr[1:])

                else:
                    # Set a beat at time 0.0
                    print("Beginning, not fit added...")
                    beat_frame_arr = numpy.append([0], beat_frame_arr)
                    is_front_extended = True
            else:
                # An extension forward is long enough.
                is_front_extended = True

                # A new beat before the first detected can fit at the beginning.
                # print("Beginning, fit added... ", end="")

                # count = 0
                # while step_back >= 0:
                #     # beat_frame_arr = numpy.append([step_back], beat_frame_arr)

                #     if count == 0: # initialize
                #         beat_frame_arr_front_extension \
                #             = numpy.arange(step_back)
                #     else: # Append
                #         beat_frame_arr_front_extension = numpy.append(
                #             [step_back], beat_frame_arr_front_extension)

                #     # step_back = beat_frame_arr[0] - beat_interval
                #     step_back = beat_frame_arr_front_extension[0] \
                #         - beat_interval

                #     count += 1

                #     # if count == max_front_quarter_note_extension_count:
                #         # break

                # print("{} times...".format(count))

                # # Extend beat_frame_arr if valid, meaning extending with a
                # # multiple of 4 beat count.
                # if count <= 4:
                #     beat_frame_arr = numpy.append(
                #         beat_frame_arr_front_extension, beat_frame_arr)

                # if count < 4:
                #     if count != max_front_quarter_note_extension_count:
                #         # The step back exceeds the 0.0 audio time.
                #         # What about 80%?
                #         step_back = beat_frame_arr[0] - beat_interval * 0.8
                #         if step_back < 0:
                #             # It doesn't fit.
                #             # pass # Let it be.
                #             print("Beginning, not fit anymore...")
                #             # What if 50%?
                #             step_back = beat_frame_arr[0] - beat_interval * 0.5
                #             if step_back < 0:
                #                 # A little bit remaining before 0.0,
                #                 # not even half so just extend to the beginning.
                #                 print("bf: {}".format(beat_frame_arr))

                #                 beat_frame_arr \
                #                     = numpy.append([0], beat_frame_arr[1:])
                #                 print("\t ...but extened.")

                #                 print("aftr: {}".format(beat_frame_arr))

                #             else:
                #                 # It doesn't fit.
                #                 # pass # Let it be.
                #                 print("\t so not added...")

                                
                #         else:
                #             # Set a beat at time 0.0
                #             print("Beginning, not fit anymore, but added...")
                #             beat_frame_arr = numpy.append([0], beat_frame_arr)
                #             count += 1

                # Extend once/ just once
                # print("beat_frame_arr: {}".format(beat_frame_arr))
                beat_frame_arr = numpy.append([step_back], beat_frame_arr)
                # print("beat_frame_arr: {}".format(beat_frame_arr))
                
                step_back = beat_frame_arr[0] - beat_interval
                # Is the first element almost the beginning (0.0)?
                if step_back < 0: # Yes.
                    # By how much?
                    step_back = beat_frame_arr[0] - beat_interval * 0.5 # half?
                    if step_back < 0: # Almost end...
                        # Then replace tha first element with 0.0.
                        beat_frame_arr = numpy.append(
                            [0], beat_frame_arr[1:])

                # print("beat_frame_arr: {}".format(beat_frame_arr))

        # End if to_extend_quarter_slice_forward:
        
        # Stepping forward from the end...
        step_forward = beat_frame_arr[-1] + beat_interval
        print("step_forward: {}".format(step_forward))
        len_to_frame = librosa.samples_to_frames(len(y))
        print("len_to_frame: {}".format(len_to_frame))

        if step_forward >= len_to_frame:
            # The step back exceeds the 0.0 audio time.
            # What about 80%?
            step_forward = beat_frame_arr[-1] + beat_interval * 0.8
            if step_forward >= len_to_frame:
                # It doesn't fit.
                # pass # Let it be.
                print("End, not fit...")
            else:
                # Set a beat at the time where the audio ends.
                print("End, not fit added...")
                ending = round(len_to_frame)
                beat_frame_arr = numpy.append(beat_frame_arr, ending)
        else:
            # A new beat after the last detected can fit at the end.
            print("End, fit added...", end="")
            count = 0
            while step_forward <= len_to_frame:
                beat_frame_arr = numpy.append(beat_frame_arr, [step_forward])
                step_forward = beat_frame_arr[-1] + beat_interval
                count += 1
            print(" {} times...".format(count))

            # The step back exceeds the 0.0 audio time.
            # What about 80%?
            step_forward = beat_frame_arr[-1] + beat_interval * 0.8
            if step_forward >= len_to_frame:
                # It doesn't fit.
                # pass # Let it be.
                print("End, not fit anymore...")
            else:
                # Set a beat at the time where the audio ends.
                print("End, not fit any more, but added...")
                ending = round(len_to_frame)
                beat_frame_arr = numpy.append(beat_frame_arr, ending)

        # Wherever the last beat landed, still add the end of the audio
        # to capture the rest, until the recoring ends.
        ending = round(len_to_frame)
        beat_frame_arr = numpy.append(beat_frame_arr, ending)

    print("after beat_frame_arr:")
    print(beat_frame_arr)

    print("\nThe quarter note slice doesn't capture beginning audio 0.0.")
    
    
    # print("is_front_extended: {}".format(is_front_extended))
    # halt() 

    """"""

    quarter_beat_arr = librosa.frames_to_samples(beat_frame_arr)

    len_to_frame = librosa.samples_to_frames(len(y))
    last_sample = librosa.frames_to_samples(len_to_frame)

    print("quarter_beat_arr:")
    print(quarter_beat_arr)
    print("last_sample: {}".format(last_sample))
    
    # tempo, quarter_beat_arr \
        # = librosa.beat.beat_track(y=y, sr=sr, units="samples")
    quarter_starts = quarter_beat_arr[:-1] # The actual audio was already...
    quarter_stops = quarter_beat_arr[1:] # ...added using...
                        # ...ending = round(len_to_frame) somewhere previously
    
    # rms_list = []

    # delete_folder("./First beats")
    if os.path.isdir("./First beats"):
        for file in os.listdir("./First beats"):
            os.remove("./First beats/" + file)
    create_folder("./First beats")

    print("\nrms_list: ")

    for i, (start, stop) in enumerate(zip(quarter_starts, quarter_stops)):
        rms = librosa.feature.rms(y=y[start: stop])
        librosa.output.write_wav("./First beats/" + str(i) + ".wav", 
            y[start: stop], sr)

        # rms_list.append(rms)
        # print("".format(rms_list))
        print(i)
        print(rms)

        if i == 5:
            break

    # print("\nrms_list {}".format(rms_list))

    # print("parang mali yung bagong quarter note index.")
    

    """"""    
    print("\nCheck if beginning is extended. ")
    print("If yes, is it blank or not?")
    print("If it is blank, remove it.")
    print("If it is not blank, keep it and assume an ONSET on the first beat.")

    add_front_as_onset = False

    if is_front_extended:
        print("Front was extended")

        # # Identify if the first quarter note slice silent (the first 80%)
        # # Get 100% length.
        # quarter_len = quarter_beat_arr[1] - quarter_beat_arr[0]
        # first_part_len = int(quarter_len * 0.8)
        # extension \
        #     = y[quarter_beat_arr[0]: quarter_beat_arr[0] + first_part_len]
        # rms = librosa.feature.rms(y=extension)
        # ave_rms = numpy.mean(rms) # Energy

        # print("ave_rms: {}".format(ave_rms))

        # # If the front extension is 
        # if ave_rms < 0.1: # If the first part 
        #     # remove front
        #     beat_frame_arr = beat_frame_arr[1:]
        #     print("Extension removed")
        # else:
        #     add_front_as_onset = True
        #     print("Extension not removed")

        # Manually check for onsets on the extended front.
        # If none is detected, remove the front extension.

        quarter_len = quarter_beat_arr[1] - quarter_beat_arr[0]
        first_part_len = int(quarter_len * 0.85) # Just 85%, because the end
            # might capture the next beat onset.
        extension \
            = y[quarter_beat_arr[0]: quarter_beat_arr[0] + first_part_len]
        rms = librosa.feature.rms(y=extension)

        
        
        # librosa.output.write_wav("./extension_for_rms.wav", extension, sr)
        # print("See extension_for_rms.wav")


        has_onset = False

        # If any of the values in the array rms 
        # if (energy.any() >= 0.1 for energy in rms): # This doesn't work!
        for i, r in enumerate(rms[0]): # Use this instead
            # print("{}: {}".format(i, r)) 
            if r > 0.1:
                has_onset = True
        
        if has_onset == False:
            # Remove the inserted extension.
            beat_frame_arr = beat_frame_arr[1:]

        # Later, during the onset detection, if front was extended,
        # it will be manually detected for onsets, using rms, segmented into 4.
        # Maybe...

        print("has_onset: {}".format(has_onset))

    # beat_location_time_array = librosa.frames_to_time(beat_frame_arr, sr=sr)
    # print("tempo: " + str(tempo))
    # print("beat_frame_arr: ")
    # print(beat_frame_arr)
    # print("beats in time: ")
    # print(beat_location_time_array)

    # Note: 40-250 bpm, quantization

    # Returns one_e_and_a_dict_list, a list containing dictionaries
    # having keys "1, e, &, a" but some keys may be absent
    one_e_and_a_dict_list = slice_input(input_dir, beat_frame_arr,
                                    add_front_as_onset, is_front_extended)
    one_two_three_four_dict_list = []
        # This is a copy of one_e_and_a_dict_list,
            # but instead of 1 e & a 1 e & a 1 e & a 1 e & a,
            # it will be 1 e & a 2 e & a 3 e & a 4 e & a,
            # which will be ued for pattern simplification

    # in_aud_feat_arr = numpy.empty(len(audio_features)*feature_array_cutoff)
    in_aud_feat_arr = numpy.zeros(7+20+10*5) 
      # Current combined lenght of feature array

    quarter_beat_index = 1 # Goes from 1 to 4 only

    ###
    print("\nExtracting sliced input audio features")

    # Try to delete Sub Sliced Input Folder
    try:
      shutil.rmtree(sub_sliced_input_destination)
    except OSError as e:
      print("Error: %s - %s." % (e.filename, e.strerror))

    # Create Sub Sliced Input Folder
    create_folder(sub_sliced_input_destination)

    is_use_long_audio = True # Long is good and working.
    # is_use_long_audio = False

    # if not is_use_long_audio:

    #     sliced_input_files = os.listdir(sliced_input_destination)
    #     is_initialized_in_aud_feat_arr = False

      
    #     sub_slice_index = 0
      
    #     for indx, (audio_file, one_e_and_a_dict) \
    #         in enumerate(zip(sliced_input_files, one_e_and_a_dict_list)):
          
    #         print("audio_file: {}".format(audio_file))
    #         audio_dir = sliced_input_destination + "/" + audio_file
    #         audio, sr = librosa.load(audio_dir)

    #         one_two_three_four_dict = {}

    #         for rhythm, scope in one_e_and_a_dict.items():

    #             if rhythm == "1":
    #                 rhythm = str(quarter_beat_index)
    #                 quarter_beat_index += 1
    #                 if quarter_beat_index == 5:
    #                     quarter_beat_index = 1
    #             one_two_three_four_dict[rhythm] = scope

    #             print("rhythm: {}".format(rhythm))
    #             print("scope: {}".format(scope))
    #             aud_slice = audio[scope[0]: scope[1]]
    #             print("len(aud_slice): {}".format(len(aud_slice)))

    #             aud_feat = extract_audio_features(y=aud_slice, sr=sr)

    #             if not is_initialized_in_aud_feat_arr:
    #                 # Initializing array
    #                 in_aud_feat_arr = numpy.array(aud_feat)
    #                 is_initialized_in_aud_feat_arr = True
    #             else: # stack
    #                 in_aud_feat_arr = numpy.vstack(
    #                        [in_aud_feat_arr, aud_feat])

    #             ###
    #             # Saving sub sliced audio of the input audio track
    #             filename = sub_sliced_input_destination \
    #                 + "/" + str(sub_slice_index).zfill(3) \
    #                 + " " + str(indx) + " " + rhythm \
    #                 + ".wav"
    #             librosa.output.write_wav(filename, aud_slice, sr)
    #             sub_slice_index += 1
    #             ###

    #         one_two_three_four_dict_list.append(one_two_three_four_dict)

    #     return (in_aud_feat_arr, one_two_three_four_dict_list, tempo, \
    #         [])
    # # End if not is_use_long_audio
    #     ####
    # else:
    #     pass
    #     # print("halt")


    print("Extracting input audio features...")

    down_beat_sixteenth_note_indices = [] # return this one too
    
       
    quarter_note_index = 1 # Just initialize as one 
        #(for the first bar's sake), 
        # but it will go from 1 to 4 only
        # If downbeat, reset to 1
            # then add "1" as the key to the 1 e & a 2 e...dict
        # If not downbeat, just increment to get keys "2", "3", and "4"
    
    onset_index = 0
    
    key_to_num_dict = {
        "e": "2",
        "&": "3",
        "a": "4"
    } # If key is a number, return "1" using value = d.get(key, "1")

    # Extract the features of each interval then save as a stacked array.
    for q_note_ind, beat_dict in enumerate(one_e_and_a_dict_list):
        # print("q_note_ind: " + str(q_note_ind))

        one_two_three_four_dict = {} # Will be appended to
            # one_two_three_four_dict_list

        print("\nq_note_ind: {}".format(q_note_ind))

        for sxtnth_note_ind, (key, val) in enumerate(beat_dict.items()):
            print("key: " + key)
            print("val[0]: " + str(val[0]))
            print("val[1]: " + str(val[1]))

            if key == "1":
                key = str(quarter_note_index) # values 1 to 4

            one_two_three_four_dict[key] = val

            audio = y[val[0]:val[1]] # audio index range
            print("q_note_ind: {}".format(q_note_ind))
            print("key: {}".format(key))
            # print("audio: {}".format(audio))
            print("audio: ")
            print(audio)

            if len(audio) == 0:
                print("An audio is empty.")
                print("Solution. Identify while slicing the audio.")
                print("y: {}".format(y))
                # sys.exit()
                continue
        
            print("Extracting...")
            # Why is sub slice folder not filled?

            aud_feat = extract_audio_features(y=audio, sr=sr)
            # save sliced audio to listen for verification

            # filename = sub_sliced_input_destination + "/" \
            #     + str(onset_index).zfill(3) + ".wav"
            # filename = sub_sliced_input_destination + "/" \
            #     + str(q_note_ind) + "_" + key \
            #     + ".wav"

            rhy = key_to_num_dict.get(key, "1") # Default is "1"
            # print("rhy: {}".format(rhy))
            filename = sub_sliced_input_destination + "/" \
                + str(q_note_ind) + "_" + rhy + "_" + key \
                + ".wav"
            print("filename: {}".format(filename))

            librosa.output.write_wav(filename, audio, sr)
            onset_index += 1

            

            # print("q_note_ind: " + str(q_note_ind))
            # print("sxtnth_note_ind: " + str(sxtnth_note_ind))

            if q_note_ind == 0 and sxtnth_note_ind == 0:
                # Initialize array
                print("aud_feat: ")
                print(aud_feat)
                print("aud_feat.shape: {}".format(aud_feat.shape))
                in_aud_feat_arr = numpy.array(aud_feat)
              # print("in_aud_feat_arr initialized...?")
            else: # stack
                # print("q_note_ind: " + str(q_note_ind))
                # print("sxtnth_note_ind: " + str(sxtnth_note_ind))

                print("\nin_aud_feat_arr.shape: {}"\
                    .format(in_aud_feat_arr.shape))
                print("aud_feat.shape: {}".format(aud_feat.shape))
                # print("\nin_aud_feat_arr: {}".format(in_aud_feat_arr))
                # print("aud_feat: {}".format(aud_feat))
                in_aud_feat_arr = numpy.vstack([in_aud_feat_arr, aud_feat])
        # End for each 1-e-&-a, or after every quarter note, feat extraction

        # Update every quarter note, because each dictionary is a quarter note
        quarter_note_index += 1 # Increment,
        if quarter_note_index == 5:
            quarter_note_index = 1 # reset
            # but it will go from 1 to 4 only
            # If downbeat, reset to 1
                # then add "1" as the key to the 1 e & a 2 e...dict
            # If not downbeat, just increment to get keys "2", "3", and "4"

        # Add the dictionary to one_two_three_four_dict_list
        one_two_three_four_dict_list.append(one_two_three_four_dict)

    # End for each quarter note duration
        # in terms of one dictionary per duration,
        # and the dictionary may have keys "1", "e", "&", "a"


    print("\nin_aud_feat_arr.shape: " + str(in_aud_feat_arr.shape))

    print("down_beat_sixteenth_note_indices:")
    print(down_beat_sixteenth_note_indices)

    # print("empty_aud: {}".format(empty_aud))


    # print("in_aud_feat_arr: {}".format(in_aud_feat_arr))
    # print("in_aud_feat_arr.shape: {}".format(in_aud_feat_arr.shape))
    


    return (in_aud_feat_arr, one_two_three_four_dict_list, tempo, \
        down_beat_sixteenth_note_indices)
    # return in_aud_feat_arr

# End process_input()




def slice_input(audio_track_dir, beat_frame_arr, add_front_as_onset, 
    is_front_extended):
    print("\nSlicing audio input...")

    print("Loading audio: " + audio_track_dir)
    y, sr = librosa.load(audio_track_dir)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

    # Index array
    full_audio_onset_indices = librosa.onset.onset_detect(
                        y=y, # Function formal parameter
                        sr=sr,
                        # backtrack=True, # If true, onset index will
                            # be adjusted right before the onset attack
                        units="samples") # set as indices not frames
                        # get onset_indices
    
    # Index array
    backtracked_full_audio_onset_indices = librosa.onset.onset_detect(
                        y=y, # Function formal parameter
                        sr=sr,
                        backtrack=True, # If true, onset index will
                            # be adjusted right before the onset attack
                        units="samples") # set as indices not frames
                        # get onset_indices

    # Backtracked vs not backtracked onset difference
    if len(full_audio_onset_indices) > 0:
        backtrack_onset_diff = full_audio_onset_indices \
                                - backtracked_full_audio_onset_indices
        backtrack_onset_diff_ave = int(numpy.mean(backtrack_onset_diff))
    else:
        backtrack_onset_diff_ave = 0

    print("Before...")
    print("full_audio_onset_indices: {}".format(full_audio_onset_indices))
    print("backtracked_full_audio_onset_indices: {}"\
        .format(backtracked_full_audio_onset_indices))

    beat_frame_indices = librosa.frames_to_samples(beat_frame_arr)
    
    # if add_front_as_onset: # Consider adding an onset manually in front.
    #     # This is the reference.
    #     print("\nTrue\n")
        
    #     # if len(beat_frame_indices) >= 2:
    #     full_audio_onset_indices = numpy.append(
    #         [beat_frame_indices[0]], full_audio_onset_indices)
    #     backtracked_front = beat_frame_indices[0] - backtrack_onset_diff_ave
    #     if backtracked_front < 0:
    #         backtracked_front = 0
    #     backtracked_full_audio_onset_indices = numpy.append(
    #         [backtracked_front], backtracked_full_audio_onset_indices)


    ##### Brought ouside for the succeeding if clause
    # because the some variables will be used later outside if.
    quarter_len = beat_frame_arr[1] - beat_frame_arr[0] # in frames
    backtrack_frame_len \
        = librosa.samples_to_frames(backtrack_onset_diff_ave)
    first_part_len = quarter_len  - backtrack_frame_len
        # The length was subtracted up to about 85%, because the end
        # might capture the next beat onset.
    begin_frame = beat_frame_arr[0]
    end_frame = beat_frame_arr[0] + first_part_len
    begin_sample = librosa.frames_to_samples(begin_frame)
    end_sample = librosa.frames_to_samples(end_frame)
    extension \
        = y[begin_sample: end_sample]
    energy_array = librosa.feature.rms(y=extension)

    if is_front_extended: # Manually detect onsets in front.
        # Within the first quarter note, compare the onsets.

        # quarter_len = beat_frame_arr[1] - beat_frame_arr[0] # in frames
        # backtrack_frame_len \
        #     = librosa.samples_to_frames(backtrack_onset_diff_ave)

        # first_part_len = quarter_len  - backtrack_frame_len
        #     # The length was subtracted up to about 85%, because the end
        #     # might capture the next beat onset.

        # # print("quarter_len: {}".format(quarter_len))
        # # print("first_part_len: {}".format(first_part_len))

        # begin_frame = beat_frame_arr[0]
        # end_frame = beat_frame_arr[0] + first_part_len

        # begin_sample = librosa.frames_to_samples(begin_frame)
        # end_sample = librosa.frames_to_samples(end_frame)

        # # extension \
        # #     = y[beat_frame_arr[0]: beat_frame_arr[0] + first_part_len]
        # extension \
        #     = y[begin_sample: end_sample]
        # energy_array = librosa.feature.rms(y=extension)

        ##### ^ put outside if clause

        # print("energy_array.shape: {}".format(energy_array.shape))
        # print("energy_array.shape[0]: {}".format(energy_array.shape[0]))
        # print("energy_array.shape[1]: {}".format(energy_array.shape[1]))

        # save extension as audio
        librosa.output.write_wav("extension.wav", extension, sr)

        # has_onset = False
        # If any of the values in the array energy_array (rms) 
        # if (energy.any() >= 0.1 for energy in energy_array):
        #     has_onset = True
        # if has_onset == False:
        #     # Remove the inserted extension.
        #     beat_frame_arr = beat_frame_arr[1:]

        pos1 = [] # 1
        pos2 = [] # e
        pos3 = [] # &
        pos4 = [] # a

        div_len = int(energy_array.shape[1]/4)
        energy_array = librosa.feature.rms(y=extension)

        # print("energy_array: {}".format(energy_array))
        # print("div_len: {}".format(div_len))


        for i, energy in enumerate(energy_array[0]):
            if i < div_len:
                pos1.append(energy)
            elif i < div_len*2:
                pos2.append(energy)
            elif i < div_len*3:
                pos3.append(energy)
            else:
                pos4.append(energy)

        # print("pos1: {}".format(pos1))
        # print("pos2: {}".format(pos2))
        # print("pos3: {}".format(pos3))
        # print("pos4: {}".format(pos4))

        has_onest_at_1 = False
        has_onest_at_e = False
        has_onest_at_n = False
        has_onest_at_a = False

        # if (energy.any() >= 0.1 for energy in pos1):
        #     has_onest_at_1 = True
        # if (energy.any() >= 0.1 for energy in pos2):
        #     has_onest_at_e = True
        # if (energy.any() >= 0.1 for energy in pos3):
        #     has_onest_at_n = True
        # if (energy.any() >= 0.1 for energy in pos4):
        #     has_onest_at_a = True

        # Check if there's energy > 0.1 on the first half of each positions
        half_div_len = div_len//2

        for i in range(half_div_len):
            if pos1[i] > 0.1:
                has_onest_at_1 = True
                break

        for i in range(half_div_len):
            if pos2[i] > 0.1:
                has_onest_at_e = True
                break

        for i in range(half_div_len):
            if pos3[i] > 0.1:
                has_onest_at_n = True
                break

        for i in range(half_div_len):
            if pos4[i] > 0.1:
                has_onest_at_a = True
                break

        # print("has_onest_at_1: {}".format(has_onest_at_1))
        # print("has_onest_at_e: {}".format(has_onest_at_e))
        # print("has_onest_at_n: {}".format(has_onest_at_n))
        # print("has_onest_at_a: {}".format(has_onest_at_a))

        # Compare with the identified onsets using librosa.
        # Maybe even ignore librosa onsets, and replace the first
        # quarter note onsets with the onsets detected using rms.

        # If any onset was detected using rms
        if has_onest_at_1 or has_onest_at_e or has_onest_at_n or has_onest_at_a:
            
            # Remove the automatic onsets before end_sample of 
            # quarter extension to avoid reduncancy.
            # I guess the rms onsets were already backtracked
            # so use backtracked first.
            backtracks_to_remove = []
            for backt_onset in backtracked_full_audio_onset_indices:
                if backt_onset > end_sample - backtrack_onset_diff_ave: 
                # if backt_onset > begin_sample - first_part_len: 
                    # Remove just up to end_sample...
                    break # ...of the front extension.
                else:
                    backtracks_to_remove.append(backt_onset)
            # Now, remove... finc the index--numpy.delete(a, index)
            for element in backtracks_to_remove:
                # Remove all elements of backtracked_full_audio_onset_indices equal
                # backtracked_full_audio_onset_indices to 
                backtracked_full_audio_onset_indices \
                    = backtracked_full_audio_onset_indices[
                        backtracked_full_audio_onset_indices != element]

            # Follow by removing also front onsets from the unbacktracked onsets.
            onsets_to_remove = []
            for unbackt_onset in full_audio_onset_indices:
                if unbackt_onset > end_sample - backtrack_onset_diff_ave:
                # if backt_onset > begin_sample - first_part_len: 
                    # Remove just up to end_sample, adjusted forward...
                    break # ...of the front extension.
                else:
                    onsets_to_remove.append(unbackt_onset)
            # Now, remove... finc the index--numpy.delete(a, index)
            for element in onsets_to_remove:
                # Remove all elements of full_audio_onset_indices equal
                # full_audio_onset_indices to 
                full_audio_onset_indices \
                    = full_audio_onset_indices[
                        full_audio_onset_indices != element]

            # After removing possible extension onsets, replace them with
            # onsets detected using rms.

            # extension = y[begin_sample: end_sample]
            ext_ind_dif = end_sample - begin_sample
            marker_len = ext_ind_dif//4
            marker1 = begin_sample
            marker2 = begin_sample + marker_len
            marker3 = begin_sample + marker_len * 2
            marker4 = begin_sample + marker_len * 3

            if has_onest_at_a:
                backtracked_full_audio_onset_indices = numpy.append(
                    [marker4], backtracked_full_audio_onset_indices)
                full_audio_onset_indices = numpy.append(
                    [marker4 + backtrack_onset_diff_ave], 
                                            full_audio_onset_indices)
            if has_onest_at_n:
                backtracked_full_audio_onset_indices = numpy.append(
                    [marker3], backtracked_full_audio_onset_indices)
                full_audio_onset_indices = numpy.append(
                    [marker3 + backtrack_onset_diff_ave], 
                                            full_audio_onset_indices)
            if has_onest_at_e:
                backtracked_full_audio_onset_indices = numpy.append(
                    [marker2], backtracked_full_audio_onset_indices)
                full_audio_onset_indices = numpy.append(
                    [marker2 + backtrack_onset_diff_ave], 
                                            full_audio_onset_indices)
            if has_onest_at_1:
                backtracked_full_audio_onset_indices = numpy.append(
                    [marker1], backtracked_full_audio_onset_indices)
                full_audio_onset_indices = numpy.append(
                    [marker1 + backtrack_onset_diff_ave], 
                                            full_audio_onset_indices)
            
            
        # End if any onset was detected from the extension

    print("\nAfter...")
    print("full_audio_onset_indices: {}".format(full_audio_onset_indices))
    print("backtracked_full_audio_onset_indices: {}"\
        .format(backtracked_full_audio_onset_indices))

    print("\nbeat_frame_indices: {}".format(beat_frame_indices))
    print("begin_sample: {}".format(begin_sample))
    print("end_sample: {}".format(end_sample))
    print("first_part_len: {}".format(first_part_len))
    print("backtrack_onset_diff_ave: {}".format(backtrack_onset_diff_ave))

    # print("\nYou've got good timing on each quarter notes. Use that to " + \
    #     "to get the right division of onsets. ")

    len_to_frame = librosa.samples_to_frames(len(y)) # The last audio frame

    delete_folder("./Onsets")
    create_folder("./Onsets")

    backtracked_full_audio_onset_indices_up_to_end \
        = numpy.append(backtracked_full_audio_onset_indices, len_to_frame)

    onset_starts = backtracked_full_audio_onset_indices_up_to_end[:-1]
    onset_stops = backtracked_full_audio_onset_indices_up_to_end[1:]

    for i, (start, stop) in enumerate(zip(onset_starts, onset_stops)):
        print("{}: {}".format(i, start))
        audio = y[start:stop]
        # if len(audio) == 0:
            # print("audio ")
        filename = "./Onsets" + "/" + str(i).zfill(3) + ".wav"
        librosa.output.write_wav(filename, audio, sr)
    
    # halt()

    print("\nIt seems in base_snare_hihat_loop, the extended " \
        + "starting front is not recognized as an onset." \
        + " How does that affect midi output?")

    # Add the indices on both ends of the two onset indices list above
    # diff = full_audio_onset_indices[0] 
    #        - backtracked_full_audio_onset_indices[0]
    # full_audio_onset_indices \
    #           = numpy.append([0], full_audio_onset_indices)
                # Add time 0.0 because we assumed it has an onset.
    # backtracked_full_audio_onset_indices \
    #           = numpy.append([diff], backtracked_full_audio_onset_indices)
    # full_audio_onset_indices \
    #           = numpy.append(full_audio_onset_indices, [len(y) - 1])
    # backtracked_full_audio_onset_indices \
    #           = numpy.append(backtracked_full_audio_onset_indices,
    #               [len(y) - diff])

    # onset_indices_2 = librosa.onset.onset_detect(
    #     onset_envelope=o_env, sr=sr, units="samples")


        # o_env = librosa.onset.onset_strength(y, sr=sr)
    # print("len(y): " + str(len(y)))
    # print("onset_env:")
    # print(o_env)
    # print("onset_env size:")
    # print(o_env.size)
    # print("onset_env [:20]:")
    # print(o_env[5000:7000])

    # Convert the frame array to audio sample index array
    audio_sample_index_arr = librosa.frames_to_samples(beat_frame_arr)
    
    # print("\nfirst quarter: {}".format(audio_sample_index_arr[0]))
    # print("first onset: {}".format(backtracked_full_audio_onset_indices[0]))
    # diff = audio_sample_index_arr[0] - backtracked_full_audio_onset_indices[0]
    # print("difference: {}".format(diff))
    # print("bactrack: {}".format(backtrack_onset_diff_ave))
    

    # After getting the audio index of every quarter note, maybe except
    # those at the beginning.
    # Getting the average difference between the audio onset indices.
    # That should be the bpm converted to index length.
    # beginning = audio_sample_index_arr[:-1] # without the last index
    # end = audio_sample_index_arr[1:] # without the first index
    # differences = end - beginning
    # average_diff = numpy.mean(differences)
    
    # # Using the average difference, countdown the audio indices
    # # in increments of the average difference, just before you reach
    # # index zero.
    # starting_indices = [] # then use this list to create a new numpy array
    #     # then, combine this with the original audio indices
    # smallest_index = audio_sample_index_arr[0]
    # print("smallest_index: {}".format(smallest_index))
    # print("average_diff: {}".format(average_diff))
    # for index in reversed(range(0, smallest_index, average_diff)):
    #     # decrement by average_diff
    #     starting_indices.insert(0, index) # Push at the beginning
    # print("starting_indices: {}".format(starting_indices))
    # The steps above seems unnecessary


    # Just appending the last audio index there is from the lenth of the audio
    # Comment out to disregard the audio end
    ##audio_sample_index_arr = numpy\
    #        .concatenate(audio_sample_index_arr, len(y))
    # Create the arrays of starting indices and ending indices

    # Adjust backward a bit the the sample indices so that when the audio
    # is sliced, aka. backtrack
    # audio_sample_index_arr = audio_sample_index_arr - backtrack_offset
        # backtrack_offset = 1100 # optimized manually, global variable
    # However, the first element could become negative.

    # # Get the onset before the first automatically identifed onset
    # beat_len = audio_sample_index_arr[1] - audio_sample_index_arr[0]
    # print("beat_len 1: {}".format(beat_len))
    # beat_len = audio_sample_index_arr[2] - audio_sample_index_arr[1]
    # print("beat_len 2: {}".format(beat_len))
    # beat_len = audio_sample_index_arr[3] - audio_sample_index_arr[2]
    # print("beat_len 3: {}".format(beat_len))
    # print("heare in input_ops...")
    # print("audio_sample_index_arr: {}".format(audio_sample_index_arr))

    # Get the average difference
    beat_len_starts = audio_sample_index_arr[:-1]
    beat_len_ends = audio_sample_index_arr[1:]
    print("beat_len_starts: {}".format(beat_len_starts))
    print("beat_len_ends: {}".format(beat_len_ends))

    beat_len_diffs = beat_len_ends - beat_len_starts
    beat_len = numpy.mean(beat_len_diffs)
    beat_len = int(beat_len)
    print("beat_len ave: {}".format(beat_len))

        # Measuring the interval each onsets by sampling the first two beats
    first_beat = audio_sample_index_arr[0] - beat_len

    # # Push the first beat if valid, meaning not negative
    # if first_beat >= 0:
    #     # pass
    #     count = 0
    #     while first_beat >= 0:
    #       audio_sample_index_arr \
    #           = numpy.append([first_beat], audio_sample_index_arr)
    #       first_beat = audio_sample_index_arr[0] - beat_len
    #       count += 1
    #     print("Added an index in front, count: {}...".format(count))
    # # else: # append index zero in front
    #     # pass
    # audio_sample_index_arr = numpy.append([0], audio_sample_index_arr)
    # print("Added the zero index in front...")
    # print("audio_sample_index_arr: {}".format(audio_sample_index_arr))

    # print("len(audio_sample_index_arr): {}"\
    #        .format(len(audio_sample_index_arr)))
    
    last_beat = audio_sample_index_arr[-1] + beat_len
    # Do the same thing as finding the first beats,
    # but for the last beats.
    # if last_beat < len(y):
    #   audio_sample_index_arr \
    #         = numpy.append(audio_sample_index_arr, [last_beat])
    #   print("Added another index at the back...")
    # else:
    #   audio_sample_index_arr \
    #         = numpy.append(audio_sample_index_arr, [len(y)-1])
    #   print("Added another index at the back, which is len(y) - 1...")

    # add the last index...

    print("len(y): {}".format(len(y)))
    print("y[-1]: {}".format(y[-1]))
    print("last_beat: {}".format(last_beat))
    print("")

    # if last_beat < len(y): 
    #     # pass
    #     index = 0
    #     while last_beat < len(y):
    #         audio_sample_index_arr \
    #             = numpy.append(audio_sample_index_arr, [last_beat])
    #         last_beat += int(beat_len)-100

    #     print("Added {} quarter note(s) duration at the end..."\
    #                .format(index+1))
    # # else: # append last index at the end of the audio
    # audio_sample_index_arr \
    #     = numpy.append(audio_sample_index_arr, [int(len(y)-1)])
    # print("Added the last index at the end...")
        # pass
    

    """ Identify the quarter note, eighth note, and sixteenth note positions """
    
    # Quarter note positions has already been identified by the computed beats
    quarter_note_pos_list = audio_sample_index_arr
    # print("\nquarter_note_pos_list:")
    # print(quarter_note_pos_list)
    # Actually, this could be either a beat of fourths or eighths
    # But it's alright


    """ NOTE: Immediatelly cutting the sample track into sixteenth notes
        produces new instrument hit rather than a continuous single instrument
        hit. This is based on how the split audio sounds.
        
        The solution is after the beat locations have been identified
        (usually fourths, but we'll see if it needs to be a half note length),
        using the given interval, use librosa.beat.beat_track to get the
        sub time and the sub onset of there is one. If none, skip slicing the
        sub audio and mark a single hit with the corresponding note length,
        which could be a quarter note, or even a half note.

        Another solution is to count the offsets and identify their locations
        to see what type of note is played. Detect onsets.

        So, what did I actually do?
    """

    # Process the each sound intervals
    # to look for another sub grouping of more onsets
    # In other words, identify if there's onset within the interval,
    # or if it's already just a single continuous hit
    # of a quarter note or a half note 

    # # Get the intervals
    start_ind_list = quarter_note_pos_list[:-1]
        # All indices except the last one
    stop_ind_list = quarter_note_pos_list[1:]
        # All indices except the first one
        # starts  |----------------------|....
        # stops    ....|----------------------|
        # Now, starts[i] to stops[i] represent the ith interval


    # # Getting the average length of the quarter notes
    # differences = stop_ind_list - start_ind_list
    #     # Trim the outlying intervals from ends of the audio
    # average_diff = numpy.mean(differences)
    # average_interval = numpy.around(average_diff) # round off
    # print("\naverage_interval: " + str(average_interval))
    # sample_diff = quarter_note_pos_list[4] - quarter_note_pos_list[3]
    # print("\nsample_diff: " + str(sample_diff))
    average_interval = beat_len 


    show_note_division(ave_int=average_interval)
    """ Note divisions
            # average_interval is the average quarter note duration
            # ave_int = average_interval
        beat    index range
        1       [0/8 ave_int : 1/8 ave_int]
        e       [1/8 ave_int : 3/8 ave_int]
        &       [3/8 ave_int : 5/8 ave_int]
        a       [5/8 ave_int : 7/8 ave_int]
        1 or 2  [7/8 ave_int : 8/8 ave_int]
    """

    one_e_and_a_dict_list = [] # Will hold all the ranges

    prev_onset_diffs = numpy.zeros(2) # What is this for?
        # This will be used

    # For identifying rhythms between each quarter note...rewriting this...
    onset_index = 0
    backtrack = int(backtrack_onset_diff_ave)

    # For each quarter note interval
    for i, (start, stop) in enumerate(zip(start_ind_list, stop_ind_list)):

        """ What's going on here? """

        # backtrack = int(backtrack/2)

        # To cut audio properly
        # start -= backtrack # Uncomment this,
        # stop -= backtrack # and also uncomment this
            # to have correct onset slices.
            # But since May 27, 2020. These should be commented out.
        if start < 0: # negative
            start = 0
        

        onset_indices = []
        # quarter_note_pos_list is already backtracked manually
        # full_audio_onset_indices is not backtracked

        backtracked_onset_indices = []

        # print("\nfull_audio_onset_indices: {}"\
        #   .format(full_audio_onset_indices))
        # print("\nlen(full_audio_onset_indices): {}"\
        #   .format(len(full_audio_onset_indices)))


        # Traverse all the full_audio_onset_indices, the onset indices
        # to the quarter note duration it belongs.

        # while onset_index < len(full_audio_onset_indices) \
            # and full_audio_onset_indices[onset_index] < stop :
        # while onset_index < len(backtracked_full_audio_onset_indices) \
            # and backtracked_full_audio_onset_indices[onset_index] < stop :
        while onset_index < len(full_audio_onset_indices) \
            and full_audio_onset_indices[onset_index] \
                < stop - backtrack_onset_diff_ave : # The stop is bactracked.

            onset_indices.append(full_audio_onset_indices[onset_index])

            backtracked_onset_indices\
                    .append(backtracked_full_audio_onset_indices[onset_index])
            
            onset_index += 1

        print("\ni: {}".format(i))
        print("quarter note")
        print("\tstart: {}".format(start))
        print("\tstop: {}".format(stop))
        print("\t\tdiff: {}".format(start - stop))
        print("onset_indices: {}".format(onset_indices))
        print("backtracked_onset_indices: {}"\
            .format(backtracked_onset_indices))

        # onset_diffs = numpy.array(onset_indices) \
                      # - numpy.array(backtracked_onset_indices)
        # if math.isnan(numpy.mean(onset_diffs)):
        #   onset_diffs = prev_onset_diffs

        if len(onset_indices) == 0 or len(backtracked_onset_indices) == 0:
            onset_diffs = prev_onset_diffs
        else:
            onset_diffs = numpy.array(onset_indices) \
                             - numpy.array(backtracked_onset_indices)

        beats_dict = identify_beats_per_quarter_note_duration(
                        onsets=onset_indices, ave_int=average_interval,
                        start_ind=start,
                        backtracked_onset_indices=backtracked_onset_indices,
                        onset_diffs=onset_diffs,
                        stop_ind=stop)
            # Example, beats_dict["1"]: [1024:3584]

        prev_onset_diffs = onset_diffs 

        print("\n")

        backtracked_onset_indices = []

        # Append the list of all the other one_e_and_a's (beats_dict)
        # with the identified beat ranges within a quarter note to the

        one_e_and_a_dict_list.append(beats_dict) 
            # append because it's just one at a time

        # if i == 20:
        #     halt()

        # here, left with how count sub offsets
    # End for each quarter  note interval

    ave_onset_diff = int(numpy.mean(onset_diffs))
    if numpy.isnan(ave_onset_diff):
        ave_onset_diff = 0

    # Show all the 1e&a's
    # Ease up tracking index by using enumerate() 
    for index, beats_dict in enumerate(one_e_and_a_dict_list):
        print("\nindex: " + str(index))
        for key, val in beats_dict.items():
            print(key, val)
    # End show all the 1e&a's

    # Commented out if you want to listen how the input was sliced
    # return one_e_and_a_dict_list

    """ Skip saving the identified onset segments into a separate wave file """


    possible_onset_possitions = quarter_note_pos_list


    # skip_subdivision = True
    # if not skip_subdivision:
    #     # Eighth notes are at the middle of the quarter notes
    #     ith_positions = quarter_note_pos_list[0:-1] # starts
    #         # All indices except the last one
    #     i_plus_1_positions = quarter_note_pos_list[1:] # stops
    #         # All indices except the first one
    #     # Getting the average
    #     sums_list = ith_positions + i_plus_1_positions #
    #     eight_note_pos_list = sums_list / 2 # average
    #     print("\neight_note_pos_list:")
    #     print(eight_note_pos_list)

        
    #     # The computed quarter note and eighth note positions combined, 
    #     # because it will be required to get the sixteenth note positions
    #     eighth_note_beats \
    #         = numpy.append(quarter_note_pos_list, eight_note_pos_list)
    #         # combining the the quarter and eights into an array
    #     eighth_note_beats = numpy.sort(eighth_note_beats)
    #         # Sixteenth note positions are in between 
    #         # the quarter and eighth note positons, eighth_note_beats


    #     # Sixteenth notes are at the middle of the eighth_note_beats
    #     ith_positions = eighth_note_beats[0:-1] # starts
    #         # All indices except the last one
    #     i_plus_1_positions = eighth_note_beats[1:] # stops
    #         # All indices except the first one
    #     # Getting the average
    #     sums_list = ith_positions + i_plus_1_positions #
    #     sixteenth_note_pos_list = sums_list / 2 # average
    #     print("\nsixteenth_note_pos_list:")
    #     print(sixteenth_note_pos_list)


    #     # Combine the recently computed sixteenth note positions
    #     # to the previously computed eight note beats, to produce a complete 
    #     # sixteenth note measure
    #     sixteenth_note_beats \
    #         = numpy.append(sixteenth_note_pos_list, eighth_note_beats)
    #         # combining the the sixteenth note positions with the quarter note
    #         # positions and the eighth notes position into a single array
    #     sixteenth_note_beats = numpy.sort(sixteenth_note_beats)
    #         # The sixteenth note beats capture all the possible drum onsets 
    #     possible_onset_possitions = sixteenth_note_beats
    # # End if not skip_subdivision


    # print("\npossible_onset_possitions:")
    # print(possible_onset_possitions)

    print("\npossible_onset_possitions.size:")
    print(possible_onset_possitions.size)

    # print("\naudio_sample_index_arr:")
    # print(audio_sample_index_arr)
    # # Must be converted to a list of integers
    # possib_ons_pos_list = possible_onset_possitions.tolist() # numpy to list
    # possib_ons_pos_list = [round(x) for x in possib_ons_pos_list] 
    #     # float list to integer list
    # print("\npossib_ons_pos_list:")
    # print(possib_ons_pos_list)


    starts = possible_onset_possitions[0:-1] # All indices except the last one
    stops = possible_onset_possitions[1:] # All indices except the first one
        # starts  |----------------------|....
        # stops    ....|----------------------|


    # A note about subgroup of notes was here

    # # Try to delete Sliced Input Folder
    # try:
    #   shutil.rmtree(sliced_input_destination)
    # except OSError as e:
    #   print("Error: %s - %s." % (e.filename, e.strerror))
    delete_folder(sliced_input_destination)

    # Try to create Sliced Input Folder
    create_folder(sliced_input_destination)

    # This is just saving the quarter note slices for referece,
    # and has nothing to do with classifcation.
    # The start, stop reference here is the tracked quarter beats

    # Saving sliced audio of the input audio track
    for i, (start, stop) in enumerate(zip(starts, stops)):
        # ave_onset_diff # When comparing backtracked vs normal onset indices
        start -= int(ave_onset_diff/2)
        stop -= int(ave_onset_diff/2)
        if start < 0:
            start = 0

        audio = y[start:stop]
        # if len(audio) == 0:
            # print("audio ")
        filename = sliced_input_destination + "/" + str(i).zfill(3) + ".wav"
        librosa.output.write_wav(filename, audio, sr)

        # if i == 20:
        #     print("Hard code limit of 20 sliced beat interval saved as audio")
        #     break

    # Just including to the sliced input audio destination the tempo
    # output_bpm = sliced_input_destination + "/bpm.csv"
    create_folder("./temp")
    output_bpm = "temp" + "/bpm.csv"
    # numpy.savetxt(output_bpm, numpy.zeros(1) + tempo, delimiter=',')
    # print("tempo:")
    # print(tempo)
    # print([tempo,])
    numpy.savetxt(output_bpm, [tempo,], delimiter=',')

    return one_e_and_a_dict_list
    # There's another return statement before this one
    # This return statement here wont be used if
    # Saving the sliced audio will be skipped for debugging

# End def slice_input()



def show_note_division(ave_int):
    """ Note divisions
                # average_interval is the average quarter note duration
                # ave_int = average_interval
            beat    index range
            1       [0/8 ave_int : 1/8 ave_int]
            e       [1/8 ave_int : 3/8 ave_int]
            &       [3/8 ave_int : 5/8 ave_int]
            a       [5/8 ave_int : 7/8 ave_int]
            1 or 2  [7/8 ave_int : 8/8 ave_int]
        """

    # Adjust the first beat a bit forward equivalent to backtrack_offset

    # backtrack_offset = 1100 # optimized manually, global variable
    # Although it seems that in this program,
    # the first beat offset start at 1536

    # However, the "for each quarter note intervals" uses backtracking=True
    # So no need to ajust for now

    print("\nNote division:")
    print("1 [ " + str(((0/8)*ave_int)) + ":" + str(((1/8)*ave_int)) + "]" \
        + " | e [" + str(((1/8)*ave_int)) + ":" + str(((3/8)*ave_int)) + "]" \
        + " | & [" + str(((3/8)*ave_int)) + ":" + str(((5/8)*ave_int)) + "]" \
        + " | a [" + str(((5/8)*ave_int)) + ":" + str(((7/8)*ave_int)) + "]")
# End def show_note_division():



def identify_beats_per_quarter_note_duration(onsets, ave_int, start_ind,
    backtracked_onset_indices, onset_diffs, stop_ind):

    print("\nIdentifying beats per quarter note duration...")

    # Getting average difference between onsets and backtracked onsets
    # print("onsets: {}".format(onsets))
    # print("backtracked_onset_indices: {}".format(backtracked_onset_indices))

    # onset_dif = numpy.array(onsets) - numpy.array(backtracked_onset_indices)
    backtrack_len = int(numpy.mean(onset_diffs))
    # backtrack_len = 0

    beats_range_dict = {} # eg "1": [1024, 9216], where the range was past
        # the e_limit, probably because there was no onset at 'e' position

    # For onsets list, shift all the values such that onsets[0]
    # is close to zero.
    # Or just adjust the limits by adding the start index
    # Tbis is necessary to compare the limits , intervals between each note end

    if len(onsets) == 0:
        print("Here: Not all quarter notes have onset.")
        # beats_range_dict["1"] = [start_ind, ave_int]
        # sys.exit() # No.
        return beats_range_dict

    # # ave_int or length of a quarter note
    # zero_relative_one_limit = (1/8)*ave_int
    # zero_relative_one_limit = int(zero_relative_one_limit)
    # zero_relative_e_limit = (3/8)*ave_int
    # zero_relative_e_limit = int(zero_relative_e_limit)
    # zero_relative_and_limit = (5/8)*ave_int
    # zero_relative_and_limit = int(zero_relative_and_limit)
    # zero_relative_a_limit = (7/8)*ave_int
    # zero_relative_a_limit = int(zero_relative_a_limit)

    # zero_relative_one_limit = (2/8)*ave_int
    # zero_relative_one_limit = int(zero_relative_one_limit)
    # zero_relative_e_limit = (4/8)*ave_int
    # zero_relative_e_limit = int(zero_relative_e_limit)
    # zero_relative_and_limit = (6/8)*ave_int
    # zero_relative_and_limit = int(zero_relative_and_limit)
    # zero_relative_a_limit = (8/8)*ave_int
    # zero_relative_a_limit = int(zero_relative_a_limit)

    # actual_beat_len = stop_ind - start_ind
    # zero_relative_one_limit = (2/8)*actual_beat_len
    # zero_relative_one_limit = int(zero_relative_one_limit)
    # zero_relative_e_limit = (4/8)*actual_beat_len
    # zero_relative_e_limit = int(zero_relative_e_limit)
    # zero_relative_and_limit = (6/8)*actual_beat_len
    # zero_relative_and_limit = int(zero_relative_and_limit)
    # zero_relative_a_limit = (8/8)*actual_beat_len
    # zero_relative_a_limit = int(zero_relative_a_limit)

    actual_beat_len = stop_ind - start_ind
    zero_relative_one_limit = (1/8)*actual_beat_len
    zero_relative_one_limit = int(zero_relative_one_limit)
    zero_relative_e_limit = (3/8)*actual_beat_len
    zero_relative_e_limit = int(zero_relative_e_limit)
    zero_relative_and_limit = (5/8)*actual_beat_len
    zero_relative_and_limit = int(zero_relative_and_limit)
    zero_relative_a_limit = (7/8)*actual_beat_len
    zero_relative_a_limit = int(zero_relative_a_limit)

    one_limit = zero_relative_one_limit + start_ind
    e_limit = zero_relative_e_limit + start_ind
    and_limit = zero_relative_and_limit + start_ind
    a_limit = zero_relative_a_limit + start_ind

    # Here, May 26, 2020

    use_relative = True
    use_backtracked = True

    prev_onset = ""

    print("backtrack_len: {}".format(backtrack_len))
    print("ave_int: {}".format(ave_int))
    cutoff = 0
    # cutoff = 200
    # cutoff = 4000

    # backtrack_len = int(backtrack_len)
    # backtrack_len = int(backtrack_len/2)
    backtrack_len = 0

    # For every identified onset
    for onset_index, onset in enumerate(onsets):
        print("onset: " + str(onset))
        if onset < one_limit:
            start = int(start_ind + onset)
            end = int(start_ind + one_limit)
            if not use_backtracked:
                
                if use_relative:
                    beats_range_dict["1"] = [0, zero_relative_one_limit]
                else:
                    beats_range_dict["1"] = [start, end]
                print(" 1")
            else:

                """ This one is actually used... """

                # begin = onsets[onset_index] # This doesn't work, as it...
                # end = begin - backtrack_len # ...out of bounds index at main.
                begin = backtracked_onset_indices[onset_index] \
                                                        + backtrack_len
                        # backtracked_onset_indices has at most 4 indices,
                        # meaning it's just for a quarter note duration,
                        # same with onsets.
                        # A sample value of an index is 1024.
                end = begin + ave_int/4 
                end = end - cutoff

                print("\nbegin: {}".format(begin))
                print("end: {}".format(end))

                beats_range_dict["1"] = [int(begin), int(end)]
                prev_onset = "1"
                # beats_range_dict["1"] \
                #     = [ backtracked_onset_indices[onset_index],
                #         int(backtracked_onset_indices[onset_index] \
                #                                  + zero_relative_one_limit) ]
        elif onset < e_limit:
            start = int(start_ind + onset)
            end = int(start_ind + e_limit)
            if not use_backtracked:
                if use_relative:
                    beats_range_dict["e"] \
                        = [zero_relative_one_limit, zero_relative_e_limit]
                else:
                    beats_range_dict["e"] = [start, end]
                print(" e")
            else:
                # begin = onsets[onset_index]
                # end = begin - backtrack_len
                begin = backtracked_onset_indices[onset_index] \
                                                        + backtrack_len
                end = begin + ave_int/4
                end = end - cutoff

                print("\nbegin: {}".format(begin))
                print("end: {}".format(end))

                beats_range_dict["e"] = [int(begin), int(end)]
                prev_onset = "e"
                # beats_range_dict["e"] \
                #     = [ backtracked_onset_indices[onset_index],
                #         int(backtracked_onset_indices[onset_index] \
                #                                  + zero_relative_e_limit) ]
        elif onset < and_limit:
            start = int(start_ind + onset)
            end = int(start_ind + and_limit)
            if not use_backtracked:
                if use_relative:
                    beats_range_dict["&"] \
                        = [zero_relative_e_limit, zero_relative_and_limit]
                else:
                    beats_range_dict["&"] = [int(start), int(end)]
                print(" &")
            else:
                # begin = onsets[onset_index]
                # end = begin - backtrack_len
                begin = backtracked_onset_indices[onset_index] \
                                                        + backtrack_len
                end = begin + ave_int/4
                end = end - cutoff

                print("\nbegin: {}".format(begin))
                print("end: {}".format(end))

                beats_range_dict["&"] = [int(begin), int(end)]
                prev_onset = "&"

                # beats_range_dict["&"] \
                #     = [ backtracked_onset_indices[onset_index],
                #         int(backtracked_onset_indices[onset_index] \
                #                                  + zero_relative_and_limit) ]
        elif onset < a_limit:
            start = round(start_ind + onset)
            end = int(start_ind + a_limit)
            if not use_backtracked:
                if use_relative:
                    beats_range_dict["a"] \
                        = [zero_relative_and_limit, zero_relative_a_limit]
                else:
                    beats_range_dict["a"] = [start, end]
                print(" a")
            else:
                # begin = onsets[onset_index]
                # end = begin - backtrack_len
                begin = backtracked_onset_indices[onset_index] \
                                                        + backtrack_len
                end = begin + ave_int/4
                end = end - cutoff

                print("\nbegin: {}".format(begin))
                print("end: {}".format(end))

                beats_range_dict["a"] = [int(begin), int(end)]
                prev_onset = "a"
                # beats_range_dict["a"] \
                #     = [ backtracked_onset_indices[onset_index],
                #         int(backtracked_onset_indices[onset_index] \
                #                                  + zero_relative_a_limit) ]

        # We added the start index because each quarter note
        # Starts from a different position

        # Ideally, there can only be 4 onsets hear at max,
        # but if there are multiple onsets per 16th note range,
        # it should just be noice so it shouldn't really matter
    # End for every identified onset

    print("beats_range_dict: {}".format(beats_range_dict))

    return beats_range_dict
# End def identify_beats_per_quarter_note_duration(onsets):


# find down beat

def find_down_beat(input_dir):

    """ https://stackoverflow.com/questions/57384448/detecting-beat\
    -energy-with-librosa-finding-the-first-beat-of-each-bar

        This does not work well, because the energy is not always hightest
        at the first beat.
    """

    y, sr = librosa.load(input_dir)
    # get onset envelope
    onset_env = librosa.onset.onset_strength(y, sr=sr, aggregate=numpy.median)
    # get tempo and beats
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    # we assume 4/4 time
    meter = 4
    # calculate number of full measures 
    measures = (len(beats) // meter)
    # get onset strengths for the known beat positions
    # Note: this is somewhat naive, as the main strength may be *around*
    #       rather than *on* the detected beat position. 
    beat_strengths = onset_env[beats]
    # make sure we only consider full measures
    # and convert to 2d array with indices for measure and beatpos
    measure_beat_strengths = beat_strengths[:measures * meter]\
        .reshape(-1, meter)
    # add up strengths per beat position
    beat_pos_strength = numpy.sum(measure_beat_strengths, axis=0)
    # find the beat position with max strength
    downbeat_pos = numpy.argmax(beat_pos_strength)
    # convert the beat positions to the same 2d measure format
    full_measure_beats = beats[:measures * meter].reshape(-1, meter)
    # and select the beat position we want: downbeat_pos
    downbeat_frames = full_measure_beats[:, downbeat_pos]
    print('Downbeat frames: {}'.format(downbeat_frames))
    # print times
    downbeat_times = librosa.frames_to_time(downbeat_frames, sr=sr)
    print('Downbeat times in s: {}'.format(downbeat_times))
    downbeat_indices = librosa.frames_to_samples(downbeat_frames)
    print('Downbeat samples as indices {}'.format(downbeat_indices))

    # downbeat_indices = downbeat_indices - 1100 # backtrack
    return downbeat_indices

# End find_down_beat()