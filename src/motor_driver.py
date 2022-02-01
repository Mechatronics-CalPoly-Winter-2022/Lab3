"""! 
@brief Offers functionality for driving the motor with PWM.
"""

import pyb      # import the micropy library


class MotorConfig:
    '''!
    This class is a container for the motor configuration.
    '''
    args: tuple

    def __init__(
        self, ena: str, in1: str, in2: str, timer: 'pyb.Timer'
            ) -> None:
        '''!
        Creates a motor configuration by saving the pins and timer.
        @param ena The pin to which the motor's enable pin is connected
        @param in1 The pin to which the motor's input 1 is connected
        @param in2 The pin to which the motor's input 2 is connected
        @param timer The timer to use for the motor
        '''
        self.args = (ena, in1, in2, timer)


class MotorDriver:
    '''!
    This class implements a motor driver for an ME405 kit.
    '''

    _m_ena: 'pyb.Pin'
    _m_pin1: 'pyb.Pin'
    _m_pin2: 'pyb.Pin'
    _m_ch1: 'pyb.Timer.channel'
    _m_ch2: 'pyb.Timer.channel'

    def __init__(
        self, en_pin: str, in1pin: str, in2pin: str, timer: 'pyb.Timer'
            ) -> None:
        '''!
        Creates a motor driver by initializing GPIO
        pins and turning the motor off for safety.
        @param en_pin The pin to which the enable signal
        @param in1pin Counter-clockwise pin ...?
        @param in2pin Clockwise pin ...?
        @param timer The timer to use for PWM
        '''
        # set timer frequency to 20 kHz
        timer.init(freq=20000)

        # activate motor
        self._m_ena = pyb.Pin(en_pin, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)

        self._m_pin1 = pyb.Pin(in1pin, pyb.Pin.OUT_PP)
        self._m_ch1 = timer.channel(1, pyb.Timer.PWM, pin=self._m_pin1)
        self._m_ch1.pulse_width_percent(0)

        self._m_pin2 = pyb.Pin(in2pin, pyb.Pin.OUT_PP)
        self._m_ch2 = timer.channel(2, pyb.Timer.PWM, pin=self._m_pin2)
        self._m_ch2.pulse_width_percent(0)

        self.disable_motor()

    def enable_motor(self):
        '''!
        This method enables the motor.
        '''
        self._m_ena.high()

    def disable_motor(self):
        '''!
        This method disables the motor.
        '''
        self._m_ena.low()

    def set_duty_cycle(self, level: int):
        '''!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
                cycle of the voltage sent to the motor
        '''
        # adjust the duty cycle to be within the range of 0 to 100
        level = max(min(level, 100), -100)
        if level != 0 and abs(level) < 25:
            if level < 0:
                level = -25
            else:
                level = 25
        level = round(level)

        if level > 0:
            self._m_ch1.pulse_width_percent(level)
            self._m_ch2.pulse_width_percent(0)
        # spin clockwise
        elif level < 0:
            self._m_ch1.pulse_width_percent(0)
            self._m_ch2.pulse_width_percent(-level)
        # stop
        else:
            self._m_ch1.pulse_width_percent(0)
            self._m_ch2.pulse_width_percent(0)
