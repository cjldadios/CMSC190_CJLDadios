
""" input_ops.py """

import os
import sys

import numpy
import librosa


from global_vars import *
from global_ops import *
from folder_ops import *
from feature_ops import *


def process_input(input_dir):

    # load as audio in memory
    y, sr = librosa.load(input_dir)

    # print("y.shape: {}".format(y.shape))
    # print("removed zeros: {}".format(numpy.trim_zeros(y).shape))

    # https://librosa.github.io/librosa/generated/librosa.beat.beat_track.html
    # Estimate tempo (bpm) and beat location as array of frame indices
    tempo, beat_frame_arr = librosa.beat.beat_track(y=y, sr=sr)
    # Convert frames array to times array
    beat_location_time_array = librosa.frames_to_time(beat_frame_arr, sr=sr)

    print("tempo: " + str(tempo))
    # print("beat_frame_arr: ")
    # print(beat_frame_arr)
    # print("beats in time: ")
    # print(beat_location_time_array)

    # Note: 40-250 bpm, quantization

    # Returns one_e_and_a_dict_list, a list containing dictionaries
    # having keys "1, e, &, a" but some keys may be absent
    one_e_and_a_dict_list = slice_input(input_dir, beat_frame_arr)
    one_two_three_four_dict_list = []
        # This is a copy of one_e_and_a_dict_list,
            # but instead of 1 e & a 1 e & a 1 e & a 1 e & a,
            # it will be 1 e & a 2 e & a 3 e & a 4 e & a,
            # which will be ued for pattern simplification

    in_aud_feat_arr = numpy.empty(len(audio_features)*feature_array_cutoff)

    print("Extracting input audio features...")


    down_beat_sixteenth_note_indices = [] # return this one too
    if is_track_downbeat: # global variable
        down_beat_positions = find_down_beat(input_dir)
        down_beat_index = 0
        down_beat_count = len(down_beat_positions)
        sixteenth_note_index = 0
        quarter_note_index = 1 # Just initialize as one 
            #(for the first bar's sake), 
            # but it will go from 1 to 4 only
            # If downbeat, reset to 1
                # then add "1" as the key to the 1 e & a 2 e...dict
            # If not downbeat, just increment to get keys "2", "3", and "4"
        got_first_downbeat = False
        first_bar_dict_list = []

        got_first_downbeat_count = 0

        empty_aud = []

        down_ind = 0
        print("Comparing 1 pos and downbeat pos")
        for ind, quarter_dur in enumerate(one_e_and_a_dict_list):
            for key, val in quarter_dur.items():
                if down_beat_positions[down_ind] < val[0]:
                    print("Missed")
                    print("quarter: {}".format(ind))
                    print("down_beat_positions[{}]: {}"\
                        .format(down_ind, down_beat_positions[down_ind]))
                    down_ind += 1
                
                if val[0] >= down_beat_positions[down_ind] \
                    and down_beat_positions[down_ind] <= val[1] :
                    print("Caught")
                    print("quarter: {}".format(ind))
                    print("down_beat_positions[{}]: {}"\
                        .format(down_ind, down_beat_positions[down_ind]))
                    down_ind += 1
    
        # Extract the features of each interval then save as a stacked array.
        for q_note_ind, beat_dict in enumerate(one_e_and_a_dict_list):
            # print("q_note_ind: " + str(q_note_ind))

            # if q_note_ind == 4:
                # halt()

            one_two_three_four_dict = {} # Will be appended to
                # one_two_three_four_dict_list
            first_bar_quarter_note_dict = {} # Isolate the quarter notes
                # of the first (incomplete) bar

            prev_keys = [] # Use this just in case a downbeat is missed,
            prev_vals = [] # so we can backtrack and see the previous value
                # where the downbeat occured.
            is_downbeat_missed = False

            for sxtnth_note_ind, (key, val) in enumerate(beat_dict.items()):
                print("\nkey: " + key)
                print("val[0]: " + str(val[0]))
                print("val[1]: " + str(val[1]))

                is_downbeat = False # This becomes True if a downbeat is encountered

                if down_beat_index < down_beat_count: # If downbeats exhausted
                    print("sixteenth_note_index: {}".format(sixteenth_note_index))
                    print("down_beat_index: {}".format(down_beat_index))

                    # Check if a downbeat is within this audio interval
                    print("Finding down_beat_positions[{}]: {}"\
                        .format(down_beat_index, down_beat_positions[down_beat_index]))
                    print("Between {} to {}".format(val[0], val[1]))
                    print("down_beat_positions[down_beat_index]: {}"\
                        .format(down_beat_positions[down_beat_index]))
                    print("val[0]: {}".format(val[0]))
                    if down_beat_positions[down_beat_index] <= val[0]:
                        print("The first downbeat was uncaptured/missed!")
                        print("Needs to be fixed...")
                        down_beat_index += 1 # Move index to find the next downbeat
                        # sys.exit()
                        is_downbeat_missed = True
                   
                    elif down_beat_positions[down_beat_index] <= val[1]:
                        down_beat_sixteenth_note_indices\
                            .append(sixteenth_note_index)
                        down_beat_index += 1 # Move index to find the next downbeat
                        print("Downbeat? Yes")
                        is_downbeat = True
                        sixteenth_note_index += 1
                        print("key: {}, must be 1".format(key))
                        if key != "1":
                            sys.exit()
                    else:
                        print("Downbeat? No")
                        is_downbeat = False
                        sixteenth_note_index += 1

                # End if downbeats are not yet exhausted

                # if the quarter note is the downbeat
                if is_downbeat:
                    got_first_downbeat_count += 1
                    print("got_first_downbeat_count: {}"\
                        .format(got_first_downbeat_count))
                    
                    if got_first_downbeat == False:
                        if(got_first_downbeat_count == 5):
                            print("input_ops.py: Why?")
                            sys.exit()
                        # Meaning, the first downbeat is found, so
                        # push the first dict list to the
                        # one_two_three_four_dict_list, just once.
                        # But first_bar_dict_list is not yet numbered correctly
                        # There should be 4 quarter notes in a bar,
                        # so the correct starting number should be
                        #   4 - (quarter_note_index) + 1
                        # where quarter_note_index is the number of "1"
                        # encountered or quarter note beginnings.
                        # print("quarter_note_index: {}".format(quarter_note_index))
                        # But there's a tendency that there are more than four
                        # quarter notes, so suse modulo
                        starting_count = quarter_note_index % 4 + 1
                        for quarter_dict in first_bar_dict_list:
                            temp_dict = {}
                            for key, val in quarter_dict.items():
                                if key == "1":
                                    temp_dict[str(starting_count)] = val
                                    if starting_count == 4:
                                        starting_count = 1 # reset
                                    else:
                                        starting_count += 1
                                else:
                                    temp_dict[key] = val
                            one_two_three_four_dict_list.append(temp_dict)
                                # Well, one_two_three_four_dict_list was empty 
                        got_first_downbeat = True # just once

                    quarter_note_index = 1 # reset
                    # Update beat position
                    one_two_three_four_dict[str(quarter_note_index)] = val
                        # val of the dictionary in one_e_and_a_dict_list
                else: # If not downbeat
                    if got_first_downbeat:
                        # If the key is "1", or start of the quarter note,
                        # but it's not the downbeat
                        if key == "1":
                            # Replace the key with either "2", "3", or "4"
                            one_two_three_four_dict[str(quarter_note_index)] = val 
                        else:
                            one_two_three_four_dict[key] = val
                                # use keys "e", "&", or "a"
                    else: # if not yet found the first downbeat
                        # Isolate the first bar to start at the right beat,
                            # whether the first quarter note starts with
                                # beat 2, 3, of 4
                        if key == "1": # Start of a quarter note
                            # We'll assume that you're indeed the right "1",
                                # or the actual downbeat...
                            first_bar_quarter_note_dict[key] = val
                                # ...but of the isolated first bar
                            quarter_note_index += 1 # The next quarter notes
                                # will be 2, 3, or 4.
                                # But it shouldn't reach four, because "4" should
                                    # be the first down beat by then.
                        else:
                            first_bar_quarter_note_dict[key] = val
                # End check if first downbeat has been found


                audio = y[val[0]:val[1]] # audio index range
                print("q_note_ind: {}".format(q_note_ind))
                print("key: {}".format(key))
                # print("audio: {}".format(audio))
                print("audio: ")
                print(audio)

                if len(audio) == 0:
                    empty_aud.append(q_note_ind)
                    continue
                # print("len(y): {}".format(len(y)))
                # print("y[len(y)]: {}".format(y[len(y)]))
                # audio = numpy.trim_zeros(audio)
                # print("audio: ")
                # print(audio)
                aud_feat = extract_audio_features(y=audio, sr=sr)

                # print("q_note_ind: " + str(q_note_ind))
                # print("sxtnth_note_ind: " + str(sxtnth_note_ind))

                if q_note_ind == 0 and sxtnth_note_ind == 0:
                    # Initialize array
                    in_aud_feat_arr = numpy.array(aud_feat)
                    # print("in_aud_feat_arr initialized...?")
                else: # stack
                    # print("q_note_ind: " + str(q_note_ind))
                    # print("sxtnth_note_ind: " + str(sxtnth_note_ind))
                    in_aud_feat_arr = numpy.vstack([in_aud_feat_arr, aud_feat])

                prev_keys.append(key)
                prev_vals.append(val)
            # End for each 1-e-&-a, or after every quarter note

            # Update every quarter note, because each dictionary is a quarter note
            quarter_note_index += 1 # Increment, 
                # but it will go from 1 to 4 only
                # If downbeat, reset to 1
                    # then add "1" as the key to the 1 e & a 2 e...dict
                # If not downbeat, just increment to get keys "2", "3", and "4"

            if got_first_downbeat:
                # Add the dictionary to one_two_three_four_dict_list
                one_two_three_four_dict_list.append(one_two_three_four_dict)
            else:
                first_bar_dict_list.append(first_bar_quarter_note_dict)

            # if q_note_ind == 20:
            #     print("Hard coded limit of 20 quarter note durations")
            #     break

        # End for each quarter note duration
            # in terms of one dictionary per duration,
            # and the dictionary may have keys "1", "e", "&", "a"

    # End if is_track_downbeat
    else: # don't track downbeat ############################
        
        quarter_note_index = 1 # Just initialize as one 
            #(for the first bar's sake), 
            # but it will go from 1 to 4 only
            # If downbeat, reset to 1
                # then add "1" as the key to the 1 e & a 2 e...dict
            # If not downbeat, just increment to get keys "2", "3", and "4"
        
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
                
                aud_feat = extract_audio_features(y=audio, sr=sr)

                # print("q_note_ind: " + str(q_note_ind))
                # print("sxtnth_note_ind: " + str(sxtnth_note_ind))

                if q_note_ind == 0 and sxtnth_note_ind == 0:
                    # Initialize array
                    in_aud_feat_arr = numpy.array(aud_feat)
                    # print("in_aud_feat_arr initialized...?")
                else: # stack
                    # print("q_note_ind: " + str(q_note_ind))
                    # print("sxtnth_note_ind: " + str(sxtnth_note_ind))
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

    # End Don't track downbeat

    print("\nin_aud_feat_arr.shape: " + str(in_aud_feat_arr.shape))

    print("down_beat_sixteenth_note_indices:")
    print(down_beat_sixteenth_note_indices)

    # print("empty_aud: {}".format(empty_aud))


    # print("in_aud_feat_arr: {}".format(in_aud_feat_arr))
    # print("in_aud_feat_arr.shape: {}".format(in_aud_feat_arr.shape))
    # halt()


    return (in_aud_feat_arr, one_two_three_four_dict_list, tempo, \
        down_beat_sixteenth_note_indices)
    # return in_aud_feat_arr

