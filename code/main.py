"""
    Author: CJLD
    Year: 2020
"""

# Runtime: 4h:52m

# Standard libary imports
import os
import sys
from midi2audio import FluidSynth



# Local application/library imports
sys.path.insert(0, os.path.abspath("") + "/components") 

from global_vars import * # importing global variables from
from folder_ops import *
from audio_ops import *
from feature_ops import *
from classification_ops import *
from input_ops import *
from midi_ops import *
from lily_ops import *
from gui import *





# def main():
 
#     if not skip_produce_instruments:
#         create_folder(sound_destination)    # setup_sound_destination()

#         if use_default_sound_source:
#            check_if_default_sound_source_is_available() # folder_ops.py

#         produce_rest_samples() # audio_ops.py

#         """ Transfer and mix files from samples folder
#             to the DTT directory for consistent application usage """

#         produce_single_instruments() # single core # old
#             # Save single instruments to ./Produced Drums/one

#         """ Compute the predicted produced sample count for a progress bar """

#         """ Produce double instruments by combining single instruments """
#         produce_double_instruments()
#         produce_triple_instruments()
#         produce_quadruple_samples()

#     # End if produce_instruments
#         # skip

#     if not skip_extract_features:
#         extract_features() # feature_ops.py # procedural programming
        

#     if not skip_loading_features: 
#         # if not skip_load_features_from_file:
#         # Load features from csv to memory for KNN
#         # class_feat_dict = import_features() # feature_ops.py, dictionary
#         # class_feat_dict = import_features("simple") # feature_ops.py, dictionary
#         class_feat_dict = import_features() # feature_ops.py, dictionary

#         # print("class_feat_dict: ")
#         # print(class_feat_dict)

#         # dictionary of string and id
#         class_code_dict = get_class_code(class_feat_dict) # classification_ops.py

#         print("\nclass_code_dict: ")
#         for key, value in class_code_dict.items():
#             print(key + ": " + str(value))
#         # End if not skip_load_features_from_file

#         # class_code_from_csv = csv_to_dictionary("./temp/class_legend.csv")
#         # print("\nclass_code_from_csv: ")
#         # for key, value in class_code_from_csv.items():
#         #     print(key + ": " + str(value))


#         # Create a list of just all the features in a numpy array,
#         # And also create a list of just the corresponding label
#          # for each feature row
#         features, labels = get_features_and_labels(
#             class_feat_dict, class_code_dict) # classification_ops.py

#         print("\nlabels list len: " + str(len(labels)))
#         print("features shape: " + str(features.shape))
#         print("features size: " + str(features.size))
#         # print("features: ")
#         # print(features)


#         """ NumPy - Indexing & Slicing
#             https://www.tutorialspoint.com/numpy/numpy_indexing_and_slicing.htm
#         """

#         # # Slice features to improve KNN Accuracy
#         # features = features[..., :20]
#             # remove the columns beyond the 20th column
#         # print("features shape: " + str(features.shape))

#         test_classify(features, labels)

#         # # sample_dir = "./Roland-SC-88-Ride-Bell.wav"
#         # sample_dir = "./acoustic-kick_G#_major.wav"

#         # print("Extracting...")
#         # feat_arr = extract_audio_features(sample_dir) # feature_ops.py
#         # print("\nfeat_arr.shape: ")
#         # print(feat_arr.shape)

#         # # classify is able to identify array of inputs, 
#         #     # with a little modification
#         # prediction = classify(feat_arr, features, labels)
#         # print("prediction:")
#         # print(prediction)

#         # # classification_ops.py
#         # class_name = get_class_name_using_id(prediction[0], class_code_dict)

#         # print("Predicted instrument:")
#         # print(class_name)
#     # End if skip loading features

#     # input_dir = "./bass_snare_hihat_loop.wav"
#     # input_dir = "./Slow Rock Drum Beat 75 BPM - JimDooley.net.wav"
#     # input_dir = "./slow_rock.wav" 
#     input_dir = "./slow_beat.mp3"


#     in_aud_feat_arr, quarter_timing_dict_list, tempo, \
#         down_beat_sixteenth_note_indices = process_input(input_dir) # input_ops.py
#         # in_aud_feat_arr is a numpy array containing
#             # all features per hit stacked together
#         # quarter_timing_dict_list is a list of dictionaries
#             # which may contain keys 1, e, &, a

#     print("in_aud_feat_arr.shape: ")
#     print(in_aud_feat_arr.shape )

#     print("Classifying input...")

#     # classify is able to identify array of inputs, with a little modification
#     prediction = classify(in_aud_feat_arr, features, labels)
#     print("prediction:")
#     print(prediction)


#     # classification_ops.py
#     class_names = get_class_name_using_id(prediction, class_code_dict)

#     print("class_names: {}".format(class_names))
#     print("quarter_timing_dict_list: {}".format(quarter_timing_dict_list))



