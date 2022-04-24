import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
import PySimpleGUI as sg

# sample data to test functions
mydata = pd.read_csv('./data/GeForce_Experience_Performance_Data_2022-04-09T10-08-15.csv')
mydf = pd.DataFrame(mydata)
mydf = mydf[['Timestamp (Elapsed time in seconds)', 'FPS', '99(%) FPS', 'Render Latency(MSec)', 'CPU Utilization(%)', 'GPU1 Utilization(%)', 'GPU1 Temperature(Degrees celsius)',
'GPU1 Frequency(MHz)', 'GPU1 Fan1 Speed (RPM)']] 


# functions for to find stutters, and the values of other metrics when stutters occur. 
def diff_list(fps_window):
    diffs = []

    for i in range(1, len(fps_window)):
        diffs.append(fps_window[1] - fps_window[i-1])

    sig_diffs = [i for i in diffs if abs(i) >= 2]

    if not sig_diffs:
        return(False)
    else:
        return(True)

# return window indices at which stutters occur
def frame_stutter(seq, window_size, column):

    seq_list = seq[column].values.tolist()
    windows = []
    indices = []

    for i in range(len(seq_list) - window_size + 1):
        windows.append(seq_list[i: i + window_size])
    
    for i in range(1, len(windows)):
        if diff_list(windows[i]) == True:
            indices.append(i)   #([i, fps_windows[i]])
    
    return(indices)

# slide thru other metrics to determine values at stutter loci
def frame_stutter_cause(seq, window_size, column):

    seq_list = seq[column].values.tolist()
    windows = []
    index_and_values = []

    for i in range(len(seq_list) - window_size + 1):
        windows.append(seq_list[i: i + window_size])

    for i in range(1, len(windows)):
        index_and_values.append(windows[i])
    
    return(index_and_values)

print(frame_stutter(mydf, 5, 'FPS'))
print(frame_stutter_cause(mydf, 5, 'GPU1 Utilization(%)'))
#print(diff_list([60.0, 59.0, 59.0, 57.0, 59.0]))