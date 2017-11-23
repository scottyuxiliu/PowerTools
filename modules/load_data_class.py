import csv
import math
import numpy as np
import pandas as pd
import os
import re


class LoadData:
    def __init__(self):
        self.num_true = -3
        self.num_false = 0

    def loadcsv(self, csvPath):
        df = pd.read_csv(csvPath,na_values=['.'],dtype=np.float)
        # df = df.astype(np.float)
        return df

    def savedf2h5(self, df, h5Path):
        df.to_hdf(h5Path, self.TABLE_NAME)

    def genh5_y_n_day_col_name(self, df, n_day, col_name):
        df['y']=df[col_name].shift(-n_day)
        df=df[:-n_day]
        return df

    def loadh5(self, h5Path):
        """ Load h5 df table
        """
        with pd.HDFStore(h5Path, "r") as hfdata:
            df = hfdata.get(self.TABLE_NAME)
        return df

    def process_raw_data(self,raw_csv_path):
        self.__read_formulas(raw_csv_path)
        # df = pd.read_csv(raw_csv_path,na_values=['.'],skiprows=38)
        # df.drop(df.columns[0],axis=1,inplace=True) #axis=0 along rows, axis=1 along columns
        # df = df.set_index(df.columns[0])
        # print(df.shape)
        # print(df.head(5))
        return 0

    def __read_formulas(self,raw_csv_path):
        df = pd.read_csv(raw_csv_path, na_values=['.'], skiprows=1, nrows=1)
        print(df)
        return 0
