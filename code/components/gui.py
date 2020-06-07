"""
    GUI
"""

import sys # First import sys
import os

# from os import listdir, path


from global_vars import * # importing global variables from
from folder_ops import *
from audio_ops import *
from feature_ops import *
from classification_ops import *
from input_ops import *
from midi_ops import *
from lily_ops import *


# import tkinter as tk
# from tkinter import Frame, Label, Button, Entry, Checkbutton, IntVar
# from tkinter import END
from tkinter import filedialog
# from playsound import playsound
from tkinter import *

# Second append the folder path
sys.path.insert(0, os.path.abspath('/components')) # Windows

# Third Make a blank file called __ init __.py in your 
# subdirectory (this tells Python it is a module)

# Fourth import the module inside the folder
# from sound_ops import SoundOverlayer



class MainFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        self.input_field = FileInput(self)        
        self.input_field.grid(row=0, column=0)

        self.transcribe_button = Button(self, text="Transcribe",
            command=self.transcribe)
        self.transcribe_button.grid(row=1)


        self.newline_label = Label(self, text="")
        self.newline_label.grid(row=3)

        # # skip_produce_instruments
        # skip_produce_instruments = BooleanVar(value=True) # Initialize checked.
        # print("skip_produce_instruments: {}".format(skip_produce_instruments))
        # self.checkbutton1 = Checkbutton(self, text="skip_produce_instruments",
        #     variable=skip_produce_instruments,
        #     onvalue=True, offvalue=False)
        # self.checkbutton1.grid(row=4, sticky=W)
        # self.checkbutton1.toggle()

        # # skip_extract_features
        # skip_extract_features = BooleanVar(value=True)
        # self.checkbutton2 = Checkbutton(self, text="skip_extract_features",
        #     variable=skip_extract_features,
        #     onvalue=True, offvalue=False)
        # self.checkbutton2.grid(row=5, sticky=W)


        # skip_loading_features


        self.pack()


    def transcribe(self):
        # Verify if correct input
        text_input = self.input_field.get_file()
        
        if text_input.isspace():
            print("No input!")
        elif not os.path.isfile(text_input):
            print("File does not exist!")
        else:
            file_ext = os.path.splitext(text_input)[1]
            print("file_ext: {}".format(file_ext))
            if file_ext != ".mp3" and file_ext != ".wav":
                print("Wrong file type, it must be mp3 or wav!")
            else:
                print("Ok")
                print("file_ext: {}".format(file_ext))
                print("Transcribing...")
        
                print("Loading audio: " + text_input)
                y, sr = librosa.load(text_input)
                tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

                if len(beats) <= 1:
                    print("Audio too short...")

                main(input_dir=text_input)

    # def run(self):
    #     print("Not yet implemented...")

    # def set_input(self):
    #     print("Setting input file directory...")
    #     file_dir = select_file()
    #     self.audio_input_field.delete(0, END)
    #     self.audio_input_field.insert(0, file_dir)

    # def update_audio_input_field(self):
    #     self.audio_input_dir = self.audio_input_field.get()

# End class MainFrame


class FileInput(Frame):
    def __init__(self, master, input_label=None, input_text=None):
        Frame.__init__(self, master)

        if input_label is not None:
            self.input_label = input_label + ": "
        else:
            self.input_label = "Input"

        if input_text is not None:
            self.input_text = input_text
        else:
            self.input_text = ""


        self.input_label = Label(self, text=self.input_label)
        self.input_label.grid(row=0, column=0, sticky=W)

        self.input_entry = Entry(self, width=40)
        self.input_entry.grid(row=0, column=1, sticky=W)

        self.browse_input_button = Button(self, text="Browse",
            command=self.set_input)
        self.browse_input_button.grid(row=0, column=2, sticky=W)

        self.grid(columnspan = 3)


        # This is a callback function to handle keyboard inputs.
        def validate_input(input_str):
            # Every input to the field
            # print(input_str)
            self.input_text = input_str
                # maybe call an update function here
            return True
                # There's no actual input validation.
                # But, this is just for handling keyboard inputs.
        # Register the callback function to an entity.
        registration = self.register(validate_input)
            # register is a widget only method.
        self.input_entry.config(validate="key",
                validatecommand=(registration, "%P"))
            # config. Also a widget only method
            # validate. Validate whenever a key is pressed. 
            # validatecommand. Tells which function needs to be called.

    def set_input(self):
        file_dir = select_file()
        self.input_entry.delete(0, END)
        self.input_entry.insert(0, file_dir)
        self.input_text = file_dir

    def get_file(self):
        return self.input_text

# End class InputField


