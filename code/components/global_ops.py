
import os
import sys
import random

from playsound import playsound # playing an audio
    # usage: playsound('/path/to/a/sound/file/you/want/to/play.mp3')
import pandas # dictionary to csv, vice-versa

from global_vars import *


def halt():
    print("\n    Oxxxxxxx{zzzzzzzzzzzzzzzzzzzz>\n")
    sys.exit()

def mark():
    print("\n                                Oxxxxxxx{zzzzzzzzzzzzzzzzzzzz>\n")

    # if not __name__ == "__main__": # if child process
    #     # get pid
    #     # terminate
    # else:
    #     print("Oxxxx{zzzzzzzzzzzzzz>")
    #     sys.exit()

def ring():
    # playsound("./../../Music/Over the Horizon 2016 - Over " \
        # + "the Horizon 2016 Samsung Galaxy Brand Sound by Dirty Loops.mp3")
    # playsound("./Produced Drums/single/snare/007.wav")
    # playsound("./Produced Drums/double/bass crash/007.wav")
    playsound("./acoustic-kick_G#_major.wav")

def blacklisted(inst_names_separated_by_space):
    print("\nChecking if '" + inst_names_separated_by_space \
        + "' is blacklisted")

    query_list = inst_names_separated_by_space.split()
    query_list.sort()

    for entry in blacklist:
        written_list = entry.split()
        written_list.sort()

        if query_list == written_list:
            return True
    # End for every entry in the blacklist

    return False
# End blacklisted()


def get_fetch_sample_sounds_multiprocessing_index_range_list():
    # Create a list of pairs: starting_index and stopping_index
    # To be iterated as arguments for multiprocessing
    index_range_list = []

    # For example,
    step = len(instruments)//number_of_process
        # Use floor division to remove decimals
        # if there are 9 instruments
        # and there are 4 CPU's
        # step <= 2 == 9/4

    for i in range(0, number_of_process):
        if i != number_of_process - 1: # while not reaching the last i (eg. 3)
            index_range_list.append((i*step, (i+1)*step))
                # Using the example,
                # i: 0
                #   index_range_list == [(0, 2)]
                # i: 1
                #   index_range_list == [(0, 2), (2, 4)]
                # i: 2
                #   index_range_list == [(0, 2), (2, 4), (4, 6)]
                # i: 3
                #   index_range_list == [(0, 2), (2, 4), (4, 6), (6, 8)]
        # What about the index 8 (inclusive)?        
        else: # if reached the last i (eg. 3)
            index_range_list.append((i*step, len(instruments)))
                # Notice the use of len(instruments)
                # When i: 3, this will produce
                #   index_range_list == [(0, 2), (2, 4), (4, 6), (6, 9)]

    print("index_range_list:")
    print(index_range_list)

    return index_range_list
# End get_fetch_sample_sounds_multiprocessing_index_range_list()



