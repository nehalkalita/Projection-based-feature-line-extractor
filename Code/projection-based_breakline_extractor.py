import csv
import math
import time
import threading
import multiprocessing
import os
#import subprocess
import sys
#import numpy
from tkinter import *
from tkinter import filedialog as fd
import tkinter.font as font
#from tkdocviewer import *

import gen_csv_terrain_GUI
import spatial_test_GUI
import join_neighbors_GUI

total_cores = multiprocessing.cpu_count()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        try:
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def change_text_1():
    global s_data_flag
    s_data_flag = 0
    filename = fd.askopenfilename(parent=root, filetypes=[('Text files', ['*.txt', '*.TXT']),('All files', '*'),])
    entry_file.delete(0,END)
    entry_file.insert(0,filename)
    if len(entry_file.get()) > 0:
        label_st_2.configure(text='File imported', fg='black')
    else:
        label_st_2.configure(text='No file imported', fg='black')

def status_thread(text1, color1):
    label_st_2.configure(text=text1, fg=color1)
    button_s.configure(state='disabled')
    button_open.configure(state='disabled')
    entry_file.configure(state='disabled')
    entry_cpu.configure(state='disabled')
    entry_skip.configure(state='disabled')
    entry_x.configure(state='disabled')
    entry_y.configure(state='disabled')
    entry_z.configure(state='disabled')
    entry_dec.configure(state='disabled')
    entry_blk.configure(state='disabled')
    entry_span.configure(state='disabled')
    entry_lht.configure(state='disabled')
    entry_cper.configure(state='disabled')
    entry_pxy.configure(state='disabled')
    entry_nbr.configure(state='disabled')
    entry_lp.configure(state='disabled')
    button2_1.configure(state='disabled')
    button2_2.configure(state='disabled')
    file1.entryconfig(0, state='disabled')

def widget_state_n():
    button_s.configure(state='normal')
    button_open.configure(state='normal')
    entry_file.configure(state='normal')
    entry_cpu.configure(state='normal')
    entry_skip.configure(state='normal')
    entry_x.configure(state='normal')
    entry_y.configure(state='normal')
    entry_z.configure(state='normal')
    entry_dec.configure(state='normal')
    entry_blk.configure(state='normal')
    entry_span.configure(state='normal')
    entry_lht.configure(state='normal')
    entry_cper.configure(state='normal')
    entry_pxy.configure(state='normal')
    entry_nbr.configure(state='normal')
    entry_lp.configure(state='normal')
    button2_1.configure(state='normal')
    button2_2.configure(state='normal')
    file1.entryconfig(0, state='normal')

s_data_flag = 0
s_data_loc = ''

def submit1_a():
    global s_data_flag
    if len(entry_file.get()) > 0:
        temp_loc1 = entry_file.get()
        #temp_loc = temp_loc[::-1]
        temp_loc2 = ''
        i1 = len(temp_loc1) - 1
        while (i1 >= 0):
            if temp_loc1[i1] == '/':
                break
            i1 = i1 - 1
        for i in range(i1 + 1):
            temp_loc2 = temp_loc2 + temp_loc1[i]

        t1 = time.time()
        if s_data_flag == 1:
            XYZ_return = gen_csv_terrain_GUI.gen_csv(s_data_loc, temp_loc2, int(entry_dec.get()), int(entry_cpu.get()), int(entry_x.get()) - 1, int(entry_y.get()) - 1, int(entry_z.get()) - 1, int(entry_skip.get()))
        else:
            XYZ_return = gen_csv_terrain_GUI.gen_csv(entry_file.get(), temp_loc2, int(entry_dec.get()), int(entry_cpu.get()), int(entry_x.get()) - 1, int(entry_y.get()) - 1, int(entry_z.get()) - 1, int(entry_skip.get()))
        if len(XYZ_return) == 3:
            spatial_test_GUI.spatial_test(int(entry_cpu.get()), temp_loc2, entry_blk.get(), entry_span.get(), entry_dec.get(), int(entry_lht.get()), int(entry_cper.get()))
            join_neighbors_GUI.join_neighbors(int(entry_cpu.get()), temp_loc2, entry_blk.get(), entry_span.get(), entry_pxy.get(), entry_nbr.get(), entry_lp.get(), int(CB2_var.get()), int(CB3_var.get()), int(entry_dec.get()), int(entry_x.get()) - 1, int(entry_y.get()) - 1, int(entry_z.get()) - 1, XYZ_return)
            temp_text = "Analysis completed \n\nTime taken : " + str(round(time.time() - t1, 2)) + " seconds"
            temp_text = temp_text + "\n\nPrimary output file : 'breaklines.obj'"
            if int(CB2_var.get()) == 1:
                temp_text = temp_text + "\nOnly points file : 'breakline_points.csv'"
            if int(CB3_var.get()) == 1:
                temp_text = temp_text + "\nOnly edges file : 'breakline_edges.csv'"
            label_st_2.configure(text=temp_text, fg='#004500')
            widget_state_n()

            if s_data_flag == 1:
                s_file = open(s_data_loc, "r")
                s_data = s_file.read()
                s_file.close()
                path_spl_out = ''
                for i in str(os.getcwd()):
                    if i == '\\':
                        path_spl_out = path_spl_out + '/'
                    else:
                        path_spl_out = path_spl_out + i

                with open(path_spl_out + '/SampleData.txt', "w") as file:
                    file.write(s_data)

        else:
            label_st_2.configure(text=XYZ_return, fg='red')
            widget_state_n()
    else:
        label_st_2.configure(text='No file imported', fg='red')
        widget_state_n()
    s_data_flag = 0

