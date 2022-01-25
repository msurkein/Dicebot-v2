import gphoto2 as gp
import random
import time

camera = gp.Camera()
try:
    camera.init()
except gp.GPhoto2Error as gp:
    print("Failed to initialize camera.  Continuing without.\n{}".format(gp))
    camera = None

from gpiozero import PhaseEnableMotor
import requests

# pin 21 - OUTPUT - direction motor 2
# pin 30 - OUTPUT - speed motor 2

spin_speed = 0.15  # percent of spin speed.  1 = 1000 RPM
sleep_time = 1  # number of seconds to sleep up to (randomly chosen with this as the max)
spin_cycles = 5  # number of cycles per trial
trial_count = 10  # number of trial
dicebot_motor = PhaseEnableMotor(phase="WPI21", enable="WPI30", pwm=True)

for trial in range(1, trial_count):
    print(trial)
    for cyclenum in range(1, spin_cycles + 1):
        sleep_scalar = max(0.5, random.random())
        dicebot_motor.forward(spin_speed)
        time.sleep(sleep_scalar * sleep_time)
        dicebot_motor.backward(spin_speed)
        time.sleep(sleep_scalar * sleep_time)
    dicebot_motor.forward(spin_speed)
    time.sleep(sleep_time * 4)
    dicebot_motor.stop()
    time.sleep(sleep_time * 2)
    print("Getting URL")
    print('Capturing image')
    if camera is not None:
        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
        print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save("/tmp/test.jpg")
    with open("/tmp/test.jpg", "rb") as tjp:
        z = requests.post("http://192.168.1.248:8000", tjp.read())
    print(z.text)
    time.sleep(sleep_time * 2)
dicebot_motor.stop()
