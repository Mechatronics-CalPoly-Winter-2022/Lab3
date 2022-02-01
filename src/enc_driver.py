"""! 
@brief Offers functionality that enables reading the current position of
the motor in encoder tics. 
"""

import pyb      # import the micropy library


class EncoderConfig:
    '''!
    This class is a container for the encoder configuration.
    '''
    args: tuple

    def __init__(self, pin1: str, pin2: str, timer: 'pyb.Timer') -> None:
        '''!
        Creates an encoder configuration by saving the pins and timer.
        @param pin1 The pin to which the encoder's pin1 is connected
        @param pin2 The pin to which the encoder's pin2 is connected
        @param timer The timer to use for the encoder
        '''
        self.args = (pin1, pin2, timer)


class EncoderDriver:
    '''!
    This class implements an encoder driver for an ME405 kit.
    '''

    MAX_VAL: int = 34464

    _e_pin1: 'pyb.Pin'
    _e_pin2: 'pyb.Pin'
    _e_tim: 'pyb.Timer'
    _e_ch1: 'pyb.Timer.channel'
    _e_ch2: 'pyb.Timer.channel'

    def __init__(self, enc_1: str, enc_2: str, timer: 'pyb.Timer') -> None:
        '''!
        Creates an encoder driver by initializing GPIO pins
        @param enc_1 The pin to which the first encoder signal
        @param enc_2 The pin to which the second encoder signal
        @param timer The timer to use for the encoder
        '''
        # setup the timer for quadrature decoding
        self._e_tim = timer
        self._e_tim.init(prescaler=1, period=100000)

        # setup the pins for quadrature decoding
        self._e_pin1 = pyb.Pin(enc_1, pyb.Pin.AF_PP)
        self._e_pin2 = pyb.Pin(enc_2, pyb.Pin.AF_PP)

        # setup the channels for quadrature decoding
        self._e_ch1 = self._e_tim.channel(1, pyb.Timer.ENC_A, pin=self._e_pin1)
        self._e_ch2 = self._e_tim.channel(2, pyb.Timer.ENC_B, pin=self._e_pin2)

    def read(self) -> int:
        '''!
        This method returns the current count of the encoder.
        @return The current count of the encoder
        '''
        return self._e_tim.counter()

    def zero(self) -> None:
        '''!
        This method resets the encoder's count to 0.
        '''
        self._e_tim.counter(0)

    def get_error(self, setpoint: int) -> int:
        '''!
        This method returns the error between the count and the setpoint
        @param setpoint The setpoint to compare the count to
        @return The error between the current count and the setpoint
        '''
        right = setpoint - self.read()
        if right < 0:
            right += self.MAX_VAL  # account for rollover

        left = self.read() - setpoint
        if left < 0:
            left += self.MAX_VAL

        return right if right <= left else -left
