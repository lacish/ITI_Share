from enum import Enum

import pandas as pd
import numpy as np
import os


def get_data_csv():
    dir_name = 'C:/Users/sjones8/Downloads/scratchpad/ITI_Share/indicators/gc.dod.totl.gd.zs'
    file_name = 'data.csv'

    # Pull in base data |Country|CountryCode|Year|Value
    base_data = pd.read_csv(os.path.join(dir_name, file_name))

    # capture the original length
    original_length = len(base_data.index)

    # remove lines with all NaN values
    # (pulling from website tends to create empty lines which are
    # represented as NaN when pulled into a dataframe
    no_nan = base_data.dropna(axis=0, how='all')

    new_length = len(no_nan.index)
    # Perform a sanity check on data after NaN removal
    assert(new_length >= original_length/2)

    return no_nan

# transform from readable to much smaller size
# remove country name and abbreviate
# eliminate repeated values etc

# will need to build a tester to verify transform / load is valid
# load will be performed into HDH5


class Country:
    def __init__(self, name, country_code, year, value):
        self.name = name
        self.cc = country_code
        self.year = year
        self.value = value
        # No abbreviation for this country on initialization
        self.short_name = 'UNK'

    def get_enum(self, name):
        pass


def _main():
    no_nans = get_data_csv()

    list_of_country_names = no_nans['Country Name']
    country_list = [Country(name=) for country in list_of_country_names]

    input("Press enter when ready to continue. ")
if __name__ == '__main__':
    _main()


