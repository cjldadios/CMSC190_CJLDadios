
import os
import sys

from midiutil import MIDIFile

from global_ops import *


""" Create lilypond file then call lilypond program to create a pdf """

def convert_to_lilypond(input_dict_list, bpm, filename,
    down_beat_positions):
    print("\nConverting predictions to lilypond...")

    # Create file
    file = open(filename + ".ly", "w")
    file.write("\\version \"2.18.2\"\n")
    file.write("\\header {\n")
    file.write("\ttitle = \"{}\"\n".format(filename))
    file.write("\tcomposer = \"  \"\n")
    file.write("\ttagline = ##f\n")
    file.write("}\n")
    # file.write("\\language \"english\"\n")
    file.write("\n")
    file.write("#(define harald '(\n")
    file.write("\t(bassdrum        default   #f           -3)\n")
    file.write("\t(snare           default   #f            1)\n")
    file.write("\t(sidestick       cross     #f            1)\n")
    file.write("\t(himidtom        default   #f            3)\n")
    file.write("\t(lowtom          default   #f           -1)\n")
    file.write("\t(hihat           cross     #f            5)\n")
    file.write("\t(openhihat       cross     \"open\"        5)\n")
    file.write("\t(pedalhihat      cross     #f           -5)\n")
    file.write("\t(crashcymbal     cross     #f            6)\n")
    file.write("\t(ridecymbal      cross     #f            4)\n")
    file.write("\t(ridebell        diamond   #f            4)))\n")
    file.write("\t% The number is 'semitones away from " \
        + "the middle staff (0)'\n")
    file.write("\n")

    drum_notes, lyrics \
        = get_lilypond_notes(input_dict_list, down_beat_positions)

    # Check the first note. If the first beat indicates no note or rest,
    # but just a duration (just a number)
    drum_notes_split = drum_notes.split()
    # print("\ndrum_notes_split[0]: {}".format(drum_notes_split[0]))

    # Somethimes the duration is dotted, so instead of "4" (numeric),
    # you may get a "8." (non numeric), and even double dotted or more...

    if drum_notes_split[0][0].isnumeric(): # ...so get the 1st char 
        # of the 1st string by double indexing, [0][0].
        drum_notes = "r" + drum_notes # ...write a small letter 'r' infront.
        # drum_notes = drum_notes.split(" ", 1)[2] # ...remove the number infront.
        
        # # Removing the number infront
        # temp = ""
        # for string in drum_notes_split[1:]: 
        #     temp += string + " "

        # drum_notes = temp
        # print("\n::")
        # print(drum_notes.split(" ", 1)[0])
        # print(">")
        # print(drum_notes.split(" ", 1)[1])

    # Check the end of drum_notes.
    # It should end with a number (note or rest with duration, e.g. <bd sn>16),
    # and not a > character (note or rest without duration, eg <sn hh>).
    # Loop string backwards
    duration = ""
    for i in range(len(drum_notes)-1, 0-1, -1):
        if drum_notes[i].isnumeric():
            duration = drum_notes[i] + duration
        elif drum_notes[i] == ">" or drum_notes[i] == "r":
            if duration == "":
                # No duration
                break

                # # Traverse, again, backwards to find the recent full bar.
                # for j in range(len(drum_notes)-1, 0-1, -1):

            else:
                # The last hit is indicated with a duration.
                break
        else:
            pass # Continue traversing backward.

    if duration == "":
        # No duration
        bar_completeness = 0
        completing_duration = "" # Numeric characters encountered

        # Traverse, again, backwards to find the recent full bar.
        for i in range(len(drum_notes)-1, 0-1, -1):
            # The loop exits when traversed fully or a bar symbol is found.
            if drum_notes[i] == "|":
                break

            if drum_notes[i].isnumeric():
                completing_duration = drum_notes[i] + completing_duration
            elif drum_notes[i] == "r" or drum_notes[i] == ">":
                # Compute duration to complete bar.
                if completing_duration != "":
                    bar_completeness += 1/int(completing_duration)
                    completing_duration = "" # Reset
        # End for traversing again

        # Computing the remaining duration
        remaining_duration = 1 - bar_completeness
        # here
        dur = duration_to_beat_length(remaining_duration)
            # Accepts a decimal parameter, returs string (i.e. "2 r8")

        # Completing drum_notes with the last duration.
        drum_notes += dur #+ " || "

    else:
        # The last hit is indicated with a duration.
        pass

    print("\ndrum_notes: {}".format(drum_notes))
    # halt()

    #################
    file.write("drum = \\drummode {\n")
    file.write("\t\\set DrumStaff.drumStyleTable = #(alist->" \
        + "hash-table harald)\n")
    file.write("\t\\stemUp\n")
    file.write("\t\\override Beam #'damping = #+i" \
        + "nf.0 % set beams horizontal\n")
    file.write("\t\\set Score.proportionalNotationDuration " \
        + " = #(ly:make-moment 1/32)\n")
    file.write("\t% Change to numeric style\n")
    file.write("\t\\numericTimeSignature\n")
    file.write("\t\\time 4/4\n")
    file.write("\t\\tempo 4 = {}\n".format(str(bpm)))


    file.write("\t% Disable beamExceptions because they are definitely\n")
    file.write("\t% defined for 4/4 time\n")
    file.write("\t\\set Timing.beamExceptions = #'()\n")
    file.write("\t\\set Timing.baseMoment = #(ly:make-moment 1/4)\n")
    file.write("\t\\set Timing.beatStructure = #'(1 1 1 1)\n")


    file.write("\t" + drum_notes + "\n")
    file.write("}\n")
    file.write("\n")
    
    file.write("lyric = \\lyricmode {\n")
    file.write("\t" + lyrics + "\n")
    file.write("}\n")
    file.write("\n")

    file.write("\\score {\n")
    file.write("<<\n")
    file.write("\\new DrumStaff{\n")
    file.write("\\new DrumVoice = \"mydrums\" { \\drum }\n")
    file.write("}\n")
    file.write("\\new Lyrics \\lyricsto \"mydrums\" { \\lyric }\n")    
    file.write(">>\n")
    file.write("}\n")
    file.write("\n")





    file.write("\n")
    file.write("% bassdrum bd\n")
    file.write("% snare sn\n")
    file.write("% sidestick ss\n")
    file.write("% himidtom tommh\n")
    file.write("% lowtom toml\n")
    file.write("% closedhihat hhc\n")
    file.write("% openhihat hho\n")
    file.write("% pedalhihat hhp\n")
    file.write("% crashcymbal cymc\n")
    file.write("% ridecymbal cymr\n")
    file.write("% ridebell rb\n")
    file.write("\n")
    file.write("% Harald Huyssen notation\n")
    file.write("% Crash: first ledger line above \n")
    file.write("% Ride: above the top line\n")
    file.write("% Hihat: through the top staff\n")
    file.write("% Rack tom: top space\n")
    file.write("% Floor tom: second space from below\n")


    file.close()

    # Create a pdf using the lilypond program
    print("\nCreating {}.pdf using lilypond...".format(filename))
    cmd = "lilypond {}.ly".format(filename)
    os.system(cmd) 
    # returned_value = os.system(cmd)  # returns the exit code in unix
    # print('returned value:', returned_value)