def select_file():
    """ Opens a file selection dialogue (window)
        Selects the filename
        Returns string filename
    """
    current_dir =  os.getcwd()

    filename =  filedialog.askopenfilename(
        initialdir = current_dir,
        title = "Select file",
        filetypes = (("mp3, wav","*.mp3 *.wav"),("all files","*.*"))
    )

    print("Selected file: {}".format(filename))
    
    return filename
# End select file



class FolderSelector:
    def __init__(self, root, label):
        self.text = label
        self.directory = ""
        self.folderSelected = IntVar()

        self.frame = Frame(
            root,
            width=500,
            height=500
            ) # main frame of directory selector

        self.label = Label(self.frame, text=label + ": ")

        self.entry = Entry(
            self.frame,
            textvariable="directory", width=35)

        self.checkButton = Checkbutton(self.frame, text=None,
            variable=self.folderSelected, state="disabled")

        self.button = Button(
            self.frame,
            text="Choose Folder",
            command=self.chooseFolder)

        self.displayContentButton = Button(
            self.frame,
            text="Print Contents",
            command=self.printContents)

        self.testButton = Button(
            self.frame,
            text="Test",
            command=self.test)

        # temporary values
        # self.directory = "unspecified"
        # self.entry.delete(0, END)
        # self.entry.insert(0,self.directory)

        # This is the assigning of the component positions 
        self.checkButton.grid(row=0, ) # sticky="w"
        self.label.grid(row=0, column=1) # sticky="e"
        self.entry.grid(row=0, column=2)
        self.button.grid(row=0, column=3)
        self.displayContentButton.grid(row=0, column=4)
        # self.testButton.grid(row=0, column=4)
        
        self.frame.pack()

    def chooseFolder(self):
        print(self.text + " is selecting folder")
        self.directory = filedialog.askdirectory()

        # Change entry test if folder has been selected
        if (path.isdir(self.directory)):
            self.entry.delete(0, END)
            self.entry.insert(0, str(self.directory))
            self.checkButton.select()


    def printContents(self):
        count = 0;
        for file in listdir(self.directory):
            count = count + 1
            print ("contains: [{0}] {1}...".format(count, file)) # format
            # play file
            # playsound('scott.wav')

    def test(self):
        print("Testing now...")
        
        print("overlay_sound sample run...")
        overlay_sound()

        print("Test end...")

    # Initialization for testing
    def setFolder(self, filepath):
        self.directory = filepath
        self.checkButton.select()
        self.entry.delete(0, END)
        self.entry.insert(0, filepath)





