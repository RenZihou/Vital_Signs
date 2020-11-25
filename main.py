# -*- encoding: utf-8 -*-
# @Author: RZH

import pandas as pd

from src.data_process import data_process
from src.plot import plot


def main(reporter_file: str = './data/reporter-export.csv'):
    data = pd.read_csv(reporter_file)
    data = data_process(data)
    plot(data)
    return None


if __name__ == '__main__':
    main()
    pass
