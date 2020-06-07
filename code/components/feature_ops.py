"""
    Extraction
"""

import sys # First import sys
import os

import librosa
import numpy


from global_vars import *
from global_ops import *
from folder_ops import *


def extract_features():

    create_folder(feature_destination)

    inst_type_count = 0
    total_inst_type = 0
    print("Counting total instrument hit classes...")
    for hit_type in os.listdir(sound_destination): # Eg single, double, rest
        if hit_type == "rest":
            total_inst_type += 1
        else:
            hit_type_dir = sound_destination + "/" + hit_type
            total_inst_type += len(os.listdir(hit_type_dir))

    print("total_inst_type: ", end="")
    print(total_inst_type)

    # This is wrong!
    # cutoff = feature_array_cutoff # global variable
    # # Save the feature arrays (1x20, cutoff), and mfcc (1x13)
    # # as a 1-dimensional numpy array
    # # There are n-1, one by cutoff, audio features, (or 1 x 20)
    # # where 1 is mfcc which is 1x13
    # feat_arr_len = (len(audio_features)) * cutoff # feature arrray length
    #     # I'm placing this code up here to save a bit of overhead

    # The correct length
    feat_arr_len = 20 + 7 + 10*5 # This is correct, I think
        # mfcc, spec contrast, 5 other cut features




    hit_type_total = len(os.listdir(sound_destination))
    hit_type_index = 0

    # sound_destination is ./Produced Drums
    # For each instruments' by hit count type

    # for hit_type in os.listdir(sound_destination): # file system based
        # This line was replaced by the "for" condition below
        # Because the loop goes up to 223 instead of 113.
        # Maybe because there are hidden files that add to the indices

    hit_type_list = ["rest", "single", "double", "triple", "quadruple"]
    for hit_type in hit_type_list: # based on type names
        # hit_type may be single, double, triple, quadruple, and rest

        hit_type_dir = sound_destination + "/" + hit_type
            # Eg. ./Produced Drums/single

        if hit_type == "rest":
            print("dir: ", end="")
            print(hit_type_dir)

            inst_type_dir = hit_type_dir
                # Eg. ./Produced Drums/rest
                # rest is a class/inst_type
        
            audio_count = 0 # will be compared with the global variable
                # audio_samples_limit_per_class, for performance reasons

            """ Identify the limit """
            inst_audio_count = len(os.listdir(inst_type_dir)) # limitation
            limit = audio_samples_limit_per_class # induced limit

            # If the audio count is less than the limit
            if inst_audio_count < limit:
                limit = inst_audio_count # The iteration will not reach
                    # the induced limit

            # Initialization of the feature array
            # with the proper column length
            inst_feat_arr = numpy.empty(feat_arr_len)
                
            # Extract the features of each audio sample of "rest" instrument
            for audio_name in os.listdir(inst_type_dir):

                """ The documentation for this bock of code is in another
                    code block somewhere below, because it's a duplicate code
                """

                print("\nExtracting audio features... ")
                print("hit_type: " + str(hit_type))
                print("hit_type_index: " + str(hit_type_index))
                print("hit_type_total: " + str(hit_type_total))
                print("inst_type: " + audio_name)
                print("inst_type_index: " + str(inst_type_count))
                print("total_inst_type: " + str(total_inst_type))
                print("Audio index" + ": " + str(audio_count))
                print("Audio limit:" + str(limit))
                audio_path = inst_type_dir + "/" + audio_name
                features = {} # Dictionary for storing

                y, sr = librosa.load(audio_path)
                
                # spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
                # if as_average["spec_bw"]: # boolean, global
                #     features["spec_bw"] = numpy.average(spec_bw)
                # else:
                #     features["spec_bw"] = spec_bw
                # S = numpy.abs(librosa.stft(y))
                # contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
                # if as_average["contrast"]:
                #     features["contrast"] = numpy.average(contrast)
                # else:
                #     features["contrast"] = contrast
                # zero_cr = librosa.feature.zero_crossing_rate(y)
                # if as_average["zero_cr"]:
                #     features["zero_cr"] = numpy.average(zero_cr)
                # else:
                #     features["zero_cr"] = zero_cr
                # cent = librosa.feature.spectral_centroid(y=y, sr=sr)
                # if as_average["cent"]:
                #     features["cent"] = numpy.average(cent)
                # else:
                #     features["cent"] = cent
                # flatness = librosa.feature.spectral_flatness(y=y)
                # if as_average["flatness"]:
                #     features["flatness"] = numpy.average(flatness)
                # else:
                #     features["flatness"] = flatness
                # rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
                # if as_average["rolloff"]:
                #     features["rolloff"] = numpy.average(rolloff)
                # else:
                #     features["rolloff"] = rolloff
                # mfcc = librosa.feature.mfcc(y=y, sr=sr, lifter=3) 
                # mfcc = numpy.resize(mfcc, (20, cutoff)) # used to be (20, 13)
                # mfcc_averaged = mfcc.mean(axis=0)
                # features["mfcc"] = mfcc_averaged

                spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
                S = numpy.abs(librosa.stft(y))
                contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
                zero_cr = librosa.feature.zero_crossing_rate(y)
                cent = librosa.feature.spectral_centroid(y=y, sr=sr)
                flatness = librosa.feature.spectral_flatness(y=y)
                rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
                mfcc = librosa.feature.mfcc(y=y, sr=sr) 
                

                # MFCC and spectral contrast are averaged
                contrast_ave = contrast.mean(axis=1) # Becomes size 7
                mfcc_averaged = mfcc.mean(axis=1) # Must be axis 1 to be size 20
                features["contrast"] = contrast_ave # contrast must be averaged
                features["mfcc"] = mfcc_averaged
                # The rest are cut off,  # used to be (20, frames)
                spec_bw_cut = numpy.resize(spec_bw, (1, 10))
                features["spec_bw"] = spec_bw_cut
                zero_cr_cut = numpy.resize(zero_cr, (1, 10))
                features["zero_cr"] = zero_cr_cut
                cent_cut = numpy.resize(cent, (1, 10))
                features["cent"] = cent_cut
                flatness_cut = numpy.resize(flatness, (1, 10))
                features["flatness"] = flatness_cut
                rolloff_cut = numpy.resize(rolloff, (1, 10))
                features["rolloff"] = rolloff_cut
                
                
                # rolloff_time = librosa.frames_to_time(rolloff, sr=sr)
                # rolloff_cut = numpy.resize(rolloff, (1, 10))
                    # used to be (20, frames)
                # print("rolloff_cut: {}".format(rolloff_cut))
                # print("rolloff_time: {}".format(rolloff_time))
                # how to resize 2d?

                # if cutoff_feature_array:
                #     for feat in audio_features: # Global variable
                #         features[feat] \
                #             = numpy.resize(features[feat], (1,cutoff))
                # """ Average audio features for performance reason, KNN """
                # for feat in audio_features: # Global list
                #     if as_average[feat]: # Global dictionary
                #         features[feat] = numpy.average(features[feat])

                """ Done extracting features of an individual audio """

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
                # Stack the audio features of the same class
                if audio_count == 0: # extracted the features of the
                    inst_feat_arr = numpy.array(audio_feat_list)
                else: # of the suceeding count, just vertically stack array
                    inst_feat_arr \
                        = numpy.vstack([inst_feat_arr, audio_feat_list])
                """ We're done for this loop.
                    Code below is for what needs to be incremented
                """
                # End for each audio samples of each audio class
                """ Save as CSV"""
                print("Saving class features to file")
                inst_feat_dir = feature_destination + "/" + "rest" + ".csv"
                numpy.savetxt(inst_feat_dir, inst_feat_arr, delimiter=",")
                # Done extracting rest features
                
                # Updatables from the loop
                audio_count += 1
                if audio_count >= audio_samples_limit_per_class:
                    break # Limit the audio to be sampled per class
               
            # End for each rest audio sample

            inst_type_count += 1 # increment
            hit_type_index += 1


        else: # single, double, triple, quadruple
            
            print("dir: ", end="")
            print(hit_type_dir)

            for inst_type in os.listdir(hit_type_dir):
                # Eg. bass, bass snare, bass snare tom, bass snare tom hihat

                # inst_type_count += 1

                inst_type_dir = hit_type_dir + "/" + inst_type
                    # Eg. ./Produced Drums/single/bass
                
                """ Each inst_type is a class, eg. 'bass floor hihat-open' """

                audio_count = 0 # will be compared with the global variable
                    # audio_samples_limit_per_class, for performance reasons

                """ Identify the limit """
                inst_audio_count = len(os.listdir(inst_type_dir)) # limitation
                limit = audio_samples_limit_per_class # induced limit

                # If the audio count is less than the limit
                if inst_audio_count < limit:
                    limit = inst_audio_count # The iteration will not reach
                        # the induced limit

                # Initialization of the feature array
                # with the proper column length
                inst_feat_arr = numpy.empty(feat_arr_len)
                    # this will hold an rxc numpy array where
                    # r is the audio count, while
                    # c is the dimension count of the features extracted
                    # It looks like this
                    #          mfcc... | spec_bw... | contrast...
                    # audio 1  ..................................
                    # audio 2  ..................................

                # Extract the features of each audio sample of each class
                for audio_name in os.listdir(inst_type_dir):
                    
                    print("\nExtracting audio features... ")
                    print("hit_type: " + str(hit_type))
                    print("hit_type_index: " + str(hit_type_index))
                    print("hit_type_total: " + str(hit_type_total))
                    print("inst_type: " + inst_type)
                    print("inst_type_index: " + str(inst_type_count))
                    print("total_inst_type: " + str(total_inst_type))
                    print("Audio index" + ": " + str(audio_count))
                    print("Audio limit:" + str(limit))

                    audio_path = inst_type_dir + "/" + audio_name

                    features = {} # Dictionary for storing
                        # to be extracted features

                    # Load the audio as a waveform `y`
                    # Store the sampling rate as `sr`
                    y, sr = librosa.load(audio_path)

                    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
                    S = numpy.abs(librosa.stft(y))
                    contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
                    zero_cr = librosa.feature.zero_crossing_rate(y)
                    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
                    flatness = librosa.feature.spectral_flatness(y=y)
                    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
                    mfcc = librosa.feature.mfcc(y=y, sr=sr) 
                    

                    # MFCC and spectral contrast are averaged
                    contrast_ave = contrast.mean(axis=1) # Becomes size 7
                    mfcc_averaged = mfcc.mean(axis=1) 
                        # Must be axis 1 to be size 20
                    
                    features["contrast"] = contrast_ave 
                        # contrast must be averaged
                    features["mfcc"] = mfcc_averaged
                    # The rest are cut off,  # used to be (20, frames)
                    spec_bw_cut = numpy.resize(spec_bw, (1, 10))
                    features["spec_bw"] = spec_bw_cut
                    zero_cr_cut = numpy.resize(zero_cr, (1, 10))
                    features["zero_cr"] = zero_cr_cut
                    cent_cut = numpy.resize(cent, (1, 10))
                    features["cent"] = cent_cut
                    flatness_cut = numpy.resize(flatness, (1, 10))
                    features["flatness"] = flatness_cut
                    rolloff_cut = numpy.resize(rolloff, (1, 10))
                    features["rolloff"] = rolloff_cut

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


                    # print("audio_feat_list:")
                    # print(audio_feat_list.shape)
                    # print("inst_feat_arr:")
                    # print(inst_feat_arr.shape)


                    # Stack the audio features of the same class
                    """
                        code: feat_arr = numpy.vstack([feat_arr, features[feat]])
                        This works for stacking together numpy array
                        but must be same length
                    """

                    if audio_count == 0: # extracted the features of the
                        # first audio sample of the inst_type (class)
                        inst_feat_arr = numpy.array(audio_feat_list)
                            # initialize the numpy features array of this class
                    else: # of the suceeding count, just vertically stack array
                        inst_feat_arr \
                            = numpy.vstack([inst_feat_arr, audio_feat_list])
                   
                    """ We're done for this loop.
                        Code below is for what needs to be incremented
                    """

                    # Updatables from the loop
                    audio_count += 1


                    # Another condition to continue
                    # The number of audio samples per inst_type to be
                    # extracted of features is limited for performance concerns
                    if audio_count >= audio_samples_limit_per_class:
                        break # Limit the audio to be sampled per class
                            # For performance reasons
                            # The actual audio sample count per class is
                            # probably 625


                # End for each audio samples of each audio class

                """# Save as CSV"""

                print("Saving class features to file")
                inst_feat_dir = feature_destination + "/" + inst_type + ".csv"
                numpy.savetxt(inst_feat_dir, inst_feat_arr, delimiter=",")


                """ Update increments """
                inst_type_count += 1

            # End for each instrument type (or class)
            
            hit_type_index += 1

        # End else, hit type is not rest
    # End for each hit type: single, double, triple, quadruple, rest