# End convert_to_lilypond()



def get_lilypond_notes(input_dict_list, down_beat_positions):
    print("\nWriting lilypond chords...")
   
    # input_dict_list is a list of dictionaries
    # The dictionaries have keys "1", "e", "&", "a"
    # where the values are class names, eg. "bass tom hihat ride"

    note_mapping = {
        "bass": "bd ",
        "stick": "ss ",
        "snare": "sn ",
        "floor": "toml ",
        "tom": "tommh ",
        # "hihat": "hhc ",
        "hihat": "hh ",
        "hihat-open": "hho ",
        "hihatp": "hhp ", # pedal
        "crash": "cymc ",
        "ride": "cymr ",
        "bell": "rb "
    } # Don't forget the space

    lyrics_mapping = {
        "1": "One",
        "e": "e",
        "&": "'n",
        "a": "a",
        "2": "two",
        "3": "three",
        "4": "four",
    } # Don't forget the space

    rhythm_start_time_dict = {
        "1": 0,
        "2": 1,
        "3": 2,
        "4": 3,
        "e": 1/4,
        "&": 1/2,
        "a": 3/4
    }

    quarter_note_start_distance = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "e": 1/4,
        "&": 1/2,
        "a": 3/4
    }

    
    hit_index = 0
    downbeat_index = 0
    is_first_note = True
    after_even_bar = True # 2 bars per line, alternating
        # ...break after the even bars
    drum_notes = ""
    lyrics = ""
    first_bar = " "
    is_first_bar_done = False
    is_downbeat = False
    quarter_note_index = 0
    prev_key = "1 1" # initialization of previous rhythm
    whole_note_monitor = 0 # add every note duration identified
    has_chord_on_downbeat = False
    is_whole_note_transition = False


    # For every quarter notes
    for index, quarter_dict in enumerate(input_dict_list):

        for sub_index, (key, val) in enumerate(quarter_dict.items()):
            # Key: Either one of 1, e, &, a
            # Val: class name


            # Actually, the keys are now indexed_keys,
            # eg. "20 1", "20 e", "20 &", and "20 a"

            print("\n\nkey: {}".format(key))
            print("val: {}".format(val))
            print("whole_note_monitor: {}".format(whole_note_monitor))
            split_prev_key = prev_key.split()
            split_key = key.split()
            beat_key = key.split()[1]

            if val != "rest": # It seems that lilypond does not alow
                # lyrics on rest notes.
                # So, if the onset is a rest, skip a lyric
                lyrics = lyrics + "" + lyrics_mapping[beat_key] + " "
                # Add the lyrics, the same way as adding the chords

            # Advance the beat depending on the rhythm, identified by the key


            
            # This is not the first note/chord,
            # so we may not add a beat.

            print("Not first note...")

            """ Add just the previous note duration, unlike in the
                where we add rest durations.
                And if the previous note was the downbeat (since
                is_downbeat is not yet updated, but later will),
                after indicating the duration, indicate also the
                "chord name" as "downbeat".
            """

            # Group notes with beams totaling a quarter note.
            # So, if this current beat is from a new quarter note group,
            # cut the duration of the previous note up to just the
            # beginning of this quarter note. Then, just fill the
            # gap with a rest for corresponding duration, up to this
            # current beat.

            split_key = key.split()
            quarter_note_id = split_key[0]
            beat_key = split_key[1]
            
            split_prev_key = prev_key.split()
            prev_quarter_note_id= split_prev_key[0]
            prev_beat_key = split_prev_key[1]

            print("quarter_note_id: {}".format(quarter_note_id))
            print("prev_quarter_note_id: {}".format(prev_quarter_note_id))
            

            # If the previous and the current notes are from the same group
            if quarter_note_id == prev_quarter_note_id:
                """ Add the duration of the previous note """
                print("Same quarter note group...")
                print("prev and current quarter note id: {}, {}"\
                    .format(prev_quarter_note_id, quarter_note_id))
                # 1, 2, 3, 4 will be 0
                prev_rhy = quarter_note_start_distance[prev_beat_key]
                curr_rhy = quarter_note_start_distance[beat_key]
                    # Decimal places
                prev_duration = curr_rhy - prev_rhy
                print("prev_duration (quarter note): {}".format(prev_duration))
                print("Adding prev duration...")
                if not is_first_bar_done:
                    dur = duration_to_beat_length(prev_duration)
                    first_bar = first_bar + dur
                    print("dur: {}".format(dur))
                    whole_note_monitor += get_duration(dur)

                else: # first bar done
                    dur = duration_to_beat_length(prev_duration)
                    drum_notes = drum_notes + dur
                    whole_note_monitor += get_duration(dur)
                # print("first_bar: {}".format(first_bar))
                # print("drum_notes: {}".format(drum_notes))

                print("whole_note_monitor: {}".format(whole_note_monitor))

            else: # If the previous note and the current note are from
                # a different quarter note grouping,
                # cut the previous note duration up to the starting
                # beat of the current quarter note.
               
                """ Add the duration of the previous note for a full
                    quarter note.
                    Then add another rest from the start of this
                    quarter note up to this onset.
                """

                print("New quarter note group, transition")
                # Compute prev_note_full_duration until the current beat
                # by getting their distance difference
                # Decimal places, where 1, 2, 3, 4 will be 0
                prev_rhy = quarter_note_start_distance[prev_beat_key]
                curr_rhy = quarter_note_start_distance[beat_key]
                # Ones place
                prev_num_id = int(prev_quarter_note_id)
                curr_num_id = int(quarter_note_id)
                # Combine ones and decimals, ones + decimal
                prev_position = prev_num_id + (prev_rhy) 
                curr_position = curr_num_id + (curr_rhy) 
                # Get the full note duration from prev to curr note
                prev_note_full_duration = curr_position - prev_position
                print("prev_note_full_duration: {}"\
                    .format(prev_note_full_duration))

                prev_note_actual_duration \
                    = prev_note_full_duration - curr_rhy
                    # curr_rhy is the rest duration from the first count
                        # of this quarter note group up to this
                        # current noteoffset
                print("prev_note_actual_duration: {}"\
                    .format(prev_note_actual_duration))

                print("Adding previous note duration...")
                # Apply the appropriate duration to the prev note
                if not is_first_bar_done:
                    dur = duration_to_beat_length(prev_note_actual_duration)
                    first_bar = first_bar + dur
                    whole_note_monitor += get_duration(dur)
                else:
                    dur = duration_to_beat_length(prev_note_actual_duration)
                    drum_notes = drum_notes + dur
                    whole_note_monitor += get_duration(dur)
                # print("first_bar: {}".format(first_bar))
                # print("drum_notes: {}".format(drum_notes))
                print("whole_note_monitor: {}".format(whole_note_monitor))

                """ Before adding the succeeding rest through the
                    new quarter note first count,
                    identify if the first count is a downbeat based
                    on the bar length (whole_note_monitor).
                    And if it's a downbeat, add a pipe to end to
                    end the bar.
                """

                # add the label somewhere here after adding the 
                # prev duration_to_beat_length
                if has_chord_on_downbeat: # needs to be resolved
                    # by adding a downbeat marker/label
                    print("Resolving a late addition of a downbeat " \
                        + "label after identifying the downbeat " \
                        + "chord and the corresponding duration...")
                    print("A chord marks the downbeat, " \
                        + "so adding the label here...")
                    if not is_first_bar_done:
                        last_char = first_bar[len(first_bar)-1]
                        if last_char == " ":
                            # Remove space
                            first_bar = first_bar[:-1]
                        first_bar = first_bar #+ "^\"downbeat A\" "
                    else: # if first bar is done
                        last_char = drum_notes[len(drum_notes)-1]
                        if last_char == " ":
                            # Remove space
                            drum_notes = drum_notes[:-1]
                        drum_notes = drum_notes #+ "^\"downbeat B\" "
                    has_chord_on_downbeat = False # late labeling resolved
                    print("The label should be added.")
                    # print("first_bar: {}".format(first_bar))
                    # print("drum_notes: {}".format(drum_notes))
                    print("whole_note_monitor: {}"\
                        .format(whole_note_monitor))


                print("Checking if the bar duration is occupied to 4/4...")
                print("whole_note_monitor: {}".format(whole_note_monitor))
                if whole_note_monitor == 1:
                    print("One bar duration complete")
                    print("Adding pipe (|) to end bar...")
                    if not is_first_bar_done:
                        first_bar = first_bar + " | \n"
                        is_first_bar_done = True
                        drum_notes += first_bar
                        first_bar = " "
                    else:
                        drum_notes = drum_notes + " | \n"
                    # reset 1 bar ruler
                    whole_note_monitor = 0

                # Commented out because this might not be an error,
                # because rest will be added after the pipe
                elif whole_note_monitor > 1:
                    print("Warning on lily_ops.py: bar length exceeded 4/4")
                    print("\nDoing the same thing as if " \
                        +"whole_note_monitor == 1, but whole_note_monitor..." \
                        + "will not reset to zero but to whole_note_monitor " \
                        + "- 1")
                    # sys.exit()
                    if not is_first_bar_done:
                        first_bar = first_bar + " | \n"
                        is_first_bar_done = True
                        drum_notes += first_bar
                        first_bar = " "
                    else:
                        drum_notes = drum_notes + " | \n"
                    # reset 1 bar ruler
                    whole_note_monitor = whole_note_monitor - 1
                else:
                    print("Bar duration is less than 4/4")

                # Still at "If a quarter note transition" block
                print("Adding rest duration after the starting count " \
                    + "of the current quarter note if there is...")
                # Also, add the appropriate rest duration from the 
                # starting count of the quarter note up to this onset
                rest_skip = 0 # also to be accessed after adding chord
                    # to indentiy where to add the chord name "downbeat"
                rest_skip = prev_note_full_duration \
                                            - prev_note_actual_duration
                
                # This is to tell whether/where to add "downbeat" label
                # has_rest_downbeat = False
                # if rest_skip > 0:

                # Remember that where on if quarter note 
                # transition block, but not on a bar transition

                # Before adding the downbeat rest, record the
                # whole_note_monitor for identifying if this is a 
                # whole note/bar transition, because when the downbeat
                # rest is added, the whole note monitor will also have
                # to be adjusted.
                if whole_note_monitor == 0:
                    is_whole_note_transition = True

                print("rest_skip: {}".format(rest_skip)) # rest_skip is decimal.
                # If the downbeat is a rest, write the rest with the
                # corresponding duration
                if rest_skip > 0:
                    # key_to_count_dict = {
                    #     "1": "one",
                    #     "2": "two",
                    #     "3": "three",
                    #     "4": "four",
                    #     "e": "e",
                    #     "&": "and",
                    #     "a": "a"
                    # }
                    # beat_count = key_to_count_dict[prev_beat_key]
                    
                    def key_to_count(q_ind):
                        beat = (q_ind) % 4 # This seems more correct
                        # beat = (q_ind + 1) % 4 # than this.
                        if beat == 0:
                            return "(one)"
                        elif beat == 1:
                            return "(two)"
                        elif beat == 2:
                            return "(three)"
                        elif beat == 3:
                            return "(four)"
                        else:
                            return "(none)"
                        
                    beat_count = key_to_count(index) # quarter note index

                    if not is_first_bar_done:
                        # print("First bar is not yet done.")
                        rest_skip = prev_note_full_duration \
                                                    - prev_note_actual_duration
                        dur = duration_to_beat_length(
                            rest_skip, rest=True, count=beat_count)
                        first_bar = first_bar + dur
                        whole_note_monitor += get_duration(dur)
                    else:
                        # print("First bar is done.")
                        rest_skip = prev_note_full_duration \
                                                    - prev_note_actual_duration
                        dur = duration_to_beat_length(
                            rest_skip, rest=True, count=beat_count)
                        drum_notes = drum_notes + dur
                        whole_note_monitor += get_duration(dur)
                # The rest skip was added if there was a skip at 1st count

                if is_whole_note_transition:
                    if rest_skip == 0:
                        print("Add the downbeat label later after " \
                            + "adding the identified chord and " \
                            + "adding the duration by the next beat of this...")
                        has_chord_on_downbeat = True
                    else:
                        print("The downbeat is a rest. Add the " \
                            + "marker from here.")
                        if not is_first_bar_done:
                            last_char = first_bar[len(first_bar)-1]
                            if last_char == " ":
                                # Remove space
                                first_bar = first_bar[:-1]
                            first_bar = first_bar #+ "^\"downbeat C\" "
                        else:
                            last_char = drum_notes[len(first_bar)-1]
                            if last_char == " ":
                                # Remove space
                                first_bar = drum_notes[:-1]
                            drum_notes = drum_notes #+ "^\"downbeat D\" "
                    is_whole_note_transition = False # reset
                        # becomes true until whole_note_monitor == 1 again

                # Done identifying a downbeat, if whole note transition

                # End if going to a new bar
                # elif whole_note_monitor > 0:
                #     print("")


                # print("first_bar: {}".format(first_bar))
                # print("drum_notes: {}".format(drum_notes))
                print("I think we may now proceed with adding a chord")


                """ Transfered to be done after indentifying the chord,
                    or not
                """
                # Append a chord name "downbeat" if the previous chord
                # was at a downbeat
                print("Adding chord name \"downbeat\" above " \
                    + " if this is a downbeat...")
                if is_downbeat:
                    if not is_first_bar_done:
                        # print("First bar is not yet done.")
                        first_bar = first_bar #+ "^\"downbeat E\""
                    else:
                        # print("First bar is done.")
                        drum_notes = drum_notes #+ "^\"downbeat F\""
                else:
                    print("Not adding chord name \"downbeat\"...")
                # print("first_bar: {}".format(first_bar))
                # print("drum_notes: {}".format(drum_notes))
                print("whole_note_monitor: {}".format(whole_note_monitor))
                

            # End check if new quarter note group
            # If else is_first_note    
            # Done adding appropriate previous note durations

            print("But first check if this is the down_beat...")

            # If this note/chord to be encoded has the downbeat
            # hit_index, from 0, indexes each onset
            # downbeat_index, from 0, indexes every downbeat positions
            print("hit_index: {}".format(hit_index))
            print("downbeat_index: {}".format(downbeat_index))
            # print("down_beat_positions[downbeat_index]: {}"\
            #     .format(down_beat_positions[downbeat_index]))
            print("Cheking if hit_index: {} ".format(hit_index))
            # print("is the down_beat_position: {}".format(
            #     down_beat_positions[downbeat_index]))
            print("beat_key: {}".format(beat_key))
            print("whole_note_monitor: {}".format(whole_note_monitor))
            
            is_redundant = True
            if is_redundant:
                print("Adding another \" | \" seems redundant...")
            else:
                # if hit_index == down_beat_positions[downbeat_index]:
                if beat_key == "1": # alternatively
                    is_downbeat = True # for marking the downbeat on the score

                    """ The current onset/hit/note/chord is the a downbeat.
                        This signals the end of a bar.
                    """

                    # If the first bar is done
                    # print("Yes, this hit is a downbeat. {} == {}"\
                    #     .format(hit_index, down_beat_positions[downbeat_index]))
                    print("Yes, this hit is a downbeat. {}".format(hit_index))
                    if is_first_bar_done:
                        print("is_first_bar_done: {}".format(is_first_bar_done))
                        print("Appending pipe (|) to drum_notes...")
                        # End the bar, before encoding the downbeat
                        drum_notes = drum_notes + " | "
                        # lyrics = lyrics + " | "
                        after_even_bar = not after_even_bar
                            # toggle every bar, starting as True from zero,
                            # set as False after odd
                        print("after_even_bar: {}".format(after_even_bar))
                        if after_even_bar:
                            print("Break staff to new line")
                            drum_notes = drum_notes + " \\break "
                    else: # if first bar is not done
                        # This marks the end of the first bar
                        print("is_first_bar_done: {}".format(is_first_bar_done))
                        print("The first bar was not yet done, but it is now")
                        is_first_bar_done = True
                        print("is_first_bar_done: {}".format(is_first_bar_done))

                        print("Appending pipe (|) to first_bar...")
                        after_even_bar = False # because this is the first bar (1)
                        print("after_even_bar: {}".format(after_even_bar))
                        first_bar = first_bar + " | " # End the first bar
                        # Append the first bar to drum_notes, which is the main
                        # string to record the drum chords.
                        # print("first_bar: {}".format(first_bar))
                        print("Appending first_bar + to the drum_notes...")
                        print("After...drum_notes: {}".format(drum_notes))
                        drum_notes = drum_notes + first_bar
                        print("After...drum_notes: {}".format(drum_notes))
                        first_bar = "" # clearing first bar
                        halt()
                    # Done checking is_first_bar_done, where to add the break
                # Done adding line breaks 
                else: # Else if not a down beat
                    is_downbeat = False # for marking the downbeat on the score
                    # print("No, this hit is a downbeat. {} == {}"\
                        # .format(hit_index, down_beat_positions[downbeat_index]))
                    print("No, this hit is a downbeat. {}".format(hit_index))
                    # Do nothing, really...
                # End of marking with a pipe symbol the end of a bar when
                # a down beat is encountered.
                print("Done checking if the current hit is a down_beat...")

            # End if redundant block, as if commented away

            prev_key = key # update prev_key,
                # used for measuring prevous note duration
                # Eg. prev_key = key, where key could be "1 3", or "1 e"

            # Identify the chord notes
            print("Adding the chord for value: {}".format(val))
            # Identify the present instruments then filter which
            # combinations are valid. Not really. This should be done
            # elsewhere.
            has_bass = False
            has_hihat = False # add the hihat last
            has_hihat_open = False
            four_hits_at_a_time = False
            has_rest = False
            hit_count = 0

            chord = ""

            for instrument in val.split(): # eg "bass snare hihat"
                if instrument == "hihat":
                    has_hihat = True
                    # Verify first the hihat later
                    # before incrementing hit_count
                elif instrument == "hihat-open":
                    has_hihat_open = True
                    # Verify first the hihat later
                    # before incrementing hit_count
                elif instrument == "rest":
                    has_rest = True
                else: # Add the rest of the instruments to the chord.
                    # Hihat has a special case instrument to be added last.
                    if instrument == "bass":
                        has_bass = True
                    chord = chord + note_mapping[instrument]
                    hit_count += 1 # verified sticking/hit
            # End for every instrument hit per rhythm

            # Add hihat last if there's hihat
            if has_hihat_open or has_hihat:
                if hit_count == 3: # If there's a limb available
                    # No other hihat option
                    chord = chord + note_mapping["hihatp"]
                    hit_count += 1 # recognize the hihat hit after verifying
                        # the hihat hit type, whether closed, open, or pedal
                elif hit_count == 2: # If two limbs were occupied
                    if has_bass: # but one of that limb is a bass
                        # so a hand is available, so option if open is available
                        if has_hihat_open:
                            chord = chord \
                                + note_mapping["hihat-open"]
                        else: # Closed hihat
                            chord = chord + note_mapping["hihat"] # closed
                        hit_count += 1 # recognize the hit after hihat is added
                    else: # If no bass, meaning two hands were used,
                        # we're only left to hit the hihat pedal
                        chord = chord + note_mapping["hihatp"] # pedal
                        hit_count += 1 # recognize the hit after hihat is added
                else: # If at most one limb was used, we have the option
                    # to hit the hihat closed or open.
                    if has_hihat_open:
                        chord = chord \
                            + note_mapping["hihat-open"]
                    else: # Closed hihat
                        chord = chord + note_mapping["hihat"] # closed
                    hit_count += 1 # recognize the hit after hihat is added
                # End choosing the hihat hit type
            # End adding hihat if a hihat was hit
            
            # If, despite adding instruments including hihat,
            # there was no recorded hit in that onset
            if hit_count == 0: 
                print("hit_count: {}".format(hit_count))
                print("No instrument within this onset...")
                chord = chord + " r" # Don't forget the space?
                # There were no instrument identified for this duration.
                # Still, this is an identified onset
                # lyrics = lyrics + "" + lyrics_mapping[beat_key] + " "

            elif has_rest == True:
                print("has_rest: {}".format(has_rest))
                print("Onset identified as rest. Weird...")
                chord = chord + " r" # Don't forget the space?
            else:
                chord = " <" + chord + ">" # Enclose the chord.

            # Done identifying the chord
            print("Identified chord: {}".format(chord))

            # Where to add the chord
            if not is_first_bar_done: # Complete the first bar first
                # print("First bar not done.")
                first_bar = first_bar + chord
            else:
                # print("First bar done.")
                drum_notes = drum_notes + chord   
            # Go back to...for each keys in a quarter note

            print("Adding the chord to the string of chord names...")
            print("first_bar: {}".format(first_bar))
            print("drum_notes: {}".format(drum_notes))
            print("Lyrics: {}".format(lyrics))

            # Hit is the chord itself
            hit_index += 1 # so increment hit_index for tracking downbeat

            # If this is the last quarter note, and
            # If this is the last sub beat of the quarter note interval
            if index == len(input_dict_list) - 1 \
                and sub_index == len(quarter_dict) - 1:
                # Computing the remaining rest for the end of the audio.
                # halt()
                pass



        # End for each rhythm within a quarter note duration
        quarter_note_index += 1

        # if quarter_note_index == 4:
        #     halt()

    # End for all the hits on each rhythm, aka for each quarter note interval

    return drum_notes, lyrics
