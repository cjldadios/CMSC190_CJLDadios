""" Select sound source locations """

import os
import sys
import shutil

from global_vars import *


def setup_sound_destination():
    print("\nSetting up '" + sound_destination + "' folder...")
    create_folder(sound_destination) # create folder if unavailable

    for inst in instruments:
        inst_folder = sound_destination + "/" + inst
        print("Setting up '" + inst_folder + "' folder...")
        create_folder(inst_folder) # create folder if unavailable

    rest_folder = sound_destination + "/" + "rest"
    print("Setting up '" + sound_destination + "/rest ' folder...")
    create_folder(rest_folder) # create folder if unavailable


def check_if_default_sound_source_is_available():

    print("\nUsing default sound source...")

    print("\nValidating sound source...\n")

    if os.path.isdir(sound_source):
        print("Default source is a directory")
        print("Checking individual sound folders...")

        is_complete = True

        print("Checking sound folders...")
        for inst in instruments:
            inst_folder = sound_source + "/" + inst 

            if os.path.isdir(inst_folder):
                print(str(inst) + ":\tok")
                # print(str(inst) + " folder located, with "
                    # + len(os.listdir(sound_source + "/"
                    # + str(inst))) + " files")
            # elif os.path.isdir(sound_source + "/" + str(inst).lower()):
            #     print(str(inst) + ":\tok")
            #     # print(str(inst) + " folder located, with "
            #         # + str(len(os.listdir(sound_source))) + "/"
            #         # + str(inst).lower() + " files")
            else:
                print(str(inst) + ":\tmissing")
                is_complete = False

        if is_complete:
            print("No missing sample folder.")
        else:
            print("Sample folder missing!")
            sys.exit()

    else:
        print("Default source is invalid!")
        sys.exit()


def create_folder(directory):

    """ Create new folder if inextisting """

    if os.path.isdir(directory):
        print("\nDirectory '" + directory + "' already exists.")
    else:
        print("\nCreating directory '" + directory + "'")
        os.mkdir(directory)


def delete_folder(directory):
    # Try to delete Sliced Input Folder
    try:
      shutil.rmtree(directory)
    except OSError as e:
      print("Error: %s - %s." % (e.filename, e.strerror))