def callback_thres(P):
    if P.isdigit():
        if int(P) > 0 and int(P) <= total_cores:
            return True
        else:
            return False
    elif P == "":
        return True
    else:
        return False

def callback_vals(P):
    if P.isdigit():
        return True
    elif P == "":
        return True
    else:
        return False

def OpenContact():
    multiprocessing.freeze_support()
    stem1 = Toplevel() #Tk()
    stem1.geometry('300x130')
    stem1.title("Contact Us")
    stem1.iconbitmap(resource_path("breakline_icon.ico"))
    stem1.resizable(0,0)

    temp1 = "\nNehal Kalita \nnehalkalita94@gmail.com \n\n\nDr. Rejesh K. Maurya \nrk.maurya@gmail.com"
    Label(stem1, text =temp1).pack()

def HelpManual():
    multiprocessing.freeze_support()
    #subprocess.Popen(["cmd", resource_path('Manual.txt')])
    stem2 = Toplevel() #Tk()
    stem2.geometry('800x550')
    stem2.title("Manual")
    stem2.iconbitmap(resource_path("breakline_icon.ico"))
    stem2.resizable(0,0)
    
    file1 = open(resource_path('Manual1.txt'), 'r')
    scrollbary = Scrollbar(stem2)
    scrollbary.pack( side = RIGHT, fill = Y )
    scrollbarx = Scrollbar(stem2, orient = HORIZONTAL)
    scrollbarx.pack( side = BOTTOM, fill = X )
    mylist = Listbox(stem2, yscrollcommand = scrollbary.set, xscrollcommand = scrollbarx.set, width = 500, height = 680)
    count1 = 0
    for line in file1:
        if count1 == 0:
           b_font = font.Font(size=11, weight='bold')
           txt1 = '\n ' + line
           Label(stem2, text = txt1, font=b_font).pack()
        elif (count1 >= 6 and count1 <= 16) or (count1 >= 32 and count1 <= 36) or (count1 == 41 or count1 == 42) or (count1 >= 47 and count1 <= 49) or (count1 >= 57 and count1 <= 59) or (count1 == 64 or count1 == 65):
            mylist.insert(END, '  ' + u'\u2022         ' + line)
        else:
            mylist.insert(END, '  ' + line)
        count1 = count1 + 1
    
    mylist.pack(fill=BOTH) #  side = LEFT, fill = BOTH 
    scrollbary.config( command = mylist.yview )
    scrollbarx.config( command = mylist.xview )
    #Label(stem2, text =temp1).pack()

def SampleData():
    global s_data_flag
    global s_data_loc
    s_data_flag = 1
    entry_file.delete(0,END)
    entry_file.insert(0,"sample_data1.csv")
    s_data_loc = resource_path("sample_data1.csv")
    entry_skip.delete(0,END)
    entry_skip.insert(0,0)
    entry_x.delete(0,END)
    entry_x.insert(0,1)
    entry_y.delete(0,END)
    entry_y.insert(0,2)
    entry_z.delete(0,END)
    entry_z.insert(0,3)
    entry_dec.delete(0,END)
    entry_dec.insert(0,2)
    entry_blk.delete(0,END)
    entry_blk.insert(0,60)
    entry_span.delete(0,END)
    entry_span.insert(0,4)
    entry_lht.delete(0,END)
    entry_lht.insert(0,80)
    entry_cper.delete(0,END)
    entry_cper.insert(0,20)
    entry_pxy.delete(0,END)
    entry_pxy.insert(0,100)
    entry_nbr.delete(0,END)
    entry_nbr.insert(0,380)
    entry_lp.delete(0,END)
    entry_lp.insert(0,35)
    label_st_2.configure(text='Sample data selected', fg='black')
    
