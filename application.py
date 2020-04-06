#!/usr/bin/env python3
import tkinter as tk
from tkinter import OptionMenu, StringVar
from lib.ssh import *
import os
import sys
import paramiko
from datetime import datetime

hosts = [
        '192.168.0.1',
        '172.16.0.1',
        '10.0.0.1'
        ]

commands = [
        'sh clock',
        'sh ver',
        'sh run | s access-group',
        'sh run', 
        'exit'
        ]

####################### Stdout Redirect to GUI ############################################
class StdoutRedirect(object):
    def __init__(self, text_frame):
        self.text_area = text_frame

    def write(self, message):
        self.text_area.configure(state = "normal")
        self.text_area.insert("end", message)
        self.text_area.update_idletasks()
        self.text_area.see('end')
        self.text_area.configure(state = "disabled")

    def flush(self, message):
        sys.__stdout__.flush(message)

####################### Create the Tkinter GUI #####################################
class GUI(tk.Frame):
    # initialize the gui
    def __init__(self, master):
        self.frame = tk.Frame.__init__(self, master)    
        self.master = master    
        self.core_gui()
        self.pack()
        self.master.title("test")

    def core_gui(self):
        self.menubar = tk.Menu(self)
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.master.quit)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menu)
        menu.add_command(label="Copy")
        menu.add_command(label="Paste")
            
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            self.master.tk.call("config", "-menu", self.menubar)

###################### Create new frame for logo image #############################
        frame_header = tk.Frame(self)
        frame_header.pack(padx=0, pady=10, anchor='w')

        self.logo = tk.PhotoImage(file = 'image1.gif')

        tk.Label(frame_header, image = self.logo).grid(row=0, column=0, rowspan = 2)
#################### Create new frame for user input boxes #########################
        #username and password
        dialog_frame = tk.Frame(self)
        dialog_frame.pack(padx=20, pady=0, anchor='w')
        #username box
        tk.Label(dialog_frame, text = 'Username:').grid(row=0, column=0, sticky='w')

        self.user_input = tk.Entry(dialog_frame, background='white', width=24)
        self.user_input.grid(row=0, column=1, sticky='w')
        #Password Box
        tk.Label(dialog_frame, text = 'Password:').grid(row=1, column=0, sticky='w')

        self.pass_input = tk.Entry(dialog_frame, background='white', width=24, show='*')
        self.pass_input.grid(row=1, column=1, sticky='w')

#################### Define a new frame for dropdowns and actions ####################
        frame_content = tk.Frame(self)
        frame_content.pack(padx=0, pady=40, anchor='w')

        tk.Label(frame_content, text = "Devices:").grid(row=3, column=0)
        tk.Label(frame_content, text = "Commands:").grid(row=5, column=0)

        self.host_select = StringVar()
        self.command_select = StringVar(frame_content)

        def get_and_assign_host(event):
            self.host_option = self.host_select.get()
            self.command_options = self.command_select.get()
            if self.host_option:
                print(self.host_option)
            if self.command_options:
                print(self.command_options)

        self.host_dropdown = OptionMenu(frame_content, self.host_select, *hosts, command = get_and_assign_host)
        self.host_dropdown.config(width=24)
        self.host_dropdown.grid(row=3, column=1)

        self.command_dropdown = OptionMenu(frame_content, self.command_select, *commands, command = get_and_assign_host)
        self.command_dropdown.config(width=24)
        self.command_dropdown.grid(row=5, column=1)


################## Define Actions for Buttons and Dropdown menu ####################
        button_frame = tk.Frame(self)
        button_frame.pack(padx=0, pady=20, anchor='e')

        def click_submit(*args):
            print("user clicked 'submit': \nUsername: {}\nPassword: {}").format(self.user_input.get(),  
                        self.pass_input.get())

            if self.host_select.get() == hosts[0]:
                host0 = ssh(hosts[0], self.user_input.get(), self.pass_input.get())
                host0.sendCommand('en' + '\n' + "terminal len 0" +'\n' + self.command_options + '\n' + "exit" + '\n')

            elif self.host_select.get() == hosts[1]:
                host1 = ssh(hosts[1], self.user_input.get(), self.pass_input.get())
                host1.sendCommand('en' + '\n' + "terminal len 0" +'\n' + self.command_options + '\n' + "exit" + '\n')

            elif self.host_select.get() == hosts[2]:
                host2 = ssh(hosts[2], self.user_input.get(), self.pass_input.get())
                host2.sendCommand('en' + '\n' + "terminal len 0" +'\n' + self.command_options + '\n' + "exit" + '\n')

        self.submit_button = tk.Button(button_frame, text = "submit", command=click_submit)
        self.submit_button.grid(row=6, column=1)

#################### Define a new frame for dropdowon button clickns and actions ####################
        text_frame = tk.Frame(borderwidth=1, relief=None)
        text_frame.pack(padx=10, pady=10, anchor='center')
        text_area = tk.Text(text_frame, wrap='word', width=100, height=15)

        self.vbar = tk.Scrollbar(text_frame, orient="vertical", borderwidth=1, command=text_area.yview)
        self.vbar.pack(in_=text_frame, side="right", fill='y', expand=False)

        text_area.configure(state='disabled', yscrollcommand=self.vbar.set)

        sys.stdout = StdoutRedirect(text_area)
        sys.stdin = StdoutRedirect(text_area)
        sys.stderr = StdoutRedirect(text_area)

        text_area.pack(in_=text_frame, fill="both", expand=True)

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def main():
    root = tk.Tk()

    canvas = tk.Canvas(root)
    vsb = tk.Scrollbar(root, orient="vertical", borderwidth=1, command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y", expand=False)

    root.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    gui = GUI(root)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.resizable(True, True)
    #w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    #root.geometry("%dx%d+20+20" % (w, h))

    root.mainloop()

if __name__ == '__main__':
    main()
