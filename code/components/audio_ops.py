""" Select sound source locations """

import os
import sys

import multiprocessing

from pydub import AudioSegment # imports file audio

from global_vars import *
from global_ops import *
from folder_ops import *

""" Copies the sound files from the source folder
    inside the DTT directory
    # May convert to mono
    # May adjust volume
"""
def produce_single_instruments():
    print("\nFetching sounds from the soure to the DTT")

    single_class_dir = sound_destination + "/" + "single"

    create_folder(single_class_dir)

    print("For each sound folders...")
    for inst_type in instruments:
        # Eg. inst_type == "bass"

        inst_dir_src = sound_source + "/" + inst_type
        # Eg. ./Sampled Drums/bass

        create_folder(single_class_dir + "/" + inst_type)

        inst_index = 0

        for inst_file in os.listdir(inst_dir_src):
            # Eg. bass

            inst_path = inst_dir_src + "/" + inst_file
            # Eg. Eg. ./Sampled Drums/bass/Yamaha-dry-kick.wav

            print("inst_file: " + inst_file)
            inst_audio = AudioSegment.from_file(inst_path, "wav")

            if use_mono:
                print("Converting to mono...")
                mono_audio = inst_audio.set_channels(1)  
                inst_audio = mono_audio  

            if mix_volumes:
                print("Adjusting volume...")
                inst_adjusted_audio = match_target_amplitude(
                    inst_audio, target_decibel[inst_type])
                inst_audio = inst_adjusted_audio

            print("Renaming using index...")
            inst_new_name = str(inst_index).zfill(3) + ".wav" # leading zero
            
            inst_renamed_path = single_class_dir \
                + "/" + inst_type + "/" + inst_new_name
            print("Saving as " + inst_renamed_path)
            inst_audio.export(inst_renamed_path, format="wav")

            # Update
            inst_index += 1
            global_variables[inst_type + " count"] = inst_index
            instrument_count[inst_type] = inst_index
                # Save the total samples per instrument type

        # End for each inst_file in inst_type

        # After producing the instruments, produce about 600 more of each
        # to even out the sample size

        sing_insts = os.listdir(inst_dir_src)
        inst_count = len(sing_insts)
        more_count = abs(600 - inst_count)
        sing_inst_ind = 0

        for ind in range(more_count):

            inst_path = inst_dir_src + "/" + sing_insts[sing_inst_ind]
            # Eg. Eg. ./Sampled Drums/bass/Yamaha-dry-kick.wav
            sing_inst_ind += 1 # increment
            if sing_inst_ind >= inst_count:
                sing_inst_ind = 0 # reset

            print("inst_file: " + inst_file)
            inst_audio = AudioSegment.from_file(inst_path, "wav")

            if use_mono:
                print("Converting to mono...")
                mono_audio = inst_audio.set_channels(1)  
                inst_audio = mono_audio  

            if mix_volumes:
                print("Adjusting volume...")
                inst_adjusted_audio = match_target_amplitude(
                    inst_audio, target_decibel[inst_type])
                inst_audio = inst_adjusted_audio

            print("Renaming using index...")
            inst_new_name = str(ind + sing_inst_ind).zfill(3) + ".wav" # leading zero
            
            inst_renamed_path = single_class_dir \
                + "/" + inst_type + "/" + inst_new_name
            print("Saving as " + inst_renamed_path)
            inst_audio.export(inst_renamed_path, format="wav")

            # Update
            inst_index += 1
            global_variables[inst_type + " count"] = inst_index
            instrument_count[inst_type] = inst_index
                # Save the total samples per instrument type



    # End for each inst_type
# End produce_single_instruments()


"""
    # Normalize all the sound samples
    https://stackoverflow.com/questions
        /42492246/how-to-normalize-the-volume-of-an-audio-file
            -in-python-any-packages-currently-a
"""
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)
# code for main:
# sound = AudioSegment.from_file("yourAudio.m4a", "m4a")
# normalized_sound = match_target_amplitude(sound, -20.0)
# normalized_sound.export("nomrmalizedAudio.m4a", format="mp4")



