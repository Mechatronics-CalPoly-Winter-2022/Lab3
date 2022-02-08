'''!
@brief This file communicates with the microcontroller over serial
in order to receive, parse, and print the data that is printed out 
in main.py
'''

import time
import serial
import matplotlib.pyplot as plt


def main():
    with serial.Serial('COM5', 115200) as ser:
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        try:
            kp = float(input('Enter Kp: '))
            period = float(input('Enter period: '))
        except ValueError:
            print('Invalid input, exiting')
            return

        data: list = [[], [], []]
        ser.write((str(kp) + '\r\n').encode())
        ser.write((str(period) + '\r\n').encode())
        time.sleep(0.1)

        # get rid of the value we just gave it
        ser.readline()

        while True:
            line: str = ser.readline().decode()
            if line == 'end.\r\n':
                break
            if ',' in line:
                name, meat = line.split(':')[0].strip(), line.split(':')[1].strip()
                meat = list(map(str.strip, meat.split(',')))
                data[0].append(name)
                data[1].append(meat[0])
                data[2].append(meat[1])

        servo1 = [[], []]
        servo2 = [[], []]
        for i in range(len(data[0])):
            if data[0][i] == 'servo1':
                servo1[0].append(float(data[1][i]))
                servo1[1].append(float(data[2][i]))
            if data[0][i] == 'servo2':
                servo2[0].append(float(data[1][i]))
                servo2[1].append(float(data[2][i]))

        figure, axis = plt.subplots(2, 1)

        axis[0].plot(servo1[0], servo1[1])
        axis[0].set_title('Servo 1')
        axis[0].set_xlabel('Time (s)')
        axis[0].set_ylabel('Position (Ticks)')

        axis[1].plot(servo2[0], servo2[1])
        axis[1].set_title('Servo 2')
        axis[1].set_xlabel('Time (s)')
        axis[1].set_ylabel('Position (Ticks)')

        plt.show()


if __name__ == '__main__':
    main()
