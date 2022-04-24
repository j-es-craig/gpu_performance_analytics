from pickle import TRUE
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
import PySimpleGUI as sg

def summary_statistics(x):
    minFPS = str(x.iloc[:,1].min())
    maxFPS = str(x.iloc[:,1].max())
    avgFPS = str(round(x.iloc[:,1].mean()))
    avg99FPS = str(round(x.iloc[:,2].mean()))
    
    layout = [
    [sg.Text("")],
    [sg.Text("min FPS = " + minFPS), sg.Text("")],
    [sg.Text("max FPS = " + maxFPS), sg.Text("")],
    [sg.Text("avg FPS = " + avgFPS), sg.Text("")],
    [sg.Text("average (99%) FPS = " + avg99FPS), sg.Text("")],
    [sg.Text("")]
    ]

    window = sg.Window('Summary Statistics', layout)
    event, values = window.read()

def frame_stutter(x):
    print(x)