# End process input()




def slice_input(audio_track_dir, beat_frame_arr):
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
    ##audio_sample_index_arr = numpy.concatenate(audio_sample_index_arr, len(y))
    # Create the arrays of starting indices and ending indices

    # Adjust backward a bit the the sample indices so that when the audio
    # is sliced, aka. backtrack
    audio_sample_index_arr = audio_sample_index_arr - backtrack_offset
        # backtrack_offset = 1100 # optimized manually, global variable

    # Get the onset before the first automatically identifed onset
    beat_len = audio_sample_index_arr[1] - audio_sample_index_arr[0]
        # Measuring the interval each onsets by sampling the first two beats
    first_beat = audio_sample_index_arr[0] - beat_len

    # Push the first beat if valid, meaning not negative
    if first_beat >= 0:
        pass
        # audio_sample_index_arr \
        #     = numpy.append([first_beat], audio_sample_index_arr)
        # print("Added an index in front...")
    else: # append index zero in front
        # audio_sample_index_arr = numpy.append([0], audio_sample_index_arr)
        # print("Added the zero index in front...")
        pass
        

    print("len(audio_sample_index_arr): {}".format(len(audio_sample_index_arr)))
    aud_ind_len = len(audio_sample_index_arr)
    last_beat = audio_sample_index_arr[aud_ind_len-1] + beat_len
    # Do the same thing as finding the first beats,
    # but for the last beats.
    if last_beat >= y[-1]: # 
        audio_sample_index_arr \
            = numpy.append(audio_sample_index_arr, [last_beat])
        print("Added an index at the end...")
    else: # append last index at the end of the audio
        audio_sample_index_arr = numpy.append(audio_sample_index_arr, [y[-1]])
        print("Added the last index at the end...")
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

    # Get the intervals
    start_ind_list = quarter_note_pos_list[0:-1]
        # All indices except the last one
    stop_ind_list = quarter_note_pos_list[1:]
        # All indices except the first one
        # starts  |----------------------|....
        # stops    ....|----------------------|
        # Now, starts[i] to stops[i] represent the ith interval


    # Getting the average length of the quarter notes
    differences = stop_ind_list - start_ind_list
        # Trim the outlying intervals from ends of the audio
    average_diff = numpy.mean(differences)
    average_interval = numpy.around(average_diff) # round off
    print("\naverage_interval: " + str(average_interval))
    sample_diff = quarter_note_pos_list[4] - quarter_note_pos_list[3]
    print("\nsample_diff: " + str(sample_diff))


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

    # For identifying rhythms between each quarter note...rewriting this...
    onset_index = 0
    for i, (start, stop) in enumerate(zip(start_ind_list, stop_ind_list)):
        onset_indices = []
        # quarter_note_pos_list is already backtracked manually
        # full_audio_onset_indices is not backtracked

        # Traverse all the full_audio_onset_indices, the onset indices
        # to the quarter note duration it belongs.
        while full_audio_onset_indices[onset_index] < stop:
            onset_indices.append(full_audio_onset_indices[onset_index])
            onset_index += 1

        print("\ni: {}".format(i))
        print("onset_indices: {}".format(onset_indices))
        beats_dict = identify_beats_per_quarter_note_duration(
                        onsets=onset_indices, ave_int=average_interval,
                        start_ind=start)
            # Example, beats_dict["1"]: [1024:3584]

        # Append the list of all the other one_e_and_a's (beats_dict)
        # with the identified beat ranges within a quarter note to the

        one_e_and_a_dict_list.append(beats_dict) 
            # append because it's just one at a time

        # if i == 20:
        #     print("Hard code limit of 20 for slicing input...")
        #     break

        # here, left with how count sub offsets
    # End for each quarter  note interval


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


    skip_subdivision = True
    if not skip_subdivision:
        # Eighth notes are at the middle of the quarter notes
        ith_positions = quarter_note_pos_list[0:-1] # starts
            # All indices except the last one
        i_plus_1_positions = quarter_note_pos_list[1:] # stops
            # All indices except the first one
        # Getting the average
        sums_list = ith_positions + i_plus_1_positions #
        eight_note_pos_list = sums_list / 2 # average
        print("\neight_note_pos_list:")
        print(eight_note_pos_list)

        
        # The computed quarter note and eighth note positions combined, 
        # because it will be required to get the sixteenth note positions
        eighth_note_beats \
            = numpy.append(quarter_note_pos_list, eight_note_pos_list)
            # combining the the quarter and eights into an array
        eighth_note_beats = numpy.sort(eighth_note_beats)
            # Sixteenth note positions are in between 
            # the quarter and eighth note positons, eighth_note_beats


        # Sixteenth notes are at the middle of the eighth_note_beats
        ith_positions = eighth_note_beats[0:-1] # starts
            # All indices except the last one
        i_plus_1_positions = eighth_note_beats[1:] # stops
            # All indices except the first one
        # Getting the average
        sums_list = ith_positions + i_plus_1_positions #
        sixteenth_note_pos_list = sums_list / 2 # average
        print("\nsixteenth_note_pos_list:")
        print(sixteenth_note_pos_list)


        # Combine the recently computed sixteenth note positions
        # to the previously computed eight note beats, to produce a complete 
        # sixteenth note measure
        sixteenth_note_beats \
            = numpy.append(sixteenth_note_pos_list, eighth_note_beats)
            # combining the the sixteenth note positions with the quarter note
            # positions and the eighth notes position into a single array
        sixteenth_note_beats = numpy.sort(sixteenth_note_beats)
            # The sixteenth note beats capture all the possible drum onsets 
        possible_onset_possitions = sixteenth_note_beats
    # End if not skip_subdivision


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


    create_folder(sliced_input_destination)

    # Saving sliced audio of the input audio track
    for i, (start, stop) in enumerate(zip(starts, stops)):
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



