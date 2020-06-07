"""
    Extraction
"""

import sys # First import sys
import os

import librosa
import numpy

# Local application/library imports
sys.path.insert(0, os.path.abspath("") + "/components") 

from global_vars import *
from global_ops import *
from folder_ops import *



def extract_audio_features(audio_path=None, y=None, sr=None):

    # Cutoff length of each audio features
    cutoff = feature_array_cutoff # global variable

    features = {} # Dictionary where to initially store extracted features  

    cutoff = feature_array_cutoff # global variable
    # Save the feature arrays (1x20, cutoff), and mfcc (1x13)
    # as a 1-dimensional numpy array
    # There are n-1, one by cutoff, audio features, (or 1 x 20)
    # where 1 is mfcc which is 1x13
    feat_arr_len = (len(audio_features)) * cutoff # feature arrray length
        # I'm placing this code up here to save a bit of overhead


    # Initialization of the feature array
    # with the proper column length
    inst_feat_arr = numpy.empty(feat_arr_len)
       

    # Load the audio as a waveform `y`
    # Store the sampling rate as `sr`


    # print("y:")
    # print(y)
    # print("sr: " + str(sr))

    if audio_path != None:
        # print("audio_path != ''")
        print("Extracting features of an onset...")
        y, sr = librosa.load(audio_path)

    # Getting spectral bandwidth
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
  
    if as_average["spec_bw"]: # boolean, global
        features["spec_bw"] = numpy.average(spec_bw)
    else:
        features["spec_bw"] = spec_bw

    # Getting spectral contrast
    S = numpy.abs(librosa.stft(y))
    contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
    if as_average["contrast"]:
        features["contrast"] = numpy.average(contrast)
    else:
        features["contrast"] = contrast

    # Getting zero crossing rate
    zero_cr = librosa.feature.zero_crossing_rate(y)
    if as_average["zero_cr"]:
        features["zero_cr"] = numpy.average(zero_cr)
    else:
        features["zero_cr"] = zero_cr

    # Getting spectral centroid
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    if as_average["cent"]:
        features["cent"] = numpy.average(cent)
    else:
        features["cent"] = cent

    # Getting spectral flatness
    flatness = librosa.feature.spectral_flatness(y=y)
    if as_average["flatness"]:
        features["flatness"] = numpy.average(flatness)
    else:
        features["flatness"] = flatness


    # Getting spectral rolloff
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    if as_average["rolloff"]:
        features["rolloff"] = numpy.average(rolloff)
    else:
        features["rolloff"] = rolloff


    # Getting mfcc
   
    # mfcc = librosa.feature.mfcc(y=y, sr=sr, lifter=3) 
    mfcc = librosa.feature.mfcc(y=y, sr=sr) 
        # lifter makes the coefficient aprroximately linear (?)

    # mfcc = numpy.resize(mfcc, (20, cutoff))
        # used to be (20, 13)
    
    # columns_average = X.mean(axis=0)
    # self.features["mfcc"] = numpy.average(mfcc)
    mfcc_averaged = mfcc.mean(axis=1)
    features["mfcc"] = mfcc_averaged
    print("mfcc.shape: {}".format(features["mfcc"].shape))
    print("mfcc.shape: {}".format(mfcc.shape))
    print("spec_bw.shape: {}".format(spec_bw.shape))
    print("contrast.shape: {}".format(contrast.shape))
    print("zero_cr.shape: {}".format(zero_cr.shape))
    print("cent.shape: {}".format(cent.shape))
    print("flatness.shape: {}".format(flatness.shape))
    print("rolloff.shape: {}".format(rolloff.shape))

    rolloff_time = librosa.frames_to_time(rolloff, sr=sr)
    rolloff_cut = numpy.resize(rolloff, (10,)) # used to be (20, frames)
    print("rolloff_cut.shape: {}".format(rolloff_cut.shape))
    print("rolloff_time: {}".format(rolloff_time))
    # how to resize 2d?

         
    halt()

    """ Edit! Average mfcc at axis=1,
        and do not resize, it's automatically 20 length
    """

    # https://www.youtube.com/watch?v=KzevshgDv8g

    #######################################################
    # Why take 13? https://www.researchgate.net/post/
    # Why_we_take_only_12-13_MFCC_coeffici
    # ents_in_feature_extraction
    # Get 2-13: http://practicalcryptography.com/miscellaneous/
    # machine-learning/guide-mel-frequency-cepstral-co\
    # efficients-mfccs/

    """ Cutoff audio features for performance reason """

    if cutoff_feature_array:
        for feat in audio_features: # Global variable
            features[feat] \
                = numpy.resize(features[feat], (1,cutoff))


    """ Average audio features for performance reason, KNN """
    for feat in audio_features: # Global list
        if as_average[feat]: # Global dictionary
            features[feat] = numpy.average(features[feat])


    audio_feat_list = [] # initialize here for reference (?)

    feat_index = 0
    for feat in audio_features:
        # print(feat + ": ")
        # print(features[feat].shape)
        if feat_index == 0: # first instanciation of numpy.array
            audio_feat_list = numpy.array(features[feat])
        else: # append the following features
            audio_feat_list \
                = numpy.append(audio_feat_list, features[feat])
            pass # break
        feat_index += 1

    return audio_feat_list
   
    # End for each audio samples of each audio class    
# End extract_audio_features()



if __name__ == '__main__':
    
    extract_audio_features(
        # audio_path="/home/cjldadios/Codes/DTT/acoustic-kick_G#_major.wav")
        # audio_path="/home/cjldadios/Codes/DTT/slow_beat.mp3")
        # audio_path="/home/cjldadios/Codes/DTT/slow_rock.wav")
        # audio_path="/home/cjldadios/Codes/DTT/036.wav")
        audio_path="/home/cjldadios/Codes/DTT/000.wav")