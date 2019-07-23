# - b5, #5, half-diminished, 13
# - better conditions for embelishments -- across chords
# - rhythm of melody
# - 6/9 chord
# - force at least one note between chords to remain constant across transitions
# - modes??


# Am A Dm E (dom7)



import pysynth_samp
pysynth_samp.patchpath = "C:\\Users\\charl\\Desktop\\SalamanderGrandPianoV3_48khz24bit\\48khz24bit\\"

import copy

import time
# guitar
#import pysynth_s as psb

# piano
#import pysynth_samp as psb

# organ
import pysynth as psb


import random
from pydub import AudioSegment

import winsound
from shutil import copyfile



NOTES   = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
NUMBERS = ["I", "II", "III", "IV", "V", "VI", "VII"]

# dials
KEY   = random.choice(NOTES)
MAJOR = True

CREATE_MELODY = False

CHORDS_IN_PROGRESSION = 4
BARS = 2

CHORD_DURATION  = 4
MELODY_DURATION = 4

PROGRESSION_OCTAVE    = random.randrange(3,4)
MELODY_OCTAVE         = random.randrange(4,7)

ALLOW_EXTENSIONS = False

BPM = 50 # random.randrange(50,80)

UNIQUE = False
FORCE_COMMON_NOTES_ACROSS_CHORD_CHANGES = True

NOTES.extend(NOTES)
NOTES.extend(NOTES)

class Progression:
    length = 8


class Chord:
    note_name = ""
    num = 0
    minor = False
    dim = False
    banned = False
    extension = ""
    extensions_enabled = False
    extension_set = False
    accent = False

    def power(self):
        return random.choice([True, False])

    # so I learned from this, that add2 and add9 have the same notes, just different
    # octaves, but since we randomize inversions, they could be the same chord
    def add2(self):
        return not self.chord_num() == "III" #self.chord_num() == "ii"

    def add9(self):
        return not self.chord_num() == "III" #self.chord_num() == "I" or self.chord_num() == "IV"

    def maj7(self):
        return not self.chord_num() == "vi" and not self.chord_num() == "ii" and not self.chord_num() == "III" #self.chord_num() == "I" or self.chord_num() == "IV"

    def maj6(self):
        return not self.chord_num() == "vi" and not self.chord_num() == "ii" and not self.chord_num() == "III"

    def sus2(self): # not sure of good numbers to apply sus chords to, or if to just combine them with parent chord
        return True#self.chord_num() == "vi" or self.chord_num == "V" or self.chord_num == "ii"

    def sus4(self):
        return True#self.chord_num() == "vi" or self.chord_num == "V" or self.chord_num == "ii"

    def dom7(self):
        return False
        return self.chord_num() == "V" or self.chord_num() == "ii"


    def aug(self):
        return False
        return self.chord_num() == "vi"

    def extensions(self):
        s = [""]
        # add 4th
        if self.add9():  s.append("add9")
        if self.add2():  s.append("add2")
        if self.maj7():  s.append("maj7")
        if self.maj6():  s.append("maj6")
        if self.dom7():  s.append("dom7")

        # move around the others
        if self.sus4():  s.append("sus4")
        if self.sus2():  s.append("sus2")
        if self.aug():   s.append("aug")
        if self.power(): s.append("5")
        return s
    
    def pick_extension(self):
        print("Ran pick extension")
        self.extension = random.choice(self.extensions())
        self.extension_set = True
        print("Set " + self.chord_num() + " to be " + self.extension)

    def type(self, number = False):
        s = ""
        s +=    "m " if (self.minor and not number) else ""
        s +=  "dim " if self.dim   else ""
        return s

    def notes(self):
        if not self.extension_set:
            self.pick_extension()

        l = [self.note_name] 

        # where middle finger goes
        second_offset = 4
        if self.minor or self.dim:
            second_offset = 3
        if self.extension == "sus2":
            second_offset = 2
        if self.extension == "sus4":
            second_offset = 5
        if self.power():
            second_offset = 0

        # where last finger goes
        third_offset  = 7
        if self.dim:
            third_offset  = 6
        if self.extension == "aug":
            third_offset = 8

        l.append(NOTES[NOTES.index(self.note_name) + second_offset])
        l.append(NOTES[NOTES.index(self.note_name) + third_offset])

        # add another finger if we have an extension with a 4th note
        if self.extension != "":
            fourth_offset = 0
            if self.extension == "add2":
                fourth_offset = 2
            if self.extension == "maj6":
                fourth_offset = 9
            if self.extension == "dom7":
                fourth_offset = 10
            if self.extension == "maj7":
                fourth_offset = 11
            if self.extension == "add9":
                fourth_offset = 14

            l.append(NOTES[NOTES.index(self.note_name) + fourth_offset])

        # crudely randomizing inversions
        notes = [i.lower() + str(PROGRESSION_OCTAVE + random.choice([0, 1])) for i in l]
        if self.accent:
            notes = [n + "*" for n in notes]
        return notes

    def chord_name(self):
        return self.note_name + self.type()

    def chord_num(self):
        number = NUMBERS[self.num]
        number = number.lower() if self.minor else number
        return number


