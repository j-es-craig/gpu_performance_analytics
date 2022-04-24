from pickle import TRUE
from tkinter import Y
import matplotlib.pyplot as plot
import numpy as np

def graph_metrics(x):
    x = x[['Timestamp (Elapsed time in seconds)', 'FPS', '99(%) FPS', 'Render Latency(MSec)', 'CPU Utilization(%)', 'GPU1 Utilization(%)', 'GPU1 Temperature(Degrees celsius)','GPU1 Frequency(MHz)', 'GPU1 Fan1 Speed (RPM)']]
    x.plot.line(x = 'Timestamp (Elapsed time in seconds)', subplots = True)
    plot.show(block = False)