# End get_lilypond_notes()


def duration_to_beat_length(quarter_note_measure, rest=None, count=None):
    # r is "r" for rest, default optional is ""
    if rest is None:
        r = ""
    else: # rest == True
        r = "r"

    if r != "r":
        if quarter_note_measure == 0.25:
            return r + "16 "
        elif quarter_note_measure == 0.5:
            return r + "8 "
        elif quarter_note_measure == 0.75:
            return r + "8. "
        elif quarter_note_measure == 1:
            return r + "4 "
        elif quarter_note_measure == 1.25:
            return r + "4 r16 "
        elif quarter_note_measure == 1.5:
            return r + "4. "
        elif quarter_note_measure == 1.75:
            return r + "4 r8. "
        elif quarter_note_measure == 2:
            return r + "2 "
        elif quarter_note_measure == 2.25:
            return r + "2 r16 "
        elif quarter_note_measure == 2.5:
            return r + "2 r8 "
        elif quarter_note_measure == 2.75:
            return r + "2 r8. "
        elif quarter_note_measure == 3:
            return r + "2. "
        elif quarter_note_measure == 3.25:
            return r + "2. r16 "
        elif quarter_note_measure == 3.5:
            return r + "2. r8 "
        elif quarter_note_measure == 3.75:
            return r + "2. r8. "
        else:
            return " "
    else:
        # If the hit is a rest, add "chord" marking the count,
        # because it's not possible (I think) in Lilipond to insert a
        # lyric where there's no note played, meaning rest.
        if quarter_note_measure == 0.25:
            r += "16 "
        elif quarter_note_measure == 0.5:
            r += "8 "
        elif quarter_note_measure == 0.75:
            r += "8. "
        elif quarter_note_measure == 1:
            r += "4 "
        elif quarter_note_measure == 1.25:
            r += "4 r16 "
        elif quarter_note_measure == 1.5:
            r += "4. "
        elif quarter_note_measure == 1.75:
            r += "4 r8. "
        elif quarter_note_measure == 2:
            r += "2 "
        elif quarter_note_measure == 2.25:
            r += "2 r16 "
        elif quarter_note_measure == 2.5:
            r += "2 r8 "
        elif quarter_note_measure == 2.75:
            r += "2 r8. "
        elif quarter_note_measure == 3:
            r += "2. "
        elif quarter_note_measure == 3.25:
            r += "2. r16 "
        elif quarter_note_measure == 3.5:
            r += "2. r8 "
        elif quarter_note_measure == 3.75:
            r += "2. r8. "
        else:
            r = " "

        # Add the chord before the first space
        split_r = r.split()
        # Recombine, adding the chord name after the first space.
        if count is None:
            count = "None"
        is_named_after_first = False
        new_r = ""
        for beat in split_r:
            if is_named_after_first == False:
                new_r += beat + "^" + "\"" + str(count) + "\"" + " "
                is_named_after_first = True # Just once
            else:
                new_r += beat + " "

        return new_r

