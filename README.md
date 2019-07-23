# WriteForMe
Generates chord progressions for you (a work in progress)

I started hacking together a quick script to generate interesting chord progressions in order to force myself to find a set of rules for what extensions sound good with what chords in the key. This thing spits out pretty cool sounding progressions -- some really nice, some less so. Certainly could be expanded upon and cleaned up, but I've actually found inspiration from it's output here and there.

Example output:
```
Picked the key of C#

Ran pick extension
Set I to be sus4
Ran pick extension
Set III to be sus2
Ran pick extension
Set V to be sus4
Ran pick extension
Set VII to be
Ran pick extension
Set V to be sus2
Ran pick extension
Set V to be add2
Ran pick extension
Set ii to be sus2
Ran pick extension
Set I to be sus2

Chose progression:
C#-Isus4-I-IIIsus2-Vsus4-Vsus2-Vadd2-iisus2-Isus2-20190723-033129

Creating wav file:
[('c#4*', 4), ('c#3', 4), ('f4', 4), ('g#3', 4), ('g#3', 4), ('g#4', 4), ('d#3', 4), ('c#3', 4)]
Writing to file 0.wav
[1/8]
[5/8]

[('f#3*', 4), ('c#4', 4), ('g3', 4), ('g#3', 4), ('g#4', 4), ('c3', 4), ('f4', 4), ('c#4', 4)]
Writing to file 1.wav
[1/8]
[5/8]

[('g#4*', 4), ('g#4', 4), ('c4', 4), ('d#3', 4), ('d#3', 4), ('d#4', 4), ('a#4', 4), ('g#4', 4)]
Writing to file 2.wav
[1/8]
[5/8]

[('c#3*', 4), ('g#3', 4), ('f4', 4), ('g#3', 4), ('g#4', 4), ('a#3', 4), ('d#4', 4), ('c#3', 4)]
Writing to file 3.wav
[1/8]
[5/8]

Keeper? (Y/N): y
Press any key to continue . . .
```