#     print("Show prediction: ")
#     class_name_index = 0
#     for quarter_measure, quarter_timing_dict \
#         in enumerate(quarter_timing_dict_list):
#         print("quarter measure: " + str(quarter_measure))
#         for rhythm, value in quarter_timing_dict.items(): # possible keys: "1", "e", "&", "a"
#             # if class_name_index >= len(class_names):
#                 # break
#             # print("rhythm: {}".format(rhythm))
#             print("\t" + rhythm + ": " + class_names[class_name_index])
#             class_name_index += 1
#     # End show prediction
#     # halt()

#     # Combine the class_names list and the quarter_timing_dict_list
#     # as a new list of dictionaries, where the keys ("1", "e", "&", "a")
#     # are mapped to a class_name (eg. bass, snare, tom, etc.)
#     print("Combining class names with rhythm...")
#     rhythym_class_name_dict_list = []

#     indexed_rhythym_class_name_dict_list = []

#     class_name_index = 0
#     for quarter_measure, quarter_timing_dict \
#         in enumerate(quarter_timing_dict_list):
#         rhythym_dict = {}
#         indexed_rhythm_dict = {}
#         for rhythm in quarter_timing_dict: # possible keys: "1", "e", "&", "a"
#             # if class_name_index >= len(class_names):
#                 # break
#             rhythym_dict[rhythm] = class_names[class_name_index]
#             key = str(quarter_measure) + " " + rhythm
#             indexed_rhythm_dict[key] = class_names[class_name_index]

#             class_name_index += 1
#         rhythym_class_name_dict_list.append(rhythym_dict)
#         indexed_rhythym_class_name_dict_list.append(indexed_rhythm_dict)
#     # End show prediction

#     # Make 2 Types of simplication
#     # 1. Basic beat: hihat, bass, snare
#     # 2. More complex than 1
#     # However, this simplified classification should be done in the KNN level.
#     rhythym_class_name_dict_list = simplify_pattern(rhythym_class_name_dict_list)
#         # classification_ops.py

#     filename = os.path.basename(input_dir)
#     filename_wo_ext = os.path.splitext(filename)[0]

#     # convert_to_midi(rhythym_class_name_dict_list, bpm=tempo,
#         # filename=filename_wo_ext) # midi_ops.py

#     convert_to_midi(indexed_rhythym_class_name_dict_list, bpm=tempo,
#         filename=filename_wo_ext) # midi_ops.py


#     print("Combining class names with indexed_rhythm...")
#     rhythym_class_name_dict_list = []
#     class_name_index = 0
#     for quarter_measure, quarter_timing_dict \
#         in enumerate(quarter_timing_dict_list):
#         rhythym_dict = {}
#         for rhythm in quarter_timing_dict:
#             # possible keys: "20 1", "20 e", "20 &", "20 a"
#             indexed_rhythm = str(quarter_measure) + " " + rhythm
#             print("indexed_rhythm: {}".format(indexed_rhythm))
#             # if class_name_index >= len(class_names):
#                 # break
#             rhythym_dict[indexed_rhythm] = class_names[class_name_index]
#             class_name_index += 1
#         rhythym_class_name_dict_list.append(rhythym_dict)
#     # End show prediction

#     print("down_beat_sixteenth_note_indices:")
#     print(down_beat_sixteenth_note_indices)

#     for _ in range(10):
#         mark() # draw a sword

#     convert_to_lilypond(rhythym_class_name_dict_list, bpm=int(round(tempo)),
#         filename=filename_wo_ext,
#         down_beat_positions=down_beat_sixteenth_note_indices
#         ) # lily_ops.py

#     print("\nConcern for lily_ops: what if the downbeat was missed?\n")
#     print("Possible solution: capture the downbeat during the transition " \
#         + "between quarter notes, which is at the part where the " \
#         + "4th count transitions to the 1st count, but the beat won't start " \
#         + "at the first count or the downbeat itself.")


#     print("Exiting main()...")

# # End main()


def print_manual():
    print("How to use:")
    print("\t> py main.py <audio file>")
    print("Options:")
    print("\ttempo <bpm>")
    print("\tblacklist <arg> <arg> <arg>...")
    print("\twhitelist <arg> <arg> <arg>...")
    print("\tremove uncommon")
    print("\tremove <arg_combo>,<arg_combo> <arg_combo>,<arg_combo>...")
    print("\tremove <commma>,<no space> <classes>,<are space>,<separated>...")
    print("\ttest <your label>")
    print("\tclasses <special grouping whilelist shortcut>")
    print("Option arguments:")
    print("\tbass, snare, stick, ride, tom, floor,\n\thihat, hihat-open, " 
        + "crash, ride, bell")
    # print("Exit: quit, exit")