def count_combined_two_sounds():

    """ Count how many sound files
        will be produced after overlaying
        two instruments on each other 
    """

    print("\nCounting combined two sounds...")

    # Use len(instruments) to get
    # the official number of drumset instrument pieces
    for inst_1_index in range(0, len(instruments)):
        # Use indexing to get the right combination of instruments

        inst_1_type = list(instrument_count)[inst_1_index]
            # get key of dictionary by indexing

        for inst_2_index in range(inst_1_index + 1, len(instruments)):
            # Use the index + 1 to exclude inst_1_type itself
            inst_2_type = list(instrument_count)[inst_2_index]
                # get key of dictionary by indexing

            # Getting the instrument 1 and 2 count from the global dictionary
            inst_1_count = instrument_count[inst_1_type]
            inst_2_count = instrument_count[inst_2_type]

            # Getting the instrument type and count by multiplication
            inst_type = inst_1_type + " " + inst_2_type
            inst_count = inst_1_count * inst_2_count

            # Saving the combined instrument count to the global dictionary
            # Using the instrument type as the key
            # And its count as the value
            instrument_count[inst_type] = inst_count

        # End for each instrument 2 of the combination, of the combined sound
    # End for each instrument 2 of the combination, of the combined sound

    print("Instrument count:")
    print(instrument_count)

    # End for each inst_type
# End count_combined_two_sounds()


def combine_sounds(): # unused, replaced by the multiprocessing version
    """ Overlays/Combines Samples from ./Produced Drums
        with other instruments """
    print("\nCombining sounds...")
    count_combined_two_sounds()
    combine_two_sounds()
    # Split the combination work to two cores
    # core_1_starting_index = 0
    # core_1_stopping_index = len(instruments)/3 # bass to bell
    # core_2_starting_index = core_1_stopping_index
        # start where the core 1 left
    # core_2_stopping_index = len(instruments) # bass to bell
    # combine_two_sounds_multiprocessing()
    # combine_three_sounds()
# End combine_sounds()


def overlay_sounds(audio1, audio2):

    """ Overlay two sounds
        Overlay the short segment on top
          of the long one to preserve length
    """

    # If audio_list, sort by ascending length

    # Compare length
    if audio1.duration_seconds > audio2.duration_seconds:
        combined = audio1.overlay(audio2)
    else:
        combined = audio2.overlay(audio1)

    return combined

# End overlay_sounds()




""" Overlays/Combines Two Instrument Types form Produced Drum Samples """