# End extract_features()


# Load features from csv to memory for KNN
def import_features(classes=None, blacklist=None, whitelist=None, remove=None):
    print("Importing feature arrays from csv files...")

    scope = list(os.listdir(feature_destination))
    print("scope: {}".format(scope))

    # put uncommon list here, before opening file
    # Remove anything whith this in them, eg. if blacklist has
    # "bass stick", "bass snare stick ride" will also be removed.
    # uncommon = [
    #     ##### Most uncommon
    #     "bass stick",
    #     "bass tom",

    #     "snare stick",
    #     "snare tom",

    #     "stick bass",
    #     "stick snare",
    #     "stick tom",
    #     "stick floor",
    #     "stick hihat-open"
    #     "stick crash",
    #     "stick ride",
    #     "stick bell",
        
    #     "tom snare",
    #     "tom floor",
    #     "tom hihat",
    #     "tom hihat-open",
    #     "tom crash",
    #     "tom ride",
    #     "tom bell",

    #     "floor hihat",
    #     "floor crash",
    #     "floor bell",

    #     "hihat hihat-open",
    #     "hihat crash",
    #     "hihat ride",
    #     "hihat bell",

    #     "crash ride",
    #     "crash bell",

    #     "ride bell",
    #     #### Least uncommon, but still uncommon
    #     # "bass snare",
    #     # "bass tom",
    #     # "bass "
    # ]
    # # class_feat_dict = import_features(blacklist=blacklist)
    # # whitelist = ["bass", "snare", "hihat"]

    uncommon = []

    # Open ./Files/uncommon.txt
    if os.path.isfile("./Files/uncommon.txt"):
        print("Opening ./Files/uncommon.txt...")
        f = open("./Files/uncommon.txt", "r")
        for line in f:
            line = line.strip() # Remove leading and trailing white spaces
            # print(line)
            if len(line) == 0:
                pass
                # print("space")
            elif line[0] == "#":
                pass
                # print("comment")
            else:
                # print(line)
                uncommon.append(line)
        f.close()

    if whitelist is not None:
        print("whitelisting...")
        scope = get_inst_comb(whitelist)
        print("new scope: {}".format(scope))

    if classes != None:
        if classes[0] == "simple":
            print("classes simple")
            combo = ["bass", "snare", "hihat"]
            scope = get_inst_comb(combo)
            # print("scope: {}".format(scope))

    print("remove: {}".format(remove))

    if remove is not None:
        if remove[0] == "uncommon":
            print("Considering to remove uncommon...")
            if blacklist is not None:
                blacklist.extend(uncommon)
            else:
                blacklist = uncommon
        else:
            blk_lst = []
            for combo in remove:
                print("combo: {}".format(combo))
                insts = combo.split(",")
                print("insts: {}".format(insts))
                classif = " ".join(insts) # join with space
                print("classif: {}".format(classif))
                blk_lst.append(classif)
            
            if blacklist is not None:
                blacklist.extend(blk_lst)
            else:
                blacklist = blk_lst

    print("blacklist: {}".format(blacklist))

    if blacklist != None:
        # Remove the blacklisted from scope
        
        scope_split = []
        for scp in scope:
            scp_name = os.path.splitext(scp)[0] # remove file extension
            print("scp_name: {}".format(scp_name))
            scp_split = scp_name.split() # split by spaces
            print("scp_split: {}".format(scp_split))
            scp_split.sort()
            print("sorted scp_split: {}".format(scp_split))
            scope_split.append(scp_split)


        black_split = []
        for black in blacklist:
            print("black: {}".format(black))
            blk_split = black.split()
            print("blk_split: {}".format(blk_split))
            blk_split.sort()
            print("sorted blk_split: {}".format(blk_split))
            black_split.append(blk_split)


        blacklist_names = []

        for blklst_inst_str in blacklist:
            blklst_insts = blklst_inst_str.split()
            blklst_insts_len = len(blklst_insts)

            print("comparing: {}".format(blklst_insts))

            counter = 0
            
            # print("Checking blacklists: {}".format(blacklist))

            # For each blacktlist inst name
            for i, inst_list in enumerate(scope_split):
                # print("\tif in official: {}".format(scope_split))
                print("\tinst_list: {}".format(inst_list))
                
                for blklst_inst in blklst_insts:
                    if blklst_inst in inst_list:
                        counter += 1
                    else:
                        break
                print("\t\tcounter: {}".format(counter))

                # ...add to scope unsorted list using i
                if counter == blklst_insts_len:
                    # print("\nfound in scope[{}]: {}".format(i, scope[i]))
                    # Save in a list
                    print("adding this one...")
                    blacklist_names.append(scope[i])
                
                counter = 0

        print("blacklist_names")
        for blklst in blacklist_names:
            print("\t{}".format(blklst))

        for blklst in blacklist_names:
            if blklst in scope:
                scope.remove(blklst)

    print("blacklist: {}".format(blacklist))
    print("scope: {}".format(scope))

    inst_index = 0

    feat_dict = {}

    for inst_feat_file in scope:

        inst_feat_dir = feature_destination + "/" + inst_feat_file
        # Loading data from csv as numpy array
        data = numpy.loadtxt(inst_feat_dir , delimiter=',')


        print("Loading " + inst_feat_dir + "")
        print("index: " + str(inst_index))
        

        print("data: ")
        # print(data)
        print(data.shape)

        inst_type = inst_feat_file.split(".")[0]

        feat_dict[inst_type] = data

        inst_index += 1

    # End for each inst_feat_file

    # print("feat_dict: ")
    # print(feat_dict)

    # class_features = feat_dict
    return feat_dict

