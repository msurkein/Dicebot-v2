import time
import random
from gpiozero import PhaseEnableMotor

# pin 21 - OUTPUT - direction motor 2
# pin 30 - OUTPUT - speed motor 2

spin_speed = 0.15
sleep_time = 1.5
spin_cycles = 5
dicebot_motor = PhaseEnableMotor(phase="WPI21", enable="WPI30", pwm=True)

for trial in range(1,10):
    print(trial)
    for cyclenum in range(1,spin_cycles+1):
        dicebot_motor.forward(spin_speed)
        time.sleep(random.random()*sleep_time)
        dicebot_motor.backward(spin_speed)
        time.sleep(random.random()*sleep_time)
    dicebot_motor.forward(spin_speed*2)
    time.sleep(sleep_time*2)
    dicebot_motor.stop()
    time.sleep(sleep_time*2)
dicebot_motor.stop()