def produce_double_instruments():
    print("\nCombining two sounds...")

    double_class_dir = sound_destination + "/" + "double"
    create_folder(double_class_dir)

    single_class_dir = sound_destination + "/" + "single"

    print("For each sound folders")
    for inst_1_index in range(0, len(instruments)):
        # Use index to differentiate inst_1 from inst_2
        # inst_type eg.: bass

        inst_1_type = instruments[inst_1_index]
        inst_1_dir = single_class_dir + "/" + inst_1_type
                # Eg. ./Sampled Drums/single/bass

        if blacklisted(inst_1_type):
            continue

        for inst_2_index in range(inst_1_index + 1, len(instruments)):
            # Use index to differentiate inst_1 from inst_2
            # inst_type eg.: snare

            """ Combine the instances of the instrument types """

            inst_2_type = instruments[inst_2_index]
            print("Combining for type '" \
                + inst_1_type + " " + inst_2_type + "'")

            if blacklisted(inst_1_type + " " + inst_2_type):
                # Must be separated by space
                continue
                    # Skip combining blacklisted combination

            inst_2_dir = single_class_dir + "/" + inst_2_type
                # Eg. ./Sampled Drums/single/snare

            inst_index = 0
            inst_type = inst_1_type + " " + inst_2_type

            print("\nCreating a new folder for inst_type '" + inst_type + "'")
            inst_dir = double_class_dir + "/" + inst_type
            create_folder(inst_dir)

            preselected_inst_1_index_list \
                = select_random_intrument_indices_list(inst_1_dir)
            inst_1_file_list = os.listdir(inst_1_dir)
                # list of all the sound files in inst_1_dir

            for inst_1_index in preselected_inst_1_index_list:
                # For every preselected indices of inst_1_type
                inst_1_file = inst_1_file_list[inst_1_index]

                # Eg. 000.wav
                inst_1_path = inst_1_dir + "/" + inst_1_file
                    # inst_1_path eg. ./Sampled Drums/single/bass/000.wav
                inst_1_audio = AudioSegment.from_file(inst_1_path, "wav")


                preselected_inst_2_index_list \
                    = select_random_intrument_indices_list(inst_2_dir)
                inst_2_file_list = os.listdir(inst_2_dir)
                    # list of all the sound files in inst_1_dir

                # Get each inst_2_audio to be combined
                for inst_2_index in preselected_inst_2_index_list:
                    # For every preselected indices of inst_2_type
                    inst_2_file = inst_2_file_list[inst_2_index]

                    
                    inst_2_path = inst_2_dir + "/" + inst_2_file
                    inst_2_audio = AudioSegment.from_file(inst_2_path, "wav")

                    inst_audio = overlay_sounds(inst_1_audio, inst_2_audio)

                    print("Instrument: " + inst_type)
                    print("\tindex " + str(inst_index))
                    inst_new_name = str(inst_index).zfill(3) + ".wav"
                        # leading zero
                    
                    inst_renamed_path = double_class_dir \
                        + "/" + inst_type + "/" + inst_new_name
                    print("Saving as " + inst_renamed_path)
                    inst_audio.export(inst_renamed_path, format="wav")

                    print("Combined " \
                        + inst_1_type + ": " + inst_1_file + ", " \
                        + inst_2_type + ": " + inst_2_file)

                    # Update
                    inst_index += 1

                    if inst_index >= maximum_limit:
                        print("'" + inst_type + \
                            "' samples reached maximum_limit: " \
                            + maximum_limit)
                        break

                # End for each inst_2_file combined to inst_1_file
            # End for each first inst_file

            
        
        # End for each second inst_2_type
    # End for each inst_1_type
# End produce_double_instruments()



""" Overlays/Combines Bass with Produced Two Instrument Types """

