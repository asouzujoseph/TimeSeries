# TimeSeries

This script makes dataframes from multiple datasets, then stores all the data frames in a dictionary. A user will be prompted to type the name of variables of interests in any or all of the datasets, then the time series subplots for the selected variables are displayed in two formats. 

The first output is based on pandas reseampling function with the options to either downsample, upsample or use the default time interval in the data set. Note that the default time interval in each dataset will be printed to the screen to enable the user to make an informed decision before using the resampling function.

The second output are the plots of the calculated summary statistics on a rolling window of time interval and variables selected by the user.  
