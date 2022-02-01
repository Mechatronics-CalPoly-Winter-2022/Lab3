class PID:
    '''!
    Class that implements a PID controller.
    '''

    setpoint: int
    kp: float
    ki: float
    kd: float
    prev_error: int
    integral: int

    def __init__(
        self, setpoint: int, kp: float = 0.08, ki: float = 0, kd: float = 0
            ) -> None:
        '''!
        Creates a PID object.
        @param setpoint The desired setpoint
        @param kp The proportional gain
        @param ki The integral gain
        @param kd The derivative gain
        '''
        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.prev_error = 0
        self.integral = 0

    def set_setpoint(self, new: int) -> None:
        '''!
        Sets the new setpoint.
        @param new The new setpoint
        '''
        self.setpoint = new

    def set_proportional_gain(self, new: float) -> None:
        '''!
        Sets the proportional gain.
        @param new The new proportional gain
        '''
        self.kp = new

    def update(self, error: int) -> int:
        '''!
        Updates the PID controller.
        @param error The current error
        @return The new duty cycle
        '''
        # calculate the proportional term
        p = self.kp * error

        # calculate the integral term
        self.integral += error
        i = self.ki * self.integral

        # calculate the derivative term
        d = self.kd * (error - self.prev_error)
        self.prev_error = error

        # return the PID output
        return p + i + d

    def print_data(self, encoder_data: list, time_data: list) -> None:
        '''!
        Prints the data of the encoder and time.
        @param encoder_data The encoder data
        @param time_data The time data
        '''
        min_length = min(len(encoder_data), len(time_data))
        for i in range(min_length):
            print(f'{time_data[i]},{encoder_data[i]}')

        print('end.')
