import evdev
import sys
import select
import time
from gpiozero import LED

led = LED(17) # this is pin 11

local_devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

#get all the keyboard interfaces for the keyboard 
keyboards = [d for d in local_devices if "keyboard" in d.name.lower()]

if not keyboards:
    print("NO KEYBOARD FOUND. STICK IT IN THE USB SLOT BRU!")
    sys.exit(1)

print(f"Hooked into {len(keyboards)} keyboard interfaces:")
for k in keyboards:
    print(f" - {k.name} on {k.path}")
    k.grab() # lock every interface so it doesn't type on the Pi, dont want it doing some messed up stuff when thing lands on it

print("\nProcess Active, drop something on the keyboard (press any key) to turn the led on")

# The logic behind actually turning the LED on :3
try:
    while True:
        r, w, x = select.select(keyboards, [], [])
        for k in r:
            for event in k.read():
                if event.type == evdev.ecodes.EV_KEY:
                    key_event = evdev.categorize(event)
                    if key_event.keystate == key_event.key_down:
			time.sleep(6)
                        led.on()
except OSError:
    print("you unplugged the keyboard, or something did idk")
except KeyboardInterrupt:
    print("\nExiting the keyboard lock phase... at last! (kidding smth went wrong, maybe)")
finally:
    for k in keyboards:
        k.ungrab()
    led.off()