# End duration_to_beat_length():


def get_duration(duration):
    """ Input of a string, eg. "2 r8. " or "r2 r8. "
        and output their total duration in fraction
    """



    prev = 0
    total = 0
    temp = ""

    def get_num_dict(c, temp=None):

        if c == ".":
            if temp == 0:
                return 1/2
            else:
                return (1/prev)*0.5
        else:
            return 1/int(c)
    # end convert char to fraction

    for c in duration:
        if c == " ": # time to evaluate the duration
            total += prev # should be zero if c was a number, and 1 if it was r
            if temp != "": # if not coming from
                
                # # parse int in temp, i.e. '8^"C#m"'
                # print("\n\ttemp: {}".format(temp))
                # if "^" in temp:
                #     temp = temp.split("^")[0] # Get the number ahead, i.e. 8.
                #     print("\ttemp: {}".format(temp))
                
                val = 1/int(temp) 
                total += val
            prev = 0 # done adding
            temp = ""
        elif c == "r":
            prev = 1 # r, alone, has a duration of 1
            temp = "" # no previous digits
        elif c == ".": # the previous c must be some digits
            total += prev * 0.5 # add half of the previous duration, could be 0
            if temp != "": # there were digits before this dot
                val = 1/int(temp) # add the first value...
                total = val + val*0.5 # and the half value
                prev = val*0.5 # The half value is the prev in a 
                    # case of another dot
        elif c.isnumeric(): # if c was a number
            # when a digit is encountered
            prev = 0 # ignore the previous and consider the following digit(s)
            temp += c # get the first digit
            # if end of duration
        else:
            pass
            # c could be pointing to any of 
            # the characters ^, ", C, , #, m, and " of (i.e.) '8^"C#m"'

    return total
# End get duration()