import time
from machine import Pin, I2C
from neopixel import NeoPixel
from ssd1306 import SSD1306_I2C
from StateModel import StateModel, BTN1_PRESS, BTN1_RELEASE, BTN2_PRESS, BTN2_RELEASE, BTN3_PRESS, BTN3_RELEASE, BTN4_PRESS, BTN4_RELEASE, BTN5_PRESS, NO_EVENT
from Button import Button
from Log import Log
from Buzzer import PassiveBuzzer
from Instruments import Organ, Violin

class MusicController:
    def __init__(self):
        # Instantiate buttons
        self._button1 = Button(12, "white", buttonhandler=self)
        self._button2 = Button(13, "red", buttonhandler=self)
        self._button3 = Button(14, "yellow", buttonhandler=self)
        self._button4 = Button(15, "blue", buttonhandler=self)
        self._button5 = Button(11, "grey", buttonhandler=self)

        # Instantiate other components
        self._buzzer = PassiveBuzzer(16)
        self._instrument = Organ()
        self._instrumentno = 0

        # Initialize I2C and Display
        self.i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)
        
        try:
            self.display = SSD1306_I2C(128, 64, self.i2c)
            self.display.fill(0)
            self.display.text('Piano', 0, 0)
            self.display.show()
        except OSError as e:
            Log.d(f'I2C Error: {e}')
            self.display = None

        # Initialize NeoPixel ring
        self.ring = NeoPixel(Pin(2), 16)

        # Instantiate the state model
        self._model = StateModel(10, self, debug=True)
        
        # Add buttons to the model
        self._model.addButton(self._button1)
        self._model.addButton(self._button2)
        self._model.addButton(self._button3)
        self._model.addButton(self._button4)
        self._model.addButton(self._button5)

        # Define state transitions
        self._model.addTransition(0, [BTN1_PRESS], 1)
        self._model.addTransition(1, [BTN1_RELEASE], 0)
        self._model.addTransition(0, [BTN2_PRESS], 2)
        self._model.addTransition(2, [BTN2_RELEASE], 0)
        self._model.addTransition(0, [BTN3_PRESS], 3)
        self._model.addTransition(3, [BTN3_RELEASE], 0)
        self._model.addTransition(0, [BTN4_PRESS], 4)
        self._model.addTransition(4, [BTN4_RELEASE], 0)
        self._model.addTransition(1, [BTN4_PRESS], 5)
        self._model.addTransition(5, [BTN4_RELEASE], 1)
        self._model.addTransition(2, [BTN4_PRESS], 5)
        self._model.addTransition(5, [BTN4_RELEASE], 2)
        self._model.addTransition(0, [BTN5_PRESS], 9)
        self._model.addTransition(9, [NO_EVENT], 0)
        self._model.addTransition(3, [BTN4_PRESS], 6)
        self._model.addTransition(6, [BTN4_RELEASE], 3)
        self._model.addTransition(4, [BTN4_PRESS], 7)
        self._model.addTransition(7, [BTN4_RELEASE], 4)
        self._model.addTransition(5, [BTN4_PRESS], 8)
        self._model.addTransition(8, [BTN4_RELEASE], 5)

    def changeInstrument(self):
        if self._instrumentno == 0:
            self._instrument = Violin()
            self._instrumentno = 1
        else:
            self._instrument = Organ()
            self._instrumentno = 0    

    def run(self):
        self._model.run()

    def stateDo(self, state):
        pass

    def stateEntered(self, state, event):
        Log.d(f'State {state} entered')
        if state == 0:
            pass
        elif state == 1:
            self._buzzer.play(self._instrument.getNote(0))
            self.blink_pattern1()
        elif state == 2:
            self._buzzer.play(self._instrument.getNote(1))
            self.blink_pattern2()
        elif state == 3:
            self._buzzer.play(self._instrument.getNote(2))
            self.blink_pattern3()
        elif state == 4:
            self._buzzer.play(self._instrument.getNote(3))
            self.blink_pattern4()
        elif state == 5:
            self._buzzer.play(self._instrument.getNote(4))
            self.blink_pattern1()
        elif state == 6:
            self._buzzer.play(self._instrument.getNote(5))
            self.blink_pattern2()
        elif state == 7:
            self._buzzer.play(self._instrument.getNote(6))
            self.blink_pattern3()
        elif state == 8:
            self._buzzer.play(self._instrument.getNote(7))
            self.blink_pattern4()
        elif state == 9:
            self.changeInstrument()
        
        self.update_display(state)

    def stateLeft(self, state, event):
        Log.d(f'State {state} exited')
        if state >= 1 and state <= 8:
            self._buzzer.stop()

    def update_display(self, state):
        if self.display:
            self.display.fill(0)  # Clear the display
            self.display.text('Piano', 0, 0)
            self.display.text(f'State: {state}', 0, 10)
            note_name = self._instrument.getNoteName(state - 1) if state > 0 else 'None'
            self.display.text(f'Note: {note_name}', 0, 20)
            self.display.show()

    def blink_pattern1(self):
        # Simple blink pattern
        for i in range(3):
            self.ring.fill((255, 0, 0))
            self.ring.write()
            time.sleep(0.2)
            self.ring.fill((0, 0, 0))
            self.ring.write()
            time.sleep(0.2)

    def blink_pattern2(self):
        # Chase pattern
        for i in range(16):
            self.ring[i] = (0, 255, 0)
            self.ring.write()
            time.sleep(0.05)
            self.ring[i] = (0, 0, 0)
            self.ring.write()

    def blink_pattern3(self):
        # Alternating pattern
        for i in range(4):
            for j in range(0, 16, 2):
                self.ring[j] = (0, 0, 255)
            self.ring.write()
            time.sleep(0.2)
            for j in range(1, 16, 2):
                self.ring[j] = (0, 0, 255)
            self.ring.write()
            time.sleep(0.2)
            self.ring.fill((0, 0, 0))
            self.ring.write()

    def blink_pattern4(self):
        # Rainbow pattern
        colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
        for color in colors:
            self.ring.fill(color)
            self.ring.write()
            time.sleep(0.3)