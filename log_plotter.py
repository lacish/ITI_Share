import pandas as pd
import os
from matplotlib.pyplot import plot, show, draw, pause
from numpy import average


def plot_csv_data(log_path, file_name, test_name):
    """Simple function that plots csv data"""
    data = pd.read_csv(os.path.join(log_path, file_name))
    plot_data = data[test_name]
    plot(plot_data)
    show(block=False)

    final_data = plot_data - (tare_data_vals(plot_data))

    plot(final_data)
    show()
    pass


def tare_data_vals(data_frame, num_points=100):
    match = False

    while not match:
        tare_data_max = max(data_frame[:num_points])
        tare_data_min = min(data_frame[:num_points])
        if abs(tare_data_max - tare_data_min) < 0.1:
            match = True
        else:
            num_points = num_points / 2

    tare_data_av = average(data_frame[:num_points])

    return tare_data_av


def _main():
    plot_csv_data("C:/Users/sjones8/rtc_logs/", 'Clamp_Force_Test__2019-06-10T10-09-27_1.csv', 'Clamp_Force_Test')


if __name__ == '__main__':
    _main()
