"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2.
"""

import gc
import pyb
import cotask
import task_share
from task_share import Share
import utime
from enc_driver import EncoderConfig
from motor_driver import MotorConfig
from servo import Servo
from pid import PID


def motor_test(servo: Servo, pid: PID, self_done: Share, other_done: Share):
    """!
    Task which puts things into a share and a queue.
    """
    # initialize encoder and time data lists
    encoder_data = []
    time_data = []

    state = 'running'
    pid.set_setpoint(servo.read() + 17232)

    while True:
        if state == 'running':
            servo.enable_motor()
            timeout = utime.ticks_add(utime.ticks_ms(), 1500)
            while utime.ticks_diff(timeout, utime.ticks_ms()) > 0:
                # get the error and adjust the duty cycle
                servo.set_duty_cycle(pid.update(servo.get_error(pid.setpoint)))

                # get the encoder data and time data
                encoder_data.append(servo.read())

                time_data.append(utime.ticks_ms())

                yield(0)

            servo.disable_motor()

            state = 'print'

        elif state == 'print':
            # reduce every element in time_data by the first element
            # not doing this cause RAM

            # print the encoder data and time data
            for i in range(len(encoder_data)):
                print(servo.name, ': ', time_data[i], ',', encoder_data[i])
                yield(0)

            state = 'stopped'

        elif state == 'stopped':
            if other_done.get() == 1:
                self_done.put(1)
                print('end.')
                while True:
                    yield(0)
            else:
                self_done.put(1)
            pass

        yield(0)


def task1_fun():
    global servo1
    global pid1
    print('running 1')
    tester = motor_test(servo1, pid1, one_done, two_done)
    while True:
        yield next(tester)


def task2_fun():
    global servo2
    global pid2
    tester = motor_test(servo2, pid2, two_done, one_done)
    print('running 2')
    while True:
        yield next(tester)


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    while True:
        print('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
            'Press ENTER to stop and show diagnostics.')

        kp = float(input('Enter Kp: '))
        period = float(input('Enter period: '))

        # initialize the encoder and motor drivers
        m_config = MotorConfig('PA10', 'PB4', 'PB5', pyb.Timer(3))
        e_config = EncoderConfig('PC6', 'PC7', pyb.Timer(8))

        # initialize the servo
        servo1 = Servo('servo1', m_config, e_config)
        servo1.zero()

        pid1 = PID(34434, kp=kp)

        m_config = MotorConfig('PC1', 'PA0', 'PA1', pyb.Timer(5))
        e_config = EncoderConfig('PB6', 'PB7', pyb.Timer(4))

        servo2 = Servo('servo2', m_config, e_config)
        servo2.zero()

        pid2 = PID(34434, kp=kp)

        # Create the tasks. If trace is enabled for any task, memory will be
        # allocated for state transition tracing, and the application will run out
        # of memory after a while and quit. Therefore, use tracing only for
        # debugging and set trace to False when it's not needed
        one_done = Share('i')
        one_done.put(0)
        task1 = cotask.Task(task1_fun, name='Task_1', priority=1,
                            period=period, profile=True, trace=False)

        two_done = Share('i')
        two_done.put(0)
        task2 = cotask.Task(task2_fun, name='Task_2', priority=1,
                            period=period, profile=True, trace=False)

        cotask.task_list.append(task1)
        cotask.task_list.append(task2)

        # Run the memory garbage collector to ensure memory is as defragmented as
        # possible before the real-time scheduler is started
        gc.collect()

        # Run the scheduler with the chosen scheduling algorithm. Quit if any
        # character is received through the serial port
        vcp = pyb.USB_VCP()

        vcp.read()

        try:
            while not vcp.any():
                cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            servo1.disable_motor()
            servo2.disable_motor()
            break

        # Empty the comm port buffer of the character(s) just pressed
        vcp.read()

        # Print a table of task data and a table of shared information data
        print('\n' + str(cotask.task_list))
        print(task_share.show_all())
        print(task1.get_trace())
        print('\r\n')