# Recursive function
def get_combine_two_sounds_multiprocessing_index_range_list(
    starting_index, stopping_index, partakers_count):

    """ This function divides the instrument indices
    for number_of_process processors.
    The division is like this:
        cpu_count == 1:
            Process 1 will get 100% of the indices
        cpu_count == 2:
            Process 1 gets the first 1/3 of the indices, while
            Process 2 gets the remaining 2/3 of the indices
        cpu_count == 4:
            Two processes will split the first 1/3 indices (first part).
                This "first part" will recursively be split again,
                    by, again, 1/3 and 2/3.
                One, among the two, process will take the (1/3) * (1/3)
                    of all the indices.
                The second one, among the two, will take the (1/3) * (2/3)
                    of all the indices.
            The other two process will take the remaining 2/3 (second part),
                recursively split as 1/3 and 2/3.
    This is because of this kind of loop...state

    """

    # Create a list of pairs: starting_index and stopping_index
    # To be iterated as arguments for multiprocessing
    index_range_list = []

    # Base case
    if partakers_count == 1:
        # return starting_index, stopping_index
        index_range_list.append((starting_index, stopping_index))
    
    # Recursive case
    else: # If more than one processes will partake the range
        # Usually, the process count are just 2, 4, 8, and so on.

        # Get the width of the index range
        index_width = stopping_index - starting_index
        # Divide it by two parts: 1/3 and 2/3
        thirds_point = starting_index + index_width//3
            # 'starting point + index_width//3' is the 1/3rd index mark,
            # contrary to the middle point which is 1/2
        # Part 1
        index_range_list.extend(
            get_combine_two_sounds_multiprocessing_index_range_list(
                starting_index, thirds_point, partakers_count//2))
                    # Parameters:
                    # 1. Starting index
                    # 2. 1/3rd mark index
                    # 3. The first half of process count
        # Part 2
        index_range_list.extend(
            get_combine_two_sounds_multiprocessing_index_range_list(
                thirds_point,
                stopping_index,
                partakers_count-(partakers_count//2)))
                    # Parameters:
                    # 1. 1/3rd mark index
                    # 2. Stopping index
                    # 3. The remaining half of process count

    # End if-else    

    return index_range_list

# End get_combine_two_sounds_multiprocessing_index_range_list()


def select_random_intrument_indices_list(inst_directory):
    print("\nSelecting random indices on the given instrument type, " \
        + "depending on the the actual insturment count, "\
        + "and on the selected limit.")

    # inst_count = instrument_count[inst_type]
        # dangerous variable for multiprocessing: instrument_count[inst_type]

    inst_dir = inst_directory
        # Eg. ./Sampled Drums/bass
    inst_count = len(os.listdir(inst_dir)) # Use this instead

    # Base is as in base and exponent
    # If limit_base is greater than or equal to the instrument sample count
    if limit_base >= inst_count:
        # No need to randomize
        return list(range(0, inst_count))
            # Just return all indices
    
    else: # the instrument sample count is larger than the limit base
        if limit_base > inst_count/2:
            """ If limit_base is more than half of inst_count,
                    meaning... 
                        inst_count: [-------------------|-------------------]
                        limit_base: [---------------------------] *removed*
                    It's faster to randomly unselect from
                        the instrument index list,
                        than to select random indices """

            indices = list(range(0, inst_count))
                # The all available indices are selected
            while len(indices) > limit_base:
                rand_index = random.randint(0,len(indices)-1)
                    # Use range up to len(indices) to make sure that
                    # every randomized index is valid
                indices.remove(indices[rand_index])
                    # Remove the randomly targeted object from the list
            return indices
            
        else:
            """ If limit_base is less than half of inst_count,
                    meaning... 
                        inst_count: [-------------------|-------------------]
                        limit_base: [--- selected ---]
                    It's faster to randomly unselect from
                        the instrument index list,
                        than to select random indices """
            
            initial_indices = list(range(0, inst_count))
                # The all available indices are selected initially
            rand_indices = [] # to be randomly selected indices

            while len(rand_indices) < limit_base: # while not selecting enough
                rand_index = random.randint(0,len(initial_indices)-1)
                    # Use range up to len(initial_indices) to make sure that
                    # every randomized index is valid
                rand_indices.append(initial_indices[rand_index])
                    # Add to the selected list the selected number
                    # using the random index
                initial_indices.remove(initial_indices[rand_index])
                    # After identifying and adding the index,
                    # remove the a target object from the list
                    # using the random index to avoid redundancy
            return rand_indices
            
        # End inner if-else...is the sample size close to limit_base or far
    # End outer if-else...is limit_base greater than available samples
# End select random indices based on limit_base


# Select two instrument types
# Except two instrument types with bass instrument
# Because, later on, each two insturment types on this list will be
# combined with the bass instrument, to produce three insturment types
def set_two_instrument_types_except_with_bass_list():
    # Get all the instrument folder names form the sound destination folder
    all_inst_type_list = os.listdir(sound_destination)
    # Remove all the identified single instruments
    for single_inst in instruments:
        # instruments is a global list containing all valid single instruments
        all_inst_type_list.remove(single_inst)
    
    # Remove types with bass instruments
    # Applies to 3 inst also, eg. bass snare to, which might already be
    # preset if this program has been run before
    for inst_type in all_inst_type_list:
        print(inst_type.split())
        if inst_type.split()[0] == "bass": 
        #     or inst_type.split()[1] == "bass": # eg. "bass snare"
        #     # print("removed")
        #     # print(inst_type)
            all_inst_type_list.remove(inst_type)

    # Another method to remove types with bass instruments
    for single_inst_type in instruments:
        single_inst_type_with_bass = "bass " + str(single_inst_type)
        # print(single_inst_type_with_bass)
        if single_inst_type_with_bass in all_inst_type_list:
            # print("Extists: " + single_inst_type_with_bass)
            all_inst_type_list.remove(single_inst_type_with_bass)

    print("all_inst_type_list:")
    print(all_inst_type_list)


    # Setting the value of the global variable...
    two_instrument_types_except_with_bass_list.extend(all_inst_type_list)
    # ...based on what this function got, or identified
    # (which are all the two instrument types, except with bass)

    # print(two_instrument_types_except_with_bass_list)

# End set_two_instrument_types_except_with_bass_list()



# Using the global list two_instrument_types_except_with_bass_list,
# identify the ranges of indicess needed to be distributed to processors
# according to number_of_process
def get_set_two_instrument_types_except_with_bass_index_range_list():
    # Create a list of pairs: starting_index and stopping_index
    # To be iterated as arguments for multiprocessing
    index_range_list = []

    two_inst_list = two_instrument_types_except_with_bass_list

    # For example,
    step = len(two_inst_list)//number_of_process
        # Use floor division to remove decimals
        # if there are 9 instruments
        # and there are 4 CPU's
        # step <= 2 == 9/4

    for i in range(0, number_of_process):
        if i != number_of_process - 1: # while not reaching the last i (eg. 3)
            index_range_list.append((i*step, (i+1)*step))
                # Using the example,
                # i: 0
                #   index_range_list == [(0, 2)]
                # i: 1
                #   index_range_list == [(0, 2), (2, 4)]
                # i: 2
                #   index_range_list == [(0, 2), (2, 4), (4, 6)]
                # i: 3
                #   index_range_list == [(0, 2), (2, 4), (4, 6), (6, 8)]
        # What about the index 8 (inclusive)?        
        else: # if reached the last i (eg. 3)
            index_range_list.append((i*step, len(two_inst_list)))
                # Notice the use of len(instruments)
                # When i: 3, this will produce
                #   index_range_list == [(0, 2), (2, 4), (4, 6), (6, 9)]

    print("index_range_list:")
    print(index_range_list)

    return index_range_list
# End get_set_two_instrument_types_except_with_bass_index_range_list()


# At the main function, after identifying
# the two-instrument types without bass,
# which is done by calling the previously written above function
def get_two_instrument_types_except_with_bass_index_range_plus_inst_list_():

    """ Count how many two_inst_non_bass_types are there.
    Distribute them by number_of_process, as range of indices.
    
    This is written like the function at the top,
    get_fetch_sample_sounds_multiprocessing_index_range_list()
    """

    index_range_list = []

    inst_count \
        = len(two_instrument_types_except_with_bass_list)

    print("inst_count: ", end="")
    print(inst_count)

    print("two_instrument_types_except_with_bass_list: ", end="")
    print(two_instrument_types_except_with_bass_list)

    halt()

    # For example,
    units_covered = inst_count//number_of_process
        # Use floor division to remove decimals
        # if there are 9 instruments
        # and there are 4 CPU's
        # step <= 2 == 9/4

    for i in range(0, number_of_process):
        if i != number_of_process - 1: # while not reaching the last i (eg. 3)
            index_range_list.append((i*units_covered, (i+1)*units_covered, \
                two_instrument_types_except_with_bass_list))
                    # plus two instruments list to make a tuple
                # Using the example,
                # i: 0
                #   index_range_list == [(0, 2)]
                # i: 1
                #   index_range_list == [(0, 2), (2, 4)]
                # i: 2
                #   index_range_list == [(0, 2), (2, 4), (4, 6)]
                # i: 3
                #   index_range_list == [(0, 2), (2, 4), (4, 6), (6, 8)]
        # What about the index 8 (inclusive)?        
        else: # if reached the last i (eg. 3)
            index_range_list.append((i*units_covered, inst_count, \
                two_instrument_types_except_with_bass_list))
                    # plus two instruments list to make a tuple
                # Notice the use of inst_count
                # When i: 3, this will produce
                #   index_range_list == [(0, 2), (2, 4), (4, 6), (6, 9)]

    print("index_range_list :  (tuple)")
    print(index_range_list)

    return index_range_list
# End get_two_instrument_types_except_with_bass_index_range_list()



""" https://stackoverflow.com/questions/34301088
    /reading-writing-out-a-dictionary-to-csv-file-in-python/34301228
"""

def dictionary_to_csv(dictionary, file_path):
    # Convert dictionary to pandas data frame
    data_frame = pandas.DataFrame.from_dict(dictionary, orient="index")
    # Create a csv file
    data_frame.to_csv(file_path) # file_path eg: ./temp/mydata.csv
# End dictionary_to_csv()


def csv_to_dictionary(file_path):
    # Read csv file into data frame
    data_frame = pandas.read_csv(file_path, index_col=0)
    # Convert data frame to dictionary
    dictionary = data_frame.to_dict("split")
    dictionary = dict(zip(dictionary["index"], dictionary["data"]))
    # Set value as int, not list of int
    dictionary_plain = {}
    for key, value in dictionary.items():
        dictionary_plain[key] = value[0]
    return dictionary_plain                                     
# End csv_to_dictionary()


