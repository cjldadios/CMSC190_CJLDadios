

""" Global Variables
    # Global varibles are fully spelled out
"""

import os
from multiprocessing import Process, Value, Array


""" Runtime
Sound combination: 4 min, 18 sec (625 samples max)
Feature extraction: (625 samples max) < 2 hours
"""





""" File Operations """

maximum_limit = 1000 # ceiling count of samples to be produced for each class
limit_base = 25
    # if 25, will produce 25*25 = 625 samples maximum
    # on combined each 2, 3 and 4 instruments
instruments = ["bass", "snare", "stick", "tom", "floor", \
            "hihat", "hihat-open", "crash", "ride", "bell"]

sound_source = "./../Sampled Drums Select"
sound_destination = "./Produced Drums"


global_variables = {} # used if using...
instrument_count = {} # ...one process ony

blacklist = [] # Each string is separated by space
whitelist = [] # Each string is separated by space

two_instrument_types_except_with_bass_list = []


""" End File Operations """




""" Audio Operations """

skip_produce_instruments = True # Editable

# number_of_process = os.cpu_count()
number_of_process = 1

use_default_sound_source = True
mix_volumes = True
use_mono = True

target_decibel = {
    "rest": -80,
    "bass": -10, 
    "snare": -20,
    "stick": -15,
    "tom": -22,
    "floor": -16,
    "hihat": -17,
    "hihat-open": -21,
    "crash": -27,
    "ride": -29,
    "bell": -28
    }

""" End Audio Operations """



""" Feature Operations """

skip_extract_features = True # Editable
skip_loading_features = False # Editable

skip_load_features_from_file = False # leave this as false

feature_destination = "./Extracted Features"

audio_samples_limit_per_class = 625 # does not have to be more than 625
# audio_samples_limit_per_class = 10 # does not have to be more than 625

cutoff_feature_array = True # leave this as true
feature_array_cutoff = 10 # Leave this to 20, now to 10

audio_features = ["spec_bw", "contrast", "zero_cr", "cent", \
            "flatness", "rolloff", "mfcc"]

as_average = {
    "spec_bw": True, 
    "contrast": True, 
    "zero_cr": True, 
    "cent": True, 
    "flatness": True, 
    "rolloff": True, 
    "mfcc": False
}

as_average = {
    "spec_bw": False, 
    "contrast": False, 
    "zero_cr": False, 
    "cent": False, 
    "flatness": False, 
    "rolloff": False, 
    "mfcc": False
} # The last declared will affect the program

class_features = {}

""" End Feature Operations """



""" Input Operations """


sliced_input_destination = "./Sliced Input"
sub_sliced_input_destination = "./Sub Sliced Input"
backtrack_offset = 1100 # optimized manually, global variable
is_track_downbeat = False # editable

""" End Input Operations """