import gc
import pyb
import cotask
import task_share
import utime
from enc_driver import EncoderConfig
from motor_driver import MotorConfig
from servo import Servo
from pid_controller import PID



# initialize the encoder and motor drivers
m_config = MotorConfig('PA10', 'PB4', 'PB5', pyb.Timer(3))
e_config = EncoderConfig('PC6', 'PC7', pyb.Timer(8))

# initialize the servo
servo1 = Servo('servo1', m_config, e_config)
servo1.zero()

pid1 = PID(0, 34434, kp = float(input('Input Kp: ')))

servo1.enable_motor()

servo1.set_duty_cycle(25)

utime.sleep_ms(100)

servo1.disable_motor()

print(servo1.read())