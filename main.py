import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from scipy import stats



def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2

#Directories
original_data_folder = 'original_data'
new_data_folder = 'data'
figures_folder = 'figures'


#.txt files have an extra space infront of all nan values that needs to be deleted before data can be read into a pandas dataframe with a proper delimiter
for file_name in os.listdir(original_data_folder):
    if file_name not in os.listdir(new_data_folder):
        file = open(original_data_folder+'/'+file_name, mode='rt')
        new_file = open(new_data_folder+'/'+file_name, mode='wt')
        for line in file:
            new_file.write(line.replace('  ', ' ',))
        file.close()
        new_file.close()
    else:
        pass


#Read correctly delimited .txt files into Pandas DataFrames with proper column names
for file_name in os.listdir(new_data_folder):
    df = pd.read_csv(new_data_folder+'/'+file_name,
                     sep=' ',
                     names=['YEAR','MONTH','DAY','PREC','PRCP',
                            'TMAX','TMIN','TAVG','WTEQ'])

    #Threshold air temperature measurements
    df[df['TMAX'] > 120] = np.nan
    df[df['TMAX'] < -120] = np.nan
    df[df['TAVG'] > 120] = np.nan
    df[df['TAVG'] < -120] = np.nan
    df[df['TMIN'] > 120] = np.nan
    df[df['TMIN'] < -120] = np.nan


    #Plot regression line between x and y
    x = df['TAVG']
    y = df['TMAX']
    sb.jointplot(x, y, kind="reg", stat_func=r2)
    plt.savefig(figures_folder + '/' + file_name.strip('.txt') + '.png')
    plt.clf()