# End import_features()


def get_inst_count_from_csv():
    inst_type = inst_file.split(".")[0]

    inst_hit_count = len(inst_type.split())

    if inst_hit_count == 1:
        if inst_type == "rest":
            inst_hit_type = "" # rest
        else:
            inst_hit_type = "single/"
    elif inst_hit_count == 2:
        inst_hit_type = "double/"
    elif inst_hit_count == 3:
        inst_hit_type = "triple/"
    elif inst_hit_count == 4:
        inst_hit_type = "quadruple/"

    inst_dir = sound_destination + "/" + inst_hit_type + inst_type

    print("inst count: " + str(len(os.listdir(inst_dir))))

    inst_index += 1
# End get_inst_count_from_csv()


def extract_audio_features(audio_path=None, y=None, sr=None):

    # Cutoff length of each audio features
    cutoff = feature_array_cutoff # global variable

    features = {} # Dictionary where to initially store extracted features  

    # cutoff = feature_array_cutoff # global variable
    # # Save the feature arrays (1x20, cutoff), and mfcc (1x13)
    # # as a 1-dimensional numpy array
    # # There are n-1, one by cutoff, audio features, (or 1 x 20)
    # # where 1 is mfcc which is 1x13
    # feat_arr_len = (len(audio_features)) * cutoff # feature arrray length
    #     # I'm placing this code up here to save a bit of overhead

    # The correct length
    feat_arr_len = 20 + 7 + 10*5 # mfcc, spec contrast, 5 other cut features


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

    # # Getting spectral bandwidth
    # spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
  
    # if as_average["spec_bw"]: # boolean, global
    #     features["spec_bw"] = numpy.average(spec_bw)
    # else:
    #     features["spec_bw"] = spec_bw

    # # Getting spectral contrast
    # S = numpy.abs(librosa.stft(y))
    # contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
    # if as_average["contrast"]:
    #     features["contrast"] = numpy.average(contrast)
    # else:
    #     features["contrast"] = contrast

    # # Getting zero crossing rate
    # zero_cr = librosa.feature.zero_crossing_rate(y)
    # if as_average["zero_cr"]:
    #     features["zero_cr"] = numpy.average(zero_cr)
    # else:
    #     features["zero_cr"] = zero_cr

    # # Getting spectral centroid
    # cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    # if as_average["cent"]:
    #     features["cent"] = numpy.average(cent)
    # else:
    #     features["cent"] = cent

    # # Getting spectral flatness
    # flatness = librosa.feature.spectral_flatness(y=y)
    # if as_average["flatness"]:
    #     features["flatness"] = numpy.average(flatness)
    # else:
    #     features["flatness"] = flatness


    # # Getting spectral rolloff
    # rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    # if as_average["rolloff"]:
    #     features["rolloff"] = numpy.average(rolloff)
    # else:
    #     features["rolloff"] = rolloff


    # # Getting mfcc
   
    # # mfcc = librosa.feature.mfcc(y=y, sr=sr, lifter=3) 
    # mfcc = librosa.feature.mfcc(y=y, sr=sr) 
    #     # lifter makes the coefficient aprroximately linear (?)

    # mfcc = numpy.resize(mfcc, (20, cutoff))
    #     # used to be (20, 13)
    
    # # columns_average = X.mean(axis=0)
    # # self.features["mfcc"] = numpy.average(mfcc)
    # mfcc_averaged = mfcc.mean(axis=0)

    #             mfcc_averaged = mfcc.mean(axis=1) 
                        # Must be axis 1 to be size 20

    # features["mfcc"] = mfcc_averaged
    

    # # https://www.youtube.com/watch?v=KzevshgDv8g

    # #######################################################
    # # Why take 13? https://www.researchgate.net/post/
    # # Why_we_take_only_12-13_MFCC_coeffici
    # # ents_in_feature_extraction
    # # Get 2-13: http://practicalcryptography.com/miscellaneous/
    # # machine-learning/guide-mel-frequency-cepstral-co\
    # # efficients-mfccs/

    # """ Cutoff audio features for performance reason """

    # if cutoff_feature_array:
    #     for feat in audio_features: # Global variable
    #         features[feat] \
    #             = numpy.resize(features[feat], (1,cutoff))


    # """ Average audio features for performance reason, KNN """
    # for feat in audio_features: # Global list
    #     if as_average[feat]: # Global dictionary
    #         features[feat] = numpy.average(features[feat])


    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    S = numpy.abs(librosa.stft(y))
    contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
    zero_cr = librosa.feature.zero_crossing_rate(y)
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    flatness = librosa.feature.spectral_flatness(y=y)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr) 
    

    # MFCC and spectral contrast are averaged
    contrast_ave = contrast.mean(axis=1) # Becomes size 7
    mfcc_averaged = mfcc.mean(axis=1) # Must be axis 1 to be size 20
    features["contrast"] = contrast_ave # contrast must be averaged
    features["mfcc"] = mfcc_averaged
    # The rest are cut off,  # used to be (20, frames)
    spec_bw_cut = numpy.resize(spec_bw, (1, 10))
    features["spec_bw"] = spec_bw_cut
    zero_cr_cut = numpy.resize(zero_cr, (1, 10))
    features["zero_cr"] = zero_cr_cut
    cent_cut = numpy.resize(cent, (1, 10))
    features["cent"] = cent_cut
    flatness_cut = numpy.resize(flatness, (1, 10))
    features["flatness"] = flatness_cut
    rolloff_cut = numpy.resize(rolloff, (1, 10))
    features["rolloff"] = rolloff_cut
                
    

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