def identify_beats_per_quarter_note_duration(onsets, ave_int, start_ind):
    print("\nIdentifying beats per quarter note duration...")

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


    zero_relative_one_limit = (1/8)*ave_int
    zero_relative_e_limit = (3/8)*ave_int
    zero_relative_and_limit = (5/8)*ave_int
    zero_relative_a_limit = (7/8)*ave_int

    one_limit = zero_relative_one_limit + start_ind
    e_limit = zero_relative_e_limit + start_ind
    and_limit = zero_relative_and_limit + start_ind
    a_limit = zero_relative_a_limit + start_ind

    # For every identified onset
    for onset in onsets:
        print("onset: " + str(onset), end="")
        if onset < one_limit:
            start = int(start_ind + onset)
            end = int(start_ind + one_limit)
            beats_range_dict["1"] = [start, end]
            print(" 1")
        elif onset < e_limit:
            start = int(start_ind + onset)
            end = int(start_ind + e_limit)
            beats_range_dict["e"] = [start, end]
            print(" e")
        elif onset < and_limit:
            start = int(start_ind + onset)
            end = int(start_ind + and_limit)
            beats_range_dict["&"] = [start, end]
            print(" &")
        elif onset < a_limit:
            start = round(start_ind + onset)
            end = int(start_ind + a_limit)
            beats_range_dict["a"] = [start, end]
            print(" a")

        # We added the start index because each quarter note
        # Starts from a different position

        # Ideally, there can only be 4 onsets hear at max,
        # but if there are multiple onsets per 16th note range,
        # it should just be noice so it shouldn't really matter
    # End for every identified onset

    return beats_range_dict
# End def identify_beats_per_quarter_note_duration(onsets):




def find_down_beat(input_dir):

    """ https://stackoverflow.com/questions/57384448/detecting-beat\
    -energy-with-librosa-finding-the-first-beat-of-each-bar """

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