def produce_triple_instruments():

    print("\nCombining three sounds multiprocessing...")


    bass_dir = sound_destination + "/" + "single/bass"
    double_class_dir = sound_destination + "/" + "double"
    triple_class_dir = sound_destination + "/" + "triple"
    create_folder(triple_class_dir)

    double_instruments = os.listdir(double_class_dir)

    # Another method to remove types with bass instruments
    for single_inst_type in instruments:
        single_inst_type_with_bass = "bass " + str(single_inst_type)
        # print(single_inst_type_with_bass)
        if single_inst_type_with_bass in double_instruments:
            # print("Extists: " + single_inst_type_with_bass)
            double_instruments.remove(single_inst_type_with_bass)


    # print("double_instruments:")
    # print(double_instruments)


    print("For each two instrument sound...")

    for two_inst_index in range(len(double_instruments)): 
        # Revert from automatic float, back to int
        # Use index to differentiate inst_1 from inst_2
        # inst_type eg.: snare tom

        print("two_inst_index: ", end = '')
        print(two_inst_index)

        two_inst_type = double_instruments[two_inst_index]
            # Eg. snare tom
        two_inst_dir = double_class_dir + "/" + two_inst_type
                # Eg. ./Sampled Drums/double/snare tom

        inst_index = 0
        inst_type = "bass" + " " + two_inst_type # it's always adding bass
            # Eg. bass snare tom

        print("\nCreating a new folder for three_inst_type '" + inst_type + "'")
        three_inst_dir = triple_class_dir + "/" + inst_type
        create_folder(three_inst_dir)
            # Eg. ./Sampled Drums/triple/bass snare tom

        preselected_two_inst_index_list \
            = select_random_intrument_indices_list(two_inst_dir)
            # The preselected list will contain indices as many as
            # the set global variable limit_base

        two_inst_file_list = os.listdir(two_inst_dir)
            # Get into a list all the sound names located in two_inst_dir
            # Eg. ./Sampled Drums/double/snare tom/000.wav, among others
            
        """ Sound file list, two_inst_file_list
        (or ['000.wav', '001.wav', ...]), will be accessed using 
        the list of random indices, preselected_two_inst_index_list 
        (or [4, 12, 33, ..., 175, 543])
        """

        # print("two_inst_file_list:")
        # print(two_inst_file_list)

        print("preselected_two_inst_index_list:", end="\n")
        print(preselected_two_inst_index_list)


        for two_inst_index in preselected_two_inst_index_list:
            # For every preselected index of preselected_two_inst_index_list
            
            # This is the file name equivalent of two_inst_index
            two_inst_file = two_inst_file_list[two_inst_index] # Eg. 000.wav
            two_inst_path = two_inst_dir + "/" + two_inst_file
                # two_inst_path eg. ./Sampled Drums/double/snare tom/000.wav
            
            # This is the audio data equivalent
            two_inst_audio = AudioSegment.from_file(two_inst_path, "wav")

            """ Each individual two_inst_audio has been setup at this point.
            Now, we must do the same to each drum audio,
            and then combine them afterwards
            """

            preselected_bass_index_list \
                = select_random_intrument_indices_list(bass_dir)
                    # Bass is the type that we only need.
                    # Because it's like this:
                    #   bass + snare + tom (or bass + two_inst_type)

            bass_file_list = os.listdir(bass_dir)
                # list of all the sound filenames in bass_dir

            """ Get each bass_audio and two_inst_audio combined """

            for bass_index in preselected_bass_index_list:
                # For every preselected index of bass
                bass_file = bass_file_list[bass_index]

                # Get bass_audio from the bass_path
                bass_path = bass_dir + "/" + bass_file
                bass_audio = AudioSegment.from_file(bass_path, "wav")

                three_inst_audio = overlay_sounds(bass_audio, two_inst_audio)
                    # The order of overlay_sounds() parameters do not matter,
                    # because overlay_sounds() was written to overlay the
                    # the shorter audio on top of the longer one to preserve
                    # the length of both audio

                print("Instrument: " + inst_type) # Eg. "bass snare tom"
                print("\tindex " + str(inst_index)) # to count the produced
                inst_new_name = str(inst_index).zfill(3) + ".wav"
                    # leading zeros, eg 000.wav
                
                inst_renamed_path = triple_class_dir \
                    + "/" + inst_type + "/" + inst_new_name
                print("Saving as " + inst_renamed_path)
                three_inst_audio.export(inst_renamed_path, format="wav")

                print("Combined " \
                    + "bass" + ": " + bass_file + ", " \
                    + two_inst_type + ": " + two_inst_file)

                # Update
                inst_index += 1

                if inst_index >= maximum_limit:
                    print("'" + inst_type + \
                        "' samples reached maximum_limit: " \
                        + maximum_limit)
                    break

            # End for each bass_file combined with two_inst_file
        # End for each two_inst_file

    # End for each two_inst_type, Eg. ./Sampled Drums/snare tom/000.wav, etc.
# End combine_three_sounds_multiprocessing()



def produce_rest_samples():
    print("\nProducing rest samples...")

    inst_type = "rest"
    inst_dest = sound_destination + "/" + inst_type

    create_folder(inst_dest)

    # Fetch all rest into DTT
    rest_dir = sound_source + "/rest"

    inst_index = 0
    total = len(os.listdir(rest_dir))

    for vinyl_filename in os.listdir(rest_dir):
        inst_new_name = str(inst_index).zfill(3) + ".wav" # leading zero
        

        print(str(inst_index+1) + "/" + str(total) + ": ", end="")

        inst_renamed_path = inst_dest \
            + "" + "" + "/" + inst_new_name
        print("Saving as " + inst_renamed_path)

        vinyl_path = rest_dir + "/" + vinyl_filename
        vinyl_audio = AudioSegment.from_file(vinyl_path, "wav")
        
        print("Adjusting volume...")
        vinyl_adjusted_audio = match_target_amplitude(
            vinyl_audio, target_decibel[inst_type])
        vinyl_audio = vinyl_adjusted_audio

        vinyl_audio.export(inst_renamed_path, format="wav")

        inst_index += 1

    print("\nSilence")

    # Duplicate silent.wav
    rest_dir = sound_source + "/rest"

    # silence_name = os.listdir(rest_dir)[0] # just one element
    silence_names = os.listdir(rest_dir) # each element
    silence_len = len(silence_names)
    silence_ind = 0

    limit = abs(600 - total)

    for i in range(limit):

        inst_new_name = str(inst_index).zfill(3) + ".wav" # leading zero

        print(str(inst_index+1) + "/" + str(total + limit) + ": ", end="")

        inst_renamed_path = inst_dest \
            + "" + "" + "/" + inst_new_name
        print("Saving as " + inst_renamed_path)

        rest_path = rest_dir + "/" + silence_names[silence_ind]
        rest_audio = AudioSegment.from_file(rest_path, "wav")

        print("Adjusting volume...")
        rest_adjusted_audio = match_target_amplitude(
            rest_audio, target_decibel[inst_type])
        rest_audio = rest_adjusted_audio

        rest_audio.export(inst_renamed_path, format="wav")

        inst_index += 1

        silence_ind += 1
        if silence_ind >= silence_len:
            silence_ind = 0