# def get_inst_comb(*instruments):
        # scope = get_inst_comb("bass", "snare", "hihat")
def get_inst_comb(instruments):

    
    """ 
        This function is used by import_features().
        It takes any number of string name of instruments.
        returns a string list of combination class names.
    """

    selected_wo_ext = os.listdir(feature_destination) # global feat_dest.
    selected_classes = []
    official_names = []
    single = []
    double = []
    triple = []
    quadruple = []

    # Get one hit instruments
    single = list(instruments)

    print("single: {}".format(single))

    # Get two hit instruments
    if len(single) >= 2:
        # Get combination of the names, where the order doesn't matter
        for i in range(len(single)):
            for j in range(i+1, len(single)):
                if not ((single[i] == "hihat" and single[j] == "hihat-open") \
                    or (single[i] == "hihat-open" and single[j] == "hihat")):
                    name = single[i] + " " + single[j]
                    double.append(name)
    print("double: {}".format(double))

    # Get three hit instruments
    if len(single) >= 3:
        # You can only get three hits at a time if either one is
        # a bass or a hihat
        print("tripling...")
        if "bass" in single:
            print("bass is in single")
            print("double: {}".format(double))
            for insts in double:
                print("insts: {}".format(insts))
                print("insts_spl: {}".format(insts.split()))
                if "bass" not in insts.split():
                    name = "bass" + " " + insts
                    print("\nname: {}".format(name))
                    triple.append(name)      
        if "hihat" in single:
            for insts in double:
                if "bass" not in insts.split() \
                    and "hihat" not in insts.split() \
                    and "hihat-open" not in insts.split():
                    name = "hihat" + " " + insts
                    triple.append(name)
        if "hihat-open" in single:
            for insts in double:
                if "bass" not in insts.split() \
                    and "hihat" not in insts.split() \
                    and "hihat-open" not in insts.split():
                    name = "hihat" + " " + insts
                    triple.append(name)
    
    print("triple: {}".format(triple))
    
    # Get four hit instruments
    if len(single) >= 4:
        # The only way for four instruments is using four limbs
        if "bass" in single and ("hihat" in single or "hihat-open" in single):
            for insts in double:
                if "bass" not in insts.split() \
                    and ("hihat" not in insts.split() \
                        or "hihat-open" not in insts.split()):
                    name = "bass hihat" + " " + insts
                    quadruple.append(name)
    print("quadruple: {}".format(quadruple))

    selected_classes.extend(single)
    selected_classes.extend(double)
    selected_classes.extend(triple)
    selected_classes.extend(quadruple)

    # print("selected_classes: {}".format(selected_classes))

    # get the official class names
    for selected in selected_classes:
        print("selected: {}".format(selected))
        selected_names = selected.split()
        selected_names.sort()
        # print("sorted selected_names: {}".format(selected_names))
        for file_name in selected_wo_ext:
            class_name = os.path.splitext(file_name)[0]
            # print("file_name: {}".format(file_name))
            # print("class_name: {}".format(class_name))
            present_insts = class_name.split()
            present_insts.sort()
            # print("\tsorted present_insts: {}".format(present_insts))
            if selected_names == present_insts:
                official_names.append(file_name)
                break

    # official_names("rest") # finally
    print("\nofficial_names: {}".format(official_names))

    return official_names
# End get_inst_comb()