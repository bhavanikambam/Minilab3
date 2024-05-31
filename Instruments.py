from Buzzer import *

class Instrument:
    """
    Create a generic instrument class
    """

    def __init__(self):
        self._notes = []

    def getNote(self, key):
        # Return the note corresponding to the key
        # Error check - make sure a valid key was pressed
        if key < len(self._notes):
            return self._notes[key]
        else:
            raise ValueError("Invalid key!!!!")

class Organ(Instrument):
    def __init__(self):
        self._notes = [DO, RE, MI, FA, SO, LA, TI, DO2]

class Violin(Instrument):
    def __init__(self):
        self._notes = [tones['C5'], tones['D5'], tones['E5'], tones['F5'], tones['G5'], tones['A5'], tones['B5'], tones['C6']]