def get_key(base_offset = 0, major = True):

    if major:
        ban                = [False, False, False,  False, False, False, True]  # you can ban 3 and 7 to make it less dissonant
        minor_pattern      = [False, True,  False,  False, False, True,  False]
        diminished_pattern = [False, False, False, False, False, False, True]
        pentatonic_pattern = [True,  True,  True,  False, True,  True,  False]
        increment_pattern  = [0, 2, 4, 5, 7, 9, 11]
    else:
        minor_pattern      = [True,  False, False, True,  True,  False, False]
        diminished_pattern = [False, True,  False, False, False, False, False]
        pentatonic_pattern = [True,  False, True,  True,  True,  False, True]
        increment_pattern  = [0, 2, 3, 5, 7, 8, 10]

    for i, (minor, increment, dim) in enumerate(zip(minor_pattern, increment_pattern, diminished_pattern)):
        chord           = Chord()
        chord.banned    = ban[i]
        chord.extensions_enabled = ALLOW_EXTENSIONS
        chord.note_name = NOTES[increment + base_offset]
        chord.minor     = minor
        chord.dim       = dim
        chord.num       = i
        #print(chord.chord_num(), "\t", chord.chord_name(), "\t", chord.notes(), "\t", "Optional extensions: ", chord.extensions())
        yield chord


def combine_sounds(files, out_file):
    sound = AudioSegment.from_file(files[0])
    for f in files[1:]:
        sound = sound.overlay(AudioSegment.from_file(f))
    sound.export(out_file, format="wav")

def common_notes(ch1, ch2):
    if not FORCE_COMMON_NOTES_ACROSS_CHORD_CHANGES:
        return True
    return any(list(set(ch1.notes()) ^ set(ch2.notes())))



def main():
    key = list(get_key(base_offset=NOTES.index(KEY), major=MAJOR))

    # first chord is the root
    starting_chord = copy.deepcopy(key[0])
    starting_chord.accent = True
    progression = [starting_chord]
                   #, key[0]]
    for i in range(1, CHORDS_IN_PROGRESSION*BARS):
        previous_chord = progression[i-1]
        while True:
            chord = copy.deepcopy(random.choice(key))
            chord.pick_extension()           
            if not chord.banned and common_notes(chord, previous_chord):
                progression += [chord]
                #progression += [chord]
                break
       

    timestr = time.strftime("%Y%m%d-%H%M%S")

    out_name    = "-".join([KEY] + [chord.chord_num() + chord.extension for chord in progression]) + "-" + timestr

    print(out_name)

    tracks = max([len(chord.notes()) for chord in progression])
    files  = [str(i) + ".wav" for i in range(tracks)]
    l      = [[] for _ in range(tracks)]

    for i in range(tracks):
        for chord in progression:

            if len(chord.notes()) > i:
                notes = (chord.notes()[i], CHORD_DURATION)
                l[i].append(notes)
            else:
                # if we're adding an extension to one of the chords, then we need another track
                # to fill in the space for the chords without the extension, just re-add their last note
                notes = (chord.notes()[i-1], CHORD_DURATION)
                l[i].append(notes)

    if CREATE_MELODY:
        melody      = [random.sample(chord.notes(), MELODY_DURATION) for chord in progression]
        melody      = [item for sublist in melody for item in sublist] # flatten list for when multiple notes per chord
        random.shuffle(melody)
        melody_l    = [(note, MELODY_DURATION*CHORD_DURATION) for note in melody]
        melody_fn   = out_name + "-melody" + ".wav"
        files       += [melody_fn]
        l           += [melody_l]

    for file, notes in zip(files, l):
        print(notes)
        psb.make_wav(notes, fn=file, bpm=BPM)

    combine_sounds(files, out_name + ".wav")

    winsound.PlaySound(out_name + ".wav", winsound.SND_LOOP + winsound.SND_ASYNC)

    keeper = input("Keeper? (Y/N): ")
    if keeper.lower() == "y":
        copyfile(out_name + ".wav", "Keepers/" + out_name + ".wav")


if __name__ == "__main__":
    main()