# End produce_rest_samples()


def produce_quadruple_samples():

    print("\nCombining four sounds multiprocessing...")

    hihat_dir = sound_destination + "/" + "single/hihat"
    hihat_open_dir = sound_destination + "/" + "single/hihat-open"
    double_class_dir = sound_destination + "/" + "double"
    triple_class_dir = sound_destination + "/" + "triple"
    quadruple_class_dir = sound_destination + "/" + "quadruple"
    
    triple_instruments_list = os.listdir(triple_class_dir)

    # Remove hihat/open triple insturment
    # To remove redundancy, because quadruple instrument will just be
    # added a foot hihat/open
    for triple_inst_type in (os.listdir(triple_class_dir)):
        
        inst_type_combination_list = triple_inst_type.split()
            # Eg. bass floor tom # print(inst_type_combination_list)

        if "hihat" in inst_type_combination_list: 
            triple_instruments_list.remove(triple_inst_type) # Remove
        elif "hihat-open" in inst_type_combination_list: 
            triple_instruments_list.remove(triple_inst_type) # Remove
        
    # End for each triple instrument, checked if it has a hihat/open

    """ At this point triple_instruments_list have been prepared,
    removed hihats
    """

    # print("triple_instruments_list:")
    # print(triple_instruments_list)

    create_folder(quadruple_class_dir)


    """ quadruple/...hihat """

    skip_quadruple_hihat = False

    if not skip_quadruple_hihat:
        print("For each three instrument sound...")
        for three_inst_index in range(len(triple_instruments_list)): 
            # Revert from automatic float, back to int
            # Use index to differentiate inst_1 from inst_2
            # inst_type eg.: snare tom

            print("three_inst_index: ", end = '')
            print(three_inst_index)

            three_inst_type = triple_instruments_list[three_inst_index]
                # Eg. bass snare tom
            three_inst_dir = triple_class_dir + "/" + three_inst_type
                    # Eg. ./Sampled Drums/triple/bass snare tom

            inst_index = 0
            inst_type = three_inst_type + " " + "hihat" 
                # it's always adding hihat
                # Eg. bass snare tom hihat

            print("\nCreating a new folder for four_inst_type '" \
                + inst_type + "'")
            four_inst_dir = quadruple_class_dir + "/" + inst_type
            create_folder(four_inst_dir)
                # Eg. ./Sampled Drums/quadruple/bass snare tom hihat

            preselected_three_inst_index_list \
                = select_random_intrument_indices_list(three_inst_dir)
                # The preselected list will contain indices as many as
                # the set global variable limit_base

            three_inst_file_list = os.listdir(three_inst_dir)
                # Get into a list all the sound names located in two_inst_dir
                # Eg. ./Sampled Drums/triple/bass snare tom/000.wav, 
                # among others
                
            # print("three_inst_file_list:")
            # print(three_inst_file_list)

            """ Sound file list, three_inst_file_list
            (or ['000.wav', '001.wav', ...]), will be accessed using 
            the list of random indices, preselected_three_inst_index_list 
            (or [4, 12, 33, ..., 175, 543])
            """

            print("preselected_three_inst_index_list:", end="\n")
            print(preselected_three_inst_index_list)

            for three_inst_index in preselected_three_inst_index_list:
                # For every preselected index of 
                # preselected_three_inst_index_list
                
                # This is the file name equivalent of two_inst_index
                three_inst_file = three_inst_file_list[three_inst_index]
                    # Eg. 000.wav
                three_inst_path = three_inst_dir + "/" + three_inst_file
                    # three_inst_path
                    # eg. ./Sampled Drums/triple/bass snare tom/000.wav
                
                # This is the audio data equivalent
                three_inst_audio \
                    = AudioSegment.from_file(three_inst_path, "wav")

                """ Each individual three_inst_audio has 
                been setup at this point.
                Now, we must do the same to each drum audio,
                and then combine them afterwards
                """

                preselected_hihat_index_list \
                    = select_random_intrument_indices_list(hihat_dir)
                        # hihiat is the type that we only need.
                        # Because it's like this:
                        # bass + snare + tom + hihiat 
                        # (or three_inst_type + hihiat)

                hihat_file_list = os.listdir(hihat_dir)
                    # list of all the sound filenames in hihat_dir

                """ Get each hihat_audio and three_inst_audio combined """

                for hihat_index in preselected_hihat_index_list:
                    # For every preselected index of hihat
                    hihat_file = hihat_file_list[hihat_index]

                    # Get hihat_audio from the hihat_path
                    hihat_path = hihat_dir + "/" + hihat_file
                    hihat_audio = AudioSegment.from_file(hihat_path, "wav")

                    four_inst_audio \
                        = overlay_sounds(hihat_audio, three_inst_audio)
                        # The order of overlay_sounds() parameters 
                        # do not matter,
                        # because overlay_sounds() was written to overlay the
                        # the shorter audio on top of the longer one
                        # to preserve the length of both audio

                    print("Instrument: " + inst_type) 
                        # Eg. "bass snare tom hihat"
                    print("\tindex " + str(inst_index)) # to count the produced
                    inst_new_name = str(inst_index).zfill(3) + ".wav"
                        # leading zeros, eg 000.wav
                    
                    inst_renamed_path = quadruple_class_dir \
                        + "/" + inst_type + "/" + inst_new_name
                    print("Saving as " + inst_renamed_path)
                    four_inst_audio.export(inst_renamed_path, format="wav")

                    print("Combined " \
                        + three_inst_type + ": " + three_inst_file + ", " \
                        + "hihat" + ": " + hihat_file)

                    # Update
                    inst_index += 1

                    if inst_index >= maximum_limit:
                        print("'" + inst_type + \
                            "' samples reached maximum_limit: " \
                            + maximum_limit)
                        break


                # End for each hihat_file combined with three_inst_file
            # End for each three_inst_file

        # End for each three_inst_type,
        # Eg. ./Sampled Drums/bass snare tom/000.wav, etc.

    # End skip if

    """ quadruple/...hihat-open """

    print("For each three instrument sound...")
    for three_inst_index in range(len(triple_instruments_list)): 
        # Revert from automatic float, back to int
        # Use index to differentiate inst_1 from inst_2
        # inst_type eg.: snare tom

        print("three_inst_index: ", end = '')
        print(three_inst_index)

        three_inst_type = triple_instruments_list[three_inst_index]
            # Eg. bass snare tom
        three_inst_dir = triple_class_dir + "/" + three_inst_type
                # Eg. ./Sampled Drums/triple/bass snare tom

        inst_index = 0
        inst_type = three_inst_type + " " + "hihat-open"
            # it's always adding hihat-open
            # Eg. bass snare tom hihat-open

        print("\nCreating a new folder for four_inst_type '" + inst_type + "'")
        four_inst_dir = quadruple_class_dir + "/" + inst_type
        create_folder(four_inst_dir)
            # Eg. ./Sampled Drums/quadruple/bass snare tom hihat-open

        preselected_three_inst_index_list \
            = select_random_intrument_indices_list(three_inst_dir)
            # The preselected list will contain indices as many as
            # the set global variable limit_base

        three_inst_file_list = os.listdir(three_inst_dir)
            # Get into a list all the sound names located in two_inst_dir
            # Eg. ./Sampled Drums/triple/bass snare tom/000.wav, among others
            
        # print("three_inst_file_list:")
        # print(three_inst_file_list)

        """ Sound file list, three_inst_file_list
        (or ['000.wav', '001.wav', ...]), will be accessed using 
        the list of random indices, preselected_three_inst_index_list 
        (or [4, 12, 33, ..., 175, 543])
        """

        print("preselected_three_inst_index_list:", end="\n")
        print(preselected_three_inst_index_list)

        for three_inst_index in preselected_three_inst_index_list:
            # For every preselected index of preselected_three_inst_index_list
            
            # This is the file name equivalent of two_inst_index
            three_inst_file = three_inst_file_list[three_inst_index]
                # Eg. 000.wav
            three_inst_path = three_inst_dir + "/" + three_inst_file
                # three_inst_path
                # eg. ./Sampled Drums/triple/bass snare tom/000.wav
            
            # This is the audio data equivalent
            three_inst_audio = AudioSegment.from_file(three_inst_path, "wav")

            """ Each individual three_inst_audio has been setup at this point.
            Now, we must do the same to each drum audio,
            and then combine them afterwards
            """

            preselected_hihat_open_index_list \
                = select_random_intrument_indices_list(hihat_open_dir)
                    # hihiat is the type that we only need.
                    # Because it's like this:
                    # bass + snare + tom + hihiat (or three_inst_type + hihiat)

            hihat_open_file_list = os.listdir(hihat_open_dir)
                # list of all the sound filenames in hihat_open_dir

            """ Get each hihat_open_audio and three_inst_audio combined """

            for hihat_open_index in preselected_hihat_open_index_list:
                # For every preselected index of hihat_open
                hihat_open_file = hihat_open_file_list[hihat_open_index]

                # Get hihat_open_audio from the hihat_path
                hihat_open_path = hihat_open_dir + "/" + hihat_open_file
                hihat_open_audio \
                    = AudioSegment.from_file(hihat_open_path, "wav")

                four_inst_audio \
                    = overlay_sounds(hihat_open_audio, three_inst_audio)
                    # The order of overlay_sounds() parameters do not matter,
                    # because overlay_sounds() was written to overlay the
                    # the shorter audio on top of the longer one to preserve
                    # the length of both audio

                print("Instrument: " + inst_type) 
                    # Eg. "bass snare tom hihat_open"
                print("\tindex " + str(inst_index)) # to count the produced
                inst_new_name = str(inst_index).zfill(3) + ".wav"
                    # leading zeros, eg 000.wav
                
                inst_renamed_path = quadruple_class_dir \
                    + "/" + inst_type + "/" + inst_new_name
                print("Saving as " + inst_renamed_path)
                four_inst_audio.export(inst_renamed_path, format="wav")

                print("Combined " \
                    + three_inst_type + ": " + three_inst_file + ", " \
                    + "hihat-open" + ": " + hihat_open_file)

                # Update
                inst_index += 1

                if inst_index >= maximum_limit:
                    print("'" + inst_type + \
                        "' samples reached maximum_limit: " \
                        + maximum_limit)
                    break


            # End for each hihat_open_file combined with three_inst_file
        # End for each three_inst_file

    # End for each three_inst_type,
   # Eg. ./Sampled Drums/bass snare tom/000.wav, etc.

# End produce_quadruple_samples()


def bal_audio(inst_path, vol_ref_inst):
    # inst_path = inst_dir_src + "/" + inst_file
    # Eg. Eg. ./Sampled Drums/bass/Yamaha-dry-kick.wav

    # print("inst_file: " + inst_file)
    inst_audio = AudioSegment.from_file(inst_path, "wav")

    if use_mono:
        print("Converting to mono...")
        mono_audio = inst_audio.set_channels(1)  
        inst_audio = mono_audio  

    if mix_volumes:
        print("Adjusting volume...")
        inst_adjusted_audio = match_target_amplitude(
            inst_audio, target_decibel[vol_ref_inst])
        inst_audio = inst_adjusted_audio

    inst_audio.export(inst_path, format="wav")