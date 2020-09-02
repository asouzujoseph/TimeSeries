#!/usr/bin/env python
'''
Author : Nnamdi Asouzu
'''
# coding: utf-8

import pandas as pd
import glob
import os
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from IPython.display import display
import matplotlib.cm as mpl_cm
import matplotlib.colors as mpl_colors
import matplotlib.pylab as pl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm
import random
get_ipython().run_line_magic('matplotlib', 'inline')


# Codes for concatenation of excel files as dataframes

'''this function will create a DateTime column in the dataframes'''
def UTCFormat (DF):
    if ("Time" in DF.columns):
        DF['Datetime'] = pd.to_datetime(DF['Date'] +' '+ DF['Time'],dayfirst = True)
        DF = DF.drop(['Date','Time'], axis=1)
        DF = DF.set_index('Datetime').sort_index()
        DF = DF.dropna()
    elif ('Time PC' in DF.columns):
        DF['Datetime'] = pd.to_datetime(DF['Date'] +' '+ DF['Time PC'],dayfirst = True)
        DF = DF.drop(['Date','Time PC'], axis=1)
        DF = DF.set_index('Datetime').sort_index()
        DF = DF.dropna()
    return DF

'''this function will make a dataframe of each file and all DFs as a dictionary with the name of the file as key''' 
def combineFiles (path): 
    bag = {}    # empty dictionary for storing dataframes
    files = glob.glob(path,recursive = True) # function to read all files even in subfolders
    for file in files: 
        xls = pd.ExcelFile(file)     # read excel file as a data frame
        if ("week 1" in xls.sheet_names): # condition to ensure that the file contains useful data
            df1 = pd.read_excel(xls, 'week 1')  # read each sheet as a data frame
            df2 = pd.read_excel(xls, 'week 2')
            df3 = pd.read_excel(xls, 'week 3')
            df4 = pd.read_excel(xls, 'week 4')
            df5 = pd.read_excel(xls, 'week 5')
            df6 = pd.read_excel(xls, 'week 6')
            filename = file.split('\\') # make a filename to act as key in the dictionary
            name = filename[-1]
            name2 = name.split('.')
            nameDF = name2[0]
            DF = pd.concat([df1,df2,df3,df4,df5,df6],axis =0) # concatenate the data frames into one mega data frame
            DF2 = UTCFormat(DF) # call function to create DateTime columns
            bag[nameDF] = DF2 # add the dataframe to the dictionary
    return bag

# Codes for data visualization
'''this function will set the background color to either light or dark'''
def set_custom_plot_colors(mode='dark'):
    from  matplotlib import rc as set_mtpl_sytle  
    if mode=='dark':  # an alternative is "white"
        ax_facecolor= '#3f3f3f'
        grid_color= '#4c4c4c'

    elif mode=='light':
        ax_facecolor='#d3d3d3'
        grid_color= '#f2f2f2'
    plt.style.use('default')
    set_mtpl_sytle('axes', edgecolor='white', labelcolor='white', facecolor=ax_facecolor,grid=True, axisbelow=True)
    set_mtpl_sytle('grid', color=grid_color)
    set_mtpl_sytle('xtick', color='#f2f2f2')
    set_mtpl_sytle('ytick', color='#f2f2f2')
    #set_mtpl_sytle('figure', facecolor='#2b2b2b')
    set_mtpl_sytle('figure', facecolor='#121212')
    