def ExitWin():
    #sys.exit()
    root.destroy()
    #root.quit()
    
if __name__ == '__main__':
    multiprocessing.freeze_support()
    root = Tk()
    root.geometry('854x480') #'1280x720'
    root.title("Projection-based Breakline Extractor")
    root.iconbitmap(resource_path("breakline_icon.ico"))
    #root.state('zoomed')
    root.resizable(0,0)
    #root.attributes('-fullscreen', True)
    size_10 = font.Font(size=10)
    size_10b = font.Font(size=10, weight='bold')

    CB2_var = IntVar()
    CB3_var = IntVar()

    frame1 = Frame(root, bg='#888888', bd=5)
    frame1.place(relx=0.5, rely=0.05, relwidth=0.95, relheight=0.1, anchor='n')

    button_open = Button(root, text="Import raw file", font=size_10, height=1, width=15, bg='#cacaca', command=lambda:change_text_1())
    button_open.place(relx=0.037, rely=0.074)
    entry_file = Entry(root, font=size_10)
    entry_file.place(relx=0.21, rely=0.079, relwidth=0.5)

    button_s = Button(root, text="Submit", font=size_10, height=1, width=10, bg='#cacaca', command=lambda:[status_thread('\n\nData under analysis', 'black'), threading.Thread(target=(submit1_a), daemon=True).start()])
    button_s.place(relx=0.86, rely=0.074)

    menubar = Menu(root)
    file1 = Menu(menubar, tearoff = 0)
    menubar.add_cascade(label= 'File', menu = file1)
    file1.add_command(label= 'Sample Data', command = SampleData)
    file1.add_separator()
    file1.add_command(label= 'Exit', command = ExitWin)
    help1 = Menu(menubar, tearoff = 0)
    menubar.add_cascade(label = 'Help', menu = help1)
    help1.add_command(label= 'Manual', command = HelpManual)
    help1.add_separator()
    help1.add_command(label= 'Contact Us', command = OpenContact)
    root.config(menu= menubar)
    reg_thres1 = root.register(callback_thres)
    reg_vals1 = root.register(callback_vals)

    label_1_test = 'Avaliable logical CPUs : ' + str(total_cores)
    label_2_test = 'CPUs to use : '
    label_1 = Label(root, text=label_1_test, font=size_10, bg='#f0f0f0', fg='blue')
    label_1.place(relx=0.030, rely=0.82)
    label_2 = Label(root, text=label_2_test, font=size_10, bg='#f0f0f0')
    label_2.place(relx=0.030, rely=0.88)
    entry_cpu = Entry(root, font=size_10)
    entry_cpu.place(relx=0.198, rely=0.88, relwidth=0.04)
    entry_cpu.delete(0,END)
    entry_cpu.insert(0,total_cores)
    entry_cpu.config(validate='key', validatecommand=(reg_thres1, '%P'))

    label_rhead = Label(root, text='Row selection', font=size_10, fg='purple', bg='#f0f0f0', justify= LEFT)
    label_rhead.place(relx=0.38, rely=0.41)
    label_skip = Label(root, text='Rows to be skipped', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_skip.place(relx=0.38, rely=0.47)
    entry_skip = Entry(root, font=size_10)
    entry_skip.place(relx=0.55, rely=0.475, relwidth=0.04)
    entry_skip.delete(0,END)
    entry_skip.insert(0,0)
    entry_skip.config(validate='key', validatecommand=(reg_vals1, '%P'))

    label_chead = Label(root, text='Column selection', font=size_10, fg='purple', bg='#f0f0f0', justify= LEFT)
    label_chead.place(relx=0.38, rely=0.61)
    label_x = Label(root, text='X column', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_x.place(relx=0.38, rely=0.67)
    entry_x = Entry(root, font=size_10)
    entry_x.place(relx=0.48, rely=0.675, relwidth=0.04)
    entry_x.delete(0,END)
    entry_x.insert(0,1)
    entry_x.config(validate='key', validatecommand=(reg_vals1, '%P'))
    label_y = Label(root, text='Y column', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_y.place(relx=0.38, rely=0.73)
    entry_y = Entry(root, font=size_10)
    entry_y.place(relx=0.48, rely=0.735, relwidth=0.04)
    entry_y.delete(0,END)
    entry_y.insert(0,2)
    entry_y.config(validate='key', validatecommand=(reg_vals1, '%P'))
    label_z = Label(root, text='Z column', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_z.place(relx=0.38, rely=0.79)
    entry_z = Entry(root, font=size_10)
    entry_z.place(relx=0.48, rely=0.795, relwidth=0.04)
    entry_z.delete(0,END)
    entry_z.insert(0,3)
    entry_z.config(validate='key', validatecommand=(reg_vals1, '%P'))

    label_dec = Label(root, text='Decimal places to round', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_dec.place(relx=0.030, rely=0.22)
    entry_dec = Entry(root, font=size_10)
    entry_dec.place(relx=0.215, rely=0.225, relwidth=0.07)
    entry_dec.delete(0,END)
    entry_dec.insert(0,2)
    label_blk = Label(root, text='Block size', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_blk.place(relx=0.030, rely=0.28)
    entry_blk = Entry(root, font=size_10)
    entry_blk.place(relx=0.215, rely=0.285, relwidth=0.07)
    entry_blk.delete(0,END)
    entry_blk.insert(0,40)
    label_span = Label(root, text='Span across \nhighest / lowest point', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_span.place(relx=0.030, rely=0.34)
    entry_span = Entry(root, font=size_10)
    entry_span.place(relx=0.215, rely=0.360, relwidth=0.07)
    entry_span.delete(0,END)
    entry_span.insert(0,5)
    #, min_local_height, median_covg_perc
    label_lht = Label(root, text='Min. local height difference', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_lht.place(relx=0.38, rely=0.22)
    entry_lht = Entry(root, font=size_10)
    entry_lht.place(relx=0.62, rely=0.225, relwidth=0.07)
    entry_lht.delete(0,END)
    entry_lht.insert(0,100)
    label_cper = Label(root, text='Section median coverage (in %)', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_cper.place(relx=0.38, rely=0.28)
    entry_cper = Entry(root, font=size_10)
    entry_cper.place(relx=0.62, rely=0.285, relwidth=0.07)
    entry_cper.delete(0,END)
    entry_cper.insert(0,25)

    label_pxy = Label(root, text='Min. breakline length \nalong X,Y coordinates', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_pxy.place(relx=0.030, rely=0.51)
    entry_pxy = Entry(root, font=size_10)
    entry_pxy.place(relx=0.215, rely=0.53, relwidth=0.07)
    entry_pxy.delete(0,END)
    entry_pxy.insert(0,100)
    label_nbr = Label(root, text='Max. length between \npoints for connectivity', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_nbr.place(relx=0.030, rely=0.61)
    entry_nbr = Entry(root, font=size_10)
    entry_nbr.place(relx=0.215, rely=0.63, relwidth=0.07)
    entry_nbr.delete(0,END)
    entry_nbr.insert(0,150)
    label_lp = Label(root, text='Max. length for \nclosed edges', font=size_10, bg='#f0f0f0', justify= LEFT)
    label_lp.place(relx=0.030, rely=0.71)
    entry_lp = Entry(root, font=size_10)
    entry_lp.place(relx=0.215, rely=0.73, relwidth=0.07)
    entry_lp.delete(0,END)
    entry_lp.insert(0,40)

    label_add = Label(root, text='Additional \nexport options', font=size_10, fg='purple', bg='#f0f0f0', justify= LEFT)
    label_add.place(relx=0.79, rely=0.22)
    button2_1 = Checkbutton(root, text="Export points", font=size_10, bg='#f0f0f0', justify= LEFT, variable=CB2_var)
    button2_1.place(relx=0.79, rely=0.32)
    button2_2 = Checkbutton(root, text="Export edges", font=size_10, bg='#f0f0f0', justify= LEFT, variable=CB3_var)
    button2_2.place(relx=0.79, rely=0.38)

    frame2 = Frame(root, bg='#cccccc', bd=5)
    frame2.place(relx=0.8, rely=0.55, relwidth=0.35, relheight=0.37, anchor='n')
    label_st_1 = Label(root, text='Status :', font=size_10, bg='#cccccc', justify= LEFT, fg='blue')
    label_st_1.place(relx=0.655, rely=0.58)
    label_st_2 = Label(root, text='No file imported', font=size_10, bg='#cccccc', justify= LEFT)
    label_st_2.place(relx=0.655, rely=0.64)

    root.mainloop()