# CircuitPython macro keyboard for RingingRoom
#
# Copy to Raspberry Pi Pico as code.py

import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

class MacroButton():
    '''
    Handle all setup for a button connected to a pin with debounce timeout
    when button is pressed
    '''
    debounce = 0.2

    def __init__(self, pin, say, keyboard):
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.DOWN
        self.say = say
        self.keyboard = keyboard
        self.last_press = time.monotonic()

    def test(self):
        if self.button.value:
            now = time.monotonic()
            if now > self.last_press + MacroButton.debounce:
                self.last_press = now
                self.keyboard.send(self.say)

keyboard = Keyboard(usb_hid.devices)

buttons = []
buttons.append(MacroButton(board.GP15, Keycode.SPACE, keyboard))    # Ring bell
buttons.append(MacroButton(board.GP14, Keycode.B, keyboard))        # Bob
buttons.append(MacroButton(board.GP13, Keycode.N, keyboard))        # Single
buttons.append(MacroButton(board.GP12, Keycode.L, keyboard))        # Look to
buttons.append(MacroButton(board.GP11, Keycode.G, keyboard))        # Go next
buttons.append(MacroButton(board.GP10, Keycode.H, keyboard))        # That's all
buttons.append(MacroButton(board.GP9, Keycode.T, keyboard))         # Stand next

while True:
    for btn in buttons:
        btn.test()
