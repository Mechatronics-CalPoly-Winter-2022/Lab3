import time
import serial


def main():
    with serial.Serial('COM5', 115201) as ser:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        kp_list = input('Enter Kp: ').split(',')
        try:
            map(float, kp_list)
        except ValueError:
            print('Kp must be a number.')
            return

        data = []
        for i, kp in enumerate(kp_list):
            ser.write((kp + '\r\n').encode())
            time.sleep(0.1)

            # get rid of the value we just gave it
            ser.readline()

            local_data = [[f'x{i}'], [f'y{i}']]
            while True:
                line: str = ser.readline().decode()
                if line == 'end.\r\n':
                    break
                if ',' in line:
                    line = line.split(',')
                    local_data[0].append(line[0].strip())
                    local_data[1].append(line[1].strip())

            data.append(local_data[0])
            data.append(local_data[1])

        with open('data.csv', 'w') as f:
            for col in zip(*data):
                f.write(','.join(col) + '\n')


if __name__ == '__main__':
    main()
