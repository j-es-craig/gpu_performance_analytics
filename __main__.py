#!/usr/bin/env python
from lib2to3.pgen2.pgen import DFAState
import PySimpleGUI as sg
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from analysis import *

# Show CSV data in Table
sg.theme('Reddit')

menu_def = [
            ['Analyses', ['Summary', 'Frame Stutter', 'Graphs']],
            #['Graphs2', ['FPS', 'GPU Utilization', 'CPU Utilization', 'GPU Temps']]
            ]

def metrics_table():
    filename = sg.popup_get_file('filename to open', no_window=True, file_types=(("CSV Files","*.csv"),))
    # --- populate table with file contents --- #
    if filename == '':
        return
    global df
    df = []    
    data = []
    header_list = []
    button = sg.popup_yes_no('Confirm?')
    if filename is not None:
        with open(filename, "r") as infile:
            reader = csv.reader(infile)
            if button == 'Yes':
                header_list = next(reader)
                header_list = [e for e in header_list if e not in ('PID', 'Average PC Latency(MSec)', 'GPU1 Fan2 Speed (RPM)', 'GPU2 Temperature(Degrees celsius)', 'GPU2 Frequency(MHz)', 'GPU2 Memory Frequency(MHz)', 'GPU2 Voltage(Milli Volts)', 'GPU2 Fan1 Speed (RPM)', 'GPU2 Fan2 Speed (RPM)', 'GPU2 Utilization(%)', '')]

            try:
                data = list(reader) # read everything else into a list of rows

                a = data
                a = np.delete(a, [1, 5, 13, 14, 15, 16, 17, 18, 19, 20], axis = 1)

                df = pd.read_csv(filename, skipinitialspace=True)
                df = pd.DataFrame(df.loc[:, df.columns != 'PID'])

                if button == 'No':
                    window.close()
                    #header_list = ['column' + str(x) for x in range(len(data[0]))]
            except:
                sg.popup_error('Error reading file')
                return
    sg.set_options(element_padding=(0, 0))

    layout = [
        [sg.Menu(menu_def, text_color = "black", font = "SYSTEM_DEFAULT", pad=(10,10))],
        [sg.Table(values=a, # note edit to a
            headings=header_list,
            max_col_width=1, # unsure how this scales exactly
            auto_size_columns=False, # true makes columns the size of their header
            justification='right',
            # alternating_row_color='lightblue',
            num_rows=min(len(a), 20))] # note edit a
        ]


    window = sg.Window('Table', layout, grab_anywhere=False)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        elif event == 'Summary':
            summary_statistics(df)
        elif event == 'Frame Stutter':
            frame_stutter(df)
        elif event == "Graphs":
            graph_metrics(df)

    window.close()

def popup_text(filename, text):

    layout = [
        [sg.Multiline(text, size=(80, 25)),],
    ]
    win = sg.Window(filename, layout, modal=True, finalize=True)

    while True:
        event, values = win.read()
        if event == sg.WINDOW_CLOSED:
            break
    win.close()

main_page_elements = [ # could be layout = ...
    [sg.Text("")],
    [sg.Button('Choose File'),
    sg.Cancel(),
    sg.Button('README')],
    [sg.Text("")]
]

layout = [ # try to make resizeable 
    [sg.VPush()],
    [sg.Push(), sg.Column(main_page_elements, element_justification='c'), sg.Push()],
    [sg.VPush()]
]

window = sg.Window('Nvidia Performance Analytics', layout, size = (500,300))

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == 'Choose File':
        metrics_table()
    elif event == 'README':
        filename = 'README.txt'
        if Path(filename).is_file():
            try:
                with open(filename, 'rt', encoding = 'utf-8') as f:
                    text = f.read()
                popup_text(filename, text)
            except Exception as e:
                print("Error: ", e)
window.close()