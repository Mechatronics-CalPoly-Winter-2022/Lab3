"""! 
@brief A class that inherits from both the MotorDriver and 
EncoderDriver classes. Offers full functionality from both classes.
"""

from enc_driver import EncoderDriver, EncoderConfig
from motor_driver import MotorDriver, MotorConfig


class Servo(MotorDriver, EncoderDriver):
    '''!
    Class that combies the functionality of the encoder and motor drivers.
    '''

    gain: float
    name: str

    def __init__(self, name: str, m_config: MotorConfig, e_config: EncoderConfig) -> None:
        '''!
        Creates a servo object by initializing the motor and encoder drivers.
        @param m_config The motor configuration
        @param e_config The encoder configuration
        '''
        self.name = name
        MotorDriver.__init__(self, *m_config.args)
        EncoderDriver.__init__(self, *e_config.args)
