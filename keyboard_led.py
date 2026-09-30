import evdev
import sys
from gpiozero import LED

led = LED(17) # pin 11 (i hope)


# get da keyboard
local_devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
keyboard = None

# loops through all local devices to see if one is a keyboard, then sets that to a var to use for later
for local_device in local_devices:
	if "keyboard" in local_device.name.lower():
		keyboard = local_device
		break
if not keyboard:
	print("NO KEYBOARD FOUND. PLEASE PLUG ONE IN THROUGH USB!")
	sys.exit(1)
print(f"Hooked into local keyboard named: {keyboard.name}\npress any key (or drop something on the keyboard) to activate the LED")

# the logic behind actually turning the LED on :3
try:
	# this makes it so the keyboard does not... like... input stuff as it is a glorfied level
	keyboard.grab()
	for event in keyboar.real_loop():
		if event.type == evdev.ecodes.EV_KEY:
			key_event = evdev.categorize(event)
				# turns it on when it is pressed, off when it is not, shrimply simple
			if key_event.keystate == key_event.key_down:
				led.on()
			elif key_event.keystate == key_event.key_up:
				led.off()
except KeyboardInput:
	print("Exiting the keyboard lock phase (probs should unplug the keyboard")
finally:
	keyboard.ungrab()
	led.off()