def main(input_dir, tempo=None, whitelist=None, blacklist=None, remove=None,
    classes=None, test=None):
 
    # skip_produce_instruments = False
    if not skip_produce_instruments:
        create_folder(sound_destination)    # setup_sound_destination()

        if use_default_sound_source:
           check_if_default_sound_source_is_available() # folder_ops.py

        produce_rest_samples() # audio_ops.py

        """ Transfer and mix files from samples folder
            to the DTT directory for consistent application usage """

        produce_single_instruments() # single core # old
            # Save single instruments to ./Produced Drums/one

        """ Compute the predicted produced sample count for a progress bar """

        """ Produce double instruments by combining single instruments """
        produce_double_instruments()
        # print("Produce just up to double.")
        
        produce_triple_instruments()
        produce_quadruple_samples()

    # End if produce_instruments
        # skip
    # print("\nDone producing instruments...")    
    
    # skip_extract_features = False
    if not skip_extract_features:
        print("ext...")
        extract_features() # feature_ops.py # procedural programming
        
    # halt()

    skip_loading_features = False
    if not skip_loading_features: 
        # if not skip_load_features_from_file:
        # Load features from csv to memory for KNN
        # class_feat_dict = import_features() # feature_ops.py, dictionary
        # class_feat_dict = import_features("simple") # feature_ops.py, dictionary
        # class_feat_dict = import_features() # feature_ops.py, dictionary

        print("1classes: {}".format(classes))
        
        class_feat_dict = import_features(
            whitelist=whitelist, blacklist=blacklist, remove=remove,
            classes=classes) 
        # class_feat_dict = import_features(whitelist=whitelist) 
        # class_feat_dict = import_features(type="simple") # type -> classes
            # feature_ops.py, dictionary

        # print("class_feat_dict: ")
        # print(class_feat_dict)

        # dictionary of string and id
        class_code_dict = get_class_code(class_feat_dict) # classification_ops.py

        print("\nclass_code_dict: ")
        for key, value in class_code_dict.items():
            print(key + ": " + str(value))
        # End if not skip_load_features_from_file

        # class_code_from_csv = csv_to_dictionary("./temp/class_legend.csv")
        # print("\nclass_code_from_csv: ")
        # for key, value in class_code_from_csv.items():
        #     print(key + ": " + str(value))


        # Create a list of just all the features in a numpy array,
        # And also create a list of just the corresponding label
         # for each feature row
        features, labels = get_features_and_labels(
            class_feat_dict, class_code_dict) # classification_ops.py

        print("\nlabels list len: " + str(len(labels)))
        print("features shape: " + str(features.shape))
        print("features size: " + str(features.size))
        # print("features: ")
        # print(features)
        # print("labels: ")
        # print(labels)

        # halt()

        """ NumPy - Indexing & Slicing
            https://www.tutorialspoint.com/numpy/numpy_indexing_and_slicing.htm
        """

        # # Slice features to improve KNN Accuracy
        # features = features[..., :20]
            # remove the columns beyond the 20th column
        # print("features shape: " + str(features.shape))

        if test != None:
            test_classify(features, labels, test=test)
            print("Test done...")
            sys.exit()

        # # sample_dir = "./Roland-SC-88-Ride-Bell.wav"
        # sample_dir = "./acoustic-kick_G#_major.wav"

        # print("Extracting...")
        # feat_arr = extract_audio_features(sample_dir) # feature_ops.py
        # print("\nfeat_arr.shape: ")
        # print(feat_arr.shape)

        # # classify is able to identify array of inputs, 
        #     # with a little modification
        # prediction = classify(feat_arr, features, labels)
        # print("prediction:")
        # print(prediction)

        # # classification_ops.py
        # class_name = get_class_name_using_id(prediction[0], class_code_dict)

        # print("Predicted instrument:")
        # print(class_name)
    # End if skip loading features

    # input_dir = "./bass_snare_hihat_loop.wav"
    # input_dir = "./Slow Rock Drum Beat 75 BPM - JimDooley.net.wav"
    # input_dir = "./slow_rock.wav" 
    # input_dir = "./slow_beat.mp3"

    # input_ops.py
    in_aud_feat_arr, quarter_timing_dict_list, tempo, \
        down_beat_sixteenth_note_indices = process_input(input_dir, tempo=tempo) 
        # in_aud_feat_arr is a numpy array containing
            # all features per hit stacked together
        # quarter_timing_dict_list is a list of dictionaries
            # which may contain keys 1, e, &, a

    print("\nin_aud_feat_arr.shape: {}".format(in_aud_feat_arr.shape))
    print("len(quarter_timing_dict_list): {}"\
            .format(len(quarter_timing_dict_list)))
    print("len(down_beat_sixteenth_note_indices): {}"\
            .format(len(down_beat_sixteenth_note_indices)))

    print("\nClassifying input...")

    # classify is able to identify array of inputs, with a little modification
    prediction = classify(in_aud_feat_arr, features, labels)
    print("prediction:")
    print(prediction)
    print("prediction.shape: {}".format(prediction.shape))



    # classification_ops.py
    class_names = get_class_name_using_id(prediction, class_code_dict)

    print("class_names: {}".format(class_names))
    print("quarter_timing_dict_list: {}".format(quarter_timing_dict_list))


    # print("Show assumed downbeats: ")
    # down_beat_positions = find_down_beat(input_dir)
    # downbeat_index = 0
    # assumed_downbeats = []

    # class_name_index = 0
    # for quarter_measure, quarter_timing_dict \
    #     in enumerate(quarter_timing_dict_list):
    #     print("quarter measure: " + str(quarter_measure))
    #     for rhythm, value in quarter_timing_dict.items(): 
    #         # possible keys: "1", "e", "&", "a"
    #         if class_name_index >= len(class_names):
    #             print("\t1/4 rest")
    #             break
    #         # print("\trhythm: {}".format(rhythm))
    #         # print("\t" + rhythm + ": " + class_names[class_name_index])
    #         print("\t" + rhythm + ": " + str(value))
    #         # if rhythm == "1" or rhythm == "2" or rhythm == "3" or rhythm == "4":
    #         #     assumed_downbeats.append(value)

    #         if downbeat_index < len(down_beat_positions):
    #             if down_beat_positions[downbeat_index] \
    #                 in range(value[0], value[1]):
    #                 print("\t\tdownbeat[{}]: {}".format(downbeat_index,
    #                     down_beat_positions[downbeat_index]))
    #                 downbeat_index += 1
    #             elif down_beat_positions[downbeat_index] < value[0]:
    #                 print("\t\t> downbeat[{}]: {}".format(downbeat_index,
    #                     down_beat_positions[downbeat_index]))
    #                 downbeat_index += 1

    #         class_name_index += 1
    # # End show assumed downbeats

    # print("len(down_beat_positions): {}".format(len(down_beat_positions)))
    # print("printed {}...".format(downbeat_index))

    # print("assumed_downbeats:")
    # print(assumed_downbeats)
    # print("extracted downbeats:")
    # print(down_beat_positions)





    print("Show prediction: ")
    class_name_index = 0
    for quarter_measure, quarter_timing_dict \
        in enumerate(quarter_timing_dict_list):
        print("quarter measure: " + str(quarter_measure))
        for rhythm, value in quarter_timing_dict.items(): 
            # possible keys: "1", "e", "&", "a"
            if class_name_index >= len(class_names):
                print("\t1/4 rest")
                break
            # print("rhythm: {}".format(rhythm))
            print("\t" + rhythm + ": " + class_names[class_name_index])
            class_name_index += 1
    # End show prediction

    # Combine the class_names list and the quarter_timing_dict_list
    # as a new list of dictionaries, where the keys ("1", "e", "&", "a")
    # are mapped to a class_name (eg. bass, snare, tom, etc.)
    print("Combining class names with rhythm...")
    rhythym_class_name_dict_list = []

    indexed_rhythym_class_name_dict_list = []

    class_name_index = 0
    for quarter_measure, quarter_timing_dict \
        in enumerate(quarter_timing_dict_list):
        rhythym_dict = {}
        indexed_rhythm_dict = {}
        for rhythm in quarter_timing_dict: # possible keys: "1", "e", "&", "a"
            if class_name_index >= len(class_names):
                break
            rhythym_dict[rhythm] = class_names[class_name_index]
            key = str(quarter_measure) + " " + rhythm
            indexed_rhythm_dict[key] = class_names[class_name_index]

            class_name_index += 1
        rhythym_class_name_dict_list.append(rhythym_dict)
        indexed_rhythym_class_name_dict_list.append(indexed_rhythm_dict)
    # End show prediction

    # Make 2 Types of simplication
    # 1. Basic beat: hihat, bass, snare
    # 2. More complex than 1
    # However, this simplified classification should be done in the KNN level.
    rhythym_class_name_dict_list = simplify_pattern(rhythym_class_name_dict_list)
        # classification_ops.py

    filename = os.path.basename(input_dir)
    filename_wo_ext = os.path.splitext(filename)[0]

    # convert_to_midi(rhythym_class_name_dict_list, bpm=tempo,
        # filename=filename_wo_ext) # midi_ops.py

    convert_to_midi(indexed_rhythym_class_name_dict_list, bpm=tempo,
        filename=filename_wo_ext) # midi_ops.py

    print("Combining class names with indexed_rhythm...")
    rhythym_class_name_dict_list = []
    class_name_index = 0
    for quarter_measure, quarter_timing_dict \
        in enumerate(quarter_timing_dict_list):
        rhythym_dict = {}
        for rhythm in quarter_timing_dict:
            # possible keys: "20 1", "20 e", "20 &", "20 a"
            indexed_rhythm = str(quarter_measure) + " " + rhythm
            print("indexed_rhythm: {}".format(indexed_rhythm))
            if class_name_index >= len(class_names):
                break
            rhythym_dict[indexed_rhythm] = class_names[class_name_index]
            class_name_index += 1
        rhythym_class_name_dict_list.append(rhythym_dict)
    # End show prediction

    print("down_beat_sixteenth_note_indices:")
    print(down_beat_sixteenth_note_indices)

    for _ in range(10):
        mark() # draw a sword

    convert_to_lilypond(rhythym_class_name_dict_list, bpm=int(round(tempo)),
        filename=filename_wo_ext,
        down_beat_positions=down_beat_sixteenth_note_indices
        ) # lily_ops.py

    # print("\nConcern for lily_ops: what if the downbeat was missed?\n")
    # print("Possible solution: capture the downbeat during the transition " \
    #     + "between quarter notes, which is at the part where the " \
    #     + "4th count transitions to the 1st count, but the beat won't start " \
    #     + "at the first count or the downbeat itself.")

    # print("Exiting main()...")

    print("\nTranscription successful.")

    print("\nThere's a concern. Have an option to manually input the "
        + "downbeat. There's problem on the initial onset recognition.")
    print("Possible fixes: Be sure to capture the first actual onset.")
    print("or, automate downbeat identification.")
    print("Another possible fix is to add silence in front of the beat, " 
        + "then detect onset.")
    print("But I think the beat tracker, itself, for quarter note slices "
        + "misses the first beat.")
    print("Be strict to start onset at the downbeat.")

# End main()







