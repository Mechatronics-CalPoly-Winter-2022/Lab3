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
import utime
from enc_driver import EncoderConfig
from motor_driver import MotorConfig
from servo import Servo
from pid import PID


def motor_test(servo: Servo, pid: PID):
    """!
    Task which puts things into a share and a queue.
    """
    # initialize encoder and time data lists
    encoder_data = []
    time_data = []
    
    state = 'running'
    flag = False
    pid.set_setpoint(servo.read() + 17232)

    while True:
        if state == 'running':
            print(pid.setpoint, end=', ')
            servo.enable_motor()
            timeout = utime.ticks_add(utime.ticks_ms(), 6000)
            while utime.ticks_diff(timeout, utime.ticks_ms()) > 0:
                # get the error and adjust the duty cycle
                servo.set_duty_cycle(pid.update(servo.get_error(pid.setpoint)))
                
                print(servo.get_error(pid1.setpoint))

                # get the encoder data and time data
                encoder_data.append(servo.read())

                time_data.append(utime.ticks_add(utime.ticks_ms(), 0))
                
                yield(0)
            
            print(servo.read())
            servo.disable_motor()
            
            if flag is True:
                state = 'print'
            else:
                state = 'inter'
                
        elif state == 'inter':
            flag = True
            pid.set_setpoint(servo.read() + 17232)
            state = 'running'
            
        elif state == 'print':
            # reduce every element in time_data by the first element
            time_data = [x - time_data[0] for x in time_data]

            # print the encoder data and time data
            for i in range(len(encoder_data)):
                print(servo.name, ': ', time_data[i], ',', encoder_data[i])
                yield(0)
                
            state = 'stopped'
            
        elif state == 'stopped':
            pass
            
        yield(0)


def task1_fun ():
    global servo1
    global pid1
    yield motor_test(servo1, pid1)

def task2_fun ():
    global servo2
    global pid2
    yield motor_test(servo2, pid2)


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')

    # initialize the encoder and motor drivers
    m_config = MotorConfig('PA10', 'PB4', 'PB5', pyb.Timer(3))
    e_config = EncoderConfig('PC6', 'PC7', pyb.Timer(8))

    # initialize the servo
    servo1 = Servo('servo1', m_config, e_config)
    servo1.zero()
    
    pid1 = PID(0, 34434, kp = float(input('Input Kp: ')))
    
    servo2 = None
    pid2 = None

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (task1_fun, name = 'Task_1', priority = 1, 
                         period = 10, profile = True, trace = False)
    
    #task2 = cotask.Task (task2_fun, name = 'Task_2', priority = 1, 
    #                     period = 10, profile = True, trace = False)
    
    cotask.task_list.append(task1)
    #cotask.task_list.append (task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP()
    
    vcp.read )
    
    while not vcp.any():
        cotask.task_list.pri_sched()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read()

    # Print a table of task data and a table of shared information data
    print('\n' + str(cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('\r\n')