'''this is the main settings for the plots'''
def plot_variables_main_ax(ax_,ds_data,ax_label,title,ax_color,lb_color,set_bottom=False):
#ax_ = selected axis index, ds_data = data point (time data)
    ax_.plot(ds_data.index.to_pydatetime(),ds_data, color=ax_color, marker = '.' ,markerfacecolor= ax_color,linewidth=1.5) # convert to dateTime format
    if set_bottom: ## sets the lowest point to zero, it is preferable to let the software decide
        ax_.set_ylim(bottom=0) 
    ax_.set_ylabel(ax_label,fontsize=16,color=ax_color,labelpad=45,rotation=90) #makes the y label bold
    ax_.tick_params(axis='y', colors=ax_color,labelsize=13) # arranges the tick of the plots
    ax_.grid(False) #removes grid
    ax_.xaxis.set_major_locator(mdates.DayLocator(interval=1)) # determines the interval (set the basis)
    ax_.xaxis.set_major_formatter(mdates.DateFormatter('%b %d')) # determines how the values show in the graph
    ax_.xaxis.grid(True, which="major") # sets only the x axis
    ax_.xaxis.set_tick_params(rotation=90,color=lb_color) # controls the position of the x axis labels
    ax_.tick_params(axis='x', color=lb_color)
    ax_.set_title(title, color = lb_color)
   
'''this function is useful if there is need to combine two variables in a plot '''   
def plot_variables_secondary_ax(ax_,ds_data,ax_label,ax_color,ax_alpha,lb_color):
    ax_.plot(ds_data.index.to_pydatetime(),ds_data,color=ax_color,linewidth=1.5)
    ymin, ymax = ax_.get_ylim() # get the minimum point
	# fill the secondary plot starting from the minimum of each plot
    ax_.fill_between(ds_data.index.to_pydatetime(), ymin, ds_data, facecolor=ax_color, alpha=ax_alpha)
    ax_.grid(False)
    ax_.tick_params(axis='y',colors=ax_color,labelsize=13) 
    ax_.set_ylabel(ax_label,fontsize=16,color=ax_color,rotation=90,labelpad=45)
    ax_.tick_params(colors=ax_color)
    ax_.xaxis.set_major_locator(mdates.DayLocator(interval=1)) 
    ax_.xaxis.set_major_formatter(mdates.DateFormatter('%b %d')) 
    ax_.xaxis.grid(True, which="major")
    ax_.xaxis.set_tick_params(rotation=90,color=lb_color)
    ax_.tick_params(axis='x', color=lb_color) 
    
'''this function will collect user's choice and store in a list'''
def variables ():
    var_list = []
    for i in range(0, 5): # set up loop to run 5 times
        variable = str(input('Please type name of a variable or press enter to skip (max of 5 variables): ')).strip().lower()
        var_list.append(variable) 
    var_list[:] = [item for item in var_list if item != '']
    return var_list
    
   
'''this function is the main plotting function'''
def plot_variables(df_,var_list,uniqName, start_date=None,end_date=None,lb_color='white',fig_length=22):
    # get the all variables in the DF
    available_var_list = list(df_.columns)
    #     Check the available variables that will be plotted (if allowed)
    # 	i.e check if the requested variables are present in the dataframe. if true add to a new list
    plot_var_list = []
    for var in var_list:
        if var in available_var_list:
            plot_var_list.append(var)
            
    # select the plot period
    if start_date is None:
        plt_start_date = df_.index[0]
    else:
        plt_start_date = start_date
    if end_date is None:
        plt_end_date = df_.index[-1]
    else:
        plt_end_date = end_date
    df = df_[start_date:end_date] # select only the chosen time periods in the DF
    
    # Define Figure
    row_num = len(plot_var_list) # equals the number of items in the list
    fig, ax = plt.subplots(nrows=row_num, ncols=1,sharex=True,figsize=(fig_length,row_num*3),dpi=150)
    indx = -1  # addition of 1 will set the first ax to zero (zero indexed coding)    
    count = 0
    colors = ['lime',"deepskyblue",'fuchsia',"y",'orange','blueviolet','c','g','m','deeppink','gold','crimson',"brown","aqua"]    
    for col,val in zip(colors,plot_var_list):
        indx = indx + 1
        var_main = val
        color_main = colors[count]   #[random.randint(0,10)]
        lb = val.split()
        lb_main = val[0:14] 
        title = val
        if row_num>1:  
            ax1 = ax[indx]
        else:
            ax1 = ax 
        plot_variables_main_ax(ax1,df[var_main],lb_main,title,color_main,lb_color)
        plt.tight_layout()
        fig = plt.gcf()
        count = count + 1
        fig.savefig('../Desktop/roundOneResults/' + uniqName + '.png', bbox_inches='tight',dpi=fig.dpi,facecolor=fig.get_facecolor(), edgecolor='none')     

