import csv
import random
import time


def create_csv(output_path='C:/TEMP/trial1.csv'):
    """Generates a semi-random CSV file for plotting
    Currently creating empty line for first line sometimes.
    Will also want to start automatically creating a header
    entitled A / B for now"""
    random.seed()
    i = 0
    while True:
        x_column = 1
        y_column = 5
        x_column += random.random()
        y_column += random.random()
        csv_output=[x_column, y_column]

        with open(output_path, 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(csv_output)
        i += 1
        if i > 100:
            time.sleep(1)
            print("Use Ctrl+C or the stop button to stop creating random data. ")
            i = 0


def _main():
    create_csv()


if __name__ == '__main__':
    _main()