if __name__ == '__main__':
    
    # print("\nRunning program...\n")

    # # filePath = select_file() # ./components/gui.py
    # # print("Selected file: {}" .format(filePath))


    # """ GUI Input Selection Start """
    # window = Tk()
    # window.geometry("700x400")
    # window.title("Drum Track Transcriptor")

    # mainFrame = MainFrame(window)
    # print("Hello there!")

    # window.mainloop()

    # print("Program ended...")

    # print("\nExiting program...\n")


    # input("Press Enter to continue...")
    # sys.exit()

    # """ GUI Input Selection End """


    # # input("Press Enter to continue...")
    # # halt()
    # # main()
    # # ring()


    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            # Check input file type.

            # Get the file extension.
            input_filename = os.path.basename(sys.argv[1]) # Eg. "solo.wav"
            input_filename_split = os.path.splitext(input_filename)
            # print("input_filename_split: {}".format(input_filename_split))
            # halt()

            instruments = "bass snare stick ride tom floor hihat hihat-open " \
                                    + "crash ride bell"
            instruments = instruments.split()
            print("instruments: {}".format(instruments))

            option = ""
            blacklist = []
            whitelist = []
            remove = []
            tempo = None
            classes = []
            test = None

            if len(sys.argv) > 2:
                for i in range(2,len(sys.argv)):
                    if sys.argv[i] == "tempo" \
                        or sys.argv[i] == "blacklist" \
                        or sys.argv[i] == "whitelist" \
                        or sys.argv[i] == "remove" \
                        or sys.argv[i] == "classes" \
                        or sys.argv[i] == "test":
                        option = sys.argv[i]
                        if sys.argv[i] == "test":
                            test = []
                    elif option == "":
                        print("Invalid argument for option {}".format(option))
                    elif option == "tempo":
                        if sys.argv[i].isnumeric():
                            tempo = int(sys.argv[i])
                        else:
                            print("Tempo must be numeric")
                    elif option == "blacklist":
                        if sys.argv[i] in instruments:
                            blacklist.append(sys.argv[i])
                        else:
                            print("Invalid blacklist keyword")
                    elif option == "whitelist":
                        if sys.argv[i] in instruments:
                            whitelist.append(sys.argv[i])
                        else:
                            print("Invalid whitelist keyword")
                    elif option == "remove":
                        remove.append(sys.argv[i])
                    elif option == "classes":
                        classes.append(sys.argv[i])
                    elif option == "test":
                        test.append(sys.argv[i])

                    # if sys.argv[i]

            print("tempo: {}".format(tempo))
            print("blacklist: {}".format(blacklist))
            print("whitelist: {}".format(whitelist))
            print("remove: {}".format(remove))
            print("classes: {}".format(classes))
            print("test: {}".format(test))
            
            # Checking file extension...
            if input_filename_split[1] == ".mid"  \
                or input_filename_split[1] == ".midi":
                # or input_filename_split[1] == ".MID" or : 
                # or input_filename_split[1] == ".MIDI" or : 
                
                print("\nInvalid file input...\n")
                
                # output_audio_filename = input_filename_split[0] \
                #                             + "_audio_from_midi" + ".wav"

                # # sound_font_file = os.path.abspath("./File/Yamaha_RX7_Drums.sf2")
                # sound_font_file = "File/Yamaha_RX7_Drums.sf2"

                # # fs = FluidSynth("./File/Yamaha_RX7_Drums.sf2")
                # # fluidSynth = FluidSynth(sound_font=sound_font_file)
                # fluidSynth = FluidSynth()

                # # print("input_filename: {}".format(input_filename))
                # # print("output_audio_filename: {}".format(output_audio_filename))

                # # sf = os.path.abspath("./File/Yamaha_RX7_Drums.sf2")
                # # sf = os.path.abspath("./File/Yamaha_RX7_Drums.sf2")

                # input_file = os.path.abspath(input_filename)
                # # output_file = os.getcwd() + "\\" + output_audio_filename
                # output_file = output_audio_filename

                # print("sound_font_file: {}".format(sound_font_file))
                # print("input_file: {}".format(input_file))
                # print("output_file: {}".format(output_file))

                # # fluidSynth.midi_to_audio(input_file, output_file)
                # # fluidSynth.play_midi(input_filename)
                # fluidSynth.play_midi(input_file)


                # print("\nFinished converting midi to wav.")

            elif input_filename_split[1] == ".mp3" \
                or input_filename_split[1] == ".wav":
                
                if len(remove) == 0:
                    remove = None
                if len(blacklist) == 0:
                    blacklist = None
                if len(whitelist) == 0:
                    whitelist = None
                if len(classes) == 0:
                    classes = None
                # if len(test) == 0:
                    # test = None
                    pass

                input_dir = sys.argv[1]
                main(input_dir = input_dir, tempo=tempo, whitelist=whitelist,
                    blacklist=blacklist, remove=remove, classes=classes,
                    test=test)

            else:
                print("\nInvalid file input...\n")

        else:
            print("Invalid argument")
            print("Run main.py with no parameters for help.")
            sys.exit()

    else:
        # input_dir = "./bass_snare_hihat_loop.wav"
        # input_dir = "./Slow Rock Drum Beat 75 BPM - JimDooley.net.wav"
        # input_dir = "./slow_rock.wav" 
        # input_dir = "./slow_beat.mp3"
        # main(input_dir = input_dir)
        print_manual()