'''this function will create a backup CSV file of the concatenated unprocessed data''' 
def RDTeam (dataFrames):
    roundOneDF = pd.concat([v.reset_index(drop=False) for k,v in dataFrames.items()], axis= 1, keys=[name for name in dataFrames.keys()], ignore_index=False)
    roundOneDF.to_csv('../Desktop/roundOneResults/roundOneDF22bbb.csv',index=False) #write to csv file    
    return roundOneDF

## code for resampling data
'''this function will visualize the resampled data'''
def vizResampled (dataFrames):
    for key,df in dataFrames.items():
        df['deltaT'] = df.index.to_series().diff().dt.seconds.div(60, fill_value=0)  ## find the time interval in each data frame
        df = df.loc[:, ~df.columns.duplicated()]  # remove duplicate columns
        print (key + " data has time interval of " + str(round(df.iloc[5,-1],1)) + " minutes ")  # print the time interval
        print ("   ")
    varTime = str(input("Please put in a desired time resolution for variable of interest . For instance, 30S, 5min, 1H, etc : ")) # ask for user input
    var_list = variables()   
    for key,df in dataFrames.items(): # loop through the data frames
        df.columns = map(str.lower, df.columns)  # convert all the column headings to lower case
        df = df.resample(varTime).first()  # resample and do not fill missing values with NaN (this allows detection of missing data)
        plot_variables(df,var_list,start_date=None,end_date=None,lb_color='white', fig_length=22, uniqName = key+'_resampled_'+datetime.today().strftime('%Y-%m-%d'))


## code for summary statistics on rolling window
''' this function will visualize the rolling function'''  
def vizRolling (dataFrames):
    varTime = str(input("Please type in the time period. For instance, 30S, 5min, 1H, etc : ")) 
    varStats = str(input("Please select a summary statistics.For instance, max, min, mean,sum, var, std etc. : ")) 
    var_list = variables()
    for key,df in dataFrames.items():
        df.columns = map(str.lower, df.columns)
        df = df.loc[:, ~df.columns.duplicated()]
        if varStats == 'sum':
            df = df.rolling(varTime).sum()
            plot_variables(df,var_list,start_date=None,end_date=None,lb_color='white', fig_length=22,uniqName = key+'_rolling_'+datetime.today().strftime('%Y-%m-%d'))

        elif varStats == 'mean':
            df = df.rolling(varTime).mean()
            plot_variables(df,var_list,start_date=None,end_date=None,lb_color='white', fig_length=22,uniqName = key+'_rolling_'+datetime.today().strftime('%Y-%m-%d'))

        elif varStats == 'max':
            df = df.rolling(varTime).max()
            plot_variables(df,var_list,start_date=None,end_date=None,lb_color='white', fig_length=22,uniqName = key+'_rolling_'+datetime.today().strftime('%Y-%m-%d'))

        elif varStats == 'min':
            df = df.rolling(varTime).min()
            plot_variables(df,var_list,start_date=None,end_date=None,lb_color='white', fig_length=22,uniqName = key+'_rolling_'+datetime.today().strftime('%Y-%m-%d'))

        elif varStats == 'std':
            df = df.rolling(varTime).std()
            plot_variables(df,var_list,start_date=None,end_date=None,lb_color='white', fig_length=22,uniqName = key+'_rolling_'+datetime.today().strftime('%Y-%m-%d'))

        elif varStats == 'var':
            df = df.rolling(varTime).var()
            plot_variables(df,var_list,start_date=None,end_date=None,lb_color='white', fig_length=22,uniqName = key+'_rolling_'+datetime.today().strftime('%Y-%m-%d'))


### call functions			
path = r'C:/Users/Nnamdi/Desktop/data/**/*.xlsx'
dataFrames = combineFiles (path)
set_custom_plot_colors(mode='dark')
RDTeam (dataFrames)
vizResampled(dataFrames)
vizRolling (dataFrames)





