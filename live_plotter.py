import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd
# from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication
from numpy import average

zero_offset = 0

fig = plt.figure()
# creating a subplot
ax1 = fig.add_subplot(1, 1, 1)

file_name = 'C:/TEMP/trial1.csv'
test_name = 'Clamp_Force_Test'


# def select_file():
#     w = QWidget()
#     w.resize(320, 240)
#     w.setWindowTitle("Select CSV for reading")
#     filename, _ = QFileDialog.getOpenFileName(w, 'Open File', '/var/log/ethicon/loki/DEMDAQ/')
#     # sys.exit(a.exec_())
#
#     return filename


def tare_data_values(data_frame, num_points=100):
    match = False

    while not match:
        tare_data_max = max(data_frame[:num_points])
        tare_data_min = min(data_frame[:num_points])
        if abs(tare_data_max - tare_data_min) < 0.1:
            match = True
        else: num_points = num_points / 2

    tare_data_av = average(data_frame[:num_points])

    return tare_data_av


def animate(i):
    plot_length = 50000
    data = open(file_name, 'r').read()

    xs = []
    ys = []

    lines = data.split('\n')

    header = True

    try:
        for line in lines:
            if not header:
                x, y = line.split(',')  # Delimiter is comma
                xs.append(float(x))
                ys.append(float(y))
            else:
                header = False
    except ValueError:
        pass

    ax1.clear()

    global zero_offset

    if zero_offset == 0:
        panda_ys = pd.DataFrame(ys)
        zero_offset = tare_data_values(panda_ys)
        panda_ys = panda_ys - zero_offset
        tared_ys = panda_ys.values.tolist()
    else:
        ys[:] = [x - zero_offset for x in ys]
        tared_ys = ys

    if len(tared_ys) < plot_length:
        plot_length = len(tared_ys)
    # ax1.plot(tared_ys[-plot_length:])
    ax1.plot(ys)


    # Issue somewhere in either Python 3 to Python 2, or syntax, animation should
    # be displaying
    plt.xlabel('Sample Time')
    plt.ylabel('Force (N)')
    plt.title('Live graph with matplotlib')


def _main():
    global file_name
    # file_name = select_file()

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()


if __name__ == '__main__':
    _main()
