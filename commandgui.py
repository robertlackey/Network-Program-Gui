import Tkinter as tk
from Tkinter import OptionMenu, StringVar

import os
import sys
import paramiko
from datetime import datetime
#
###############################
#retu
day_of_year = datetime.now().timetuple().tm_yday
now = datetime.now ()
abbrev_month = datetime.now()
abbrev_yr = datetime.now()
current_day = now.day
current_year = now.year
CONFIGSTR = "Device Configs on "
JULIANDATESTR = abbrev_yr.strftime('%y') + str(day_of_year) + " "
TIMESTAMP = '%s %s %s' % (abbrev_month.strftime('%b'), now.day, now.year)
FULLNAME = CONFIGSTR + JULIANDATESTR + TIMESTAMP
#
###############################
#
#storing the path in a variable
#THIS IS FOR LINUX PC/SERVER AND WILL NEED TO BE MODIFIED FOR WINDOWS
CONFIGDIR = str(FULLNAME)
#
###############################
#
TESTDEV0 = "TESTDEV0.txt"
TESTDEV1 = "TESTDEV1.txt"
#
###############################
#
TESTDEV0DIR = os.path.join(CONFIGDIR, TESTDEV0)
TESTDEV1DIR = os.path.join(CONFIGDIR, TESTDEV1)
#
###############################
#
ioshosts = [
##*** CISCO IOS IPs ***##
        #TESTDEV0 IP
        '192.168.0.1',
        '172.16.1.1',
        '172.22.0.230',
        ]
asahosts = [
##*** CISCO ASA IPs ***##
        #TESTDEV0 IP
        '192.168.1.1',
        '172.16.1.1',
        '10.112.113.129',
        ]
#
###############################
ioscommands = [
        'sh clock',
        'sh ver',
        'sh run | s access-group',
        'sh run', 
        'exit'
        ]
asacommands = [
        'sh clock',
        'sh ver',
        'sh run access-group',
        'sh run', 
        'exit'
        ]
####################################################################################
####################### Stdout Redirect ############################################
####################################################################################
#
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
#
####################################################################################
################### SSH Class for Accessing Cisco Devices ##########################
####################################################################################
#
class ssh:
    client = None
#
####################################################################################
########### initialize the ssh class and create the necessary parts ################
#
    def __init__(self, address, username, password):
        # Let the user know we're connecting to the device
        print "Connecting to device"
            # Create a new SSH client
        self.client = paramiko.SSHClient()
            # The following line is required if you want the script to be able to access a devices that's not yet in the known_hosts file
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Make the connection
        self.client.connect(address, username=username, password=password, look_for_keys=False)
#
####################################################################################
###################### create the function to send the commands ####################
#
    def sendCommand(self, command):
        #time.sleep(20)
        chan = self.client.invoke_shell()
        chan.send(command)
        print "sending commands"
        clientbuffer = []
        try:
            while not chan.exit_status_ready():
                if chan.recv_ready():
                    data = chan.recv(9999)
                    while data:
                        clientbuffer.append(data)
                        data = chan.recv(99999)
            self.clientoutput = ''.join(clientbuffer)
        except:
            raise
        print self.clientoutput
        self.client.close()
        sys.stdout = StdoutRedirect(self.clientoutput)
#
####################################################################################
####################### Create the Tkinter GUI #####################################
####################################################################################
#
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
#
####################################################################################
###################### Create new frame for logo image #############################
#
        frame_header = tk.Frame(self)
        frame_header.pack(padx=0, pady=10, anchor='w')

        self.logo = tk.PhotoImage(file = 'image1.gif')

        tk.Label(frame_header, image = self.logo).grid(row=0, column=0, rowspan = 2)
#
####################################################################################
#################### Create new frame for user input boxes #########################
#
        #username and password
        dialog_frame = tk.Frame(self)
        dialog_frame.pack(padx=20, pady=0, anchor='w')
        #username box
        tk.Label(dialog_frame, text = 'Username:').grid(row=0, column=0, sticky='w')
#
        self.user_input = tk.Entry(dialog_frame, background='white', width=24)
        self.user_input.grid(row=0, column=1, sticky='w')
        #Password Box
        tk.Label(dialog_frame, text = 'Password:').grid(row=1, column=0, sticky='w')
#
        self.pass_input = tk.Entry(dialog_frame, background='white', width=24, show='*')
        self.pass_input.grid(row=1, column=1, sticky='w')
#
######################################################################################
#################### Define a new frame for dropdowns and actions ####################
#
        #IP and Commands Labels
        frame_content = tk.Frame(self)
        frame_content.pack(padx=0, pady=40, anchor='w')
#
        tk.Label(frame_content, text = "ios Devices:").grid(row=3, column=0)
        tk.Label(frame_content, text = "asa devices:").grid(row=3, column=5)
        tk.Label(frame_content, text = "ios commands:").grid(row=5, column=0)
        tk.Label(frame_content, text = "asa commands:").grid(row=5, column=5)
#
        self.ioshost_select = StringVar()
        self.ioscommand_select = StringVar(frame_content)
        self.asahost_select = StringVar(frame_content)
        self.asacommand_select = StringVar(frame_content)
#
        def get_and_assign_ios(event):
            self.ioshost_option = self.ioshost_select.get()
            self.ioscommand_options = self.ioscommand_select.get()
            if self.ioshost_option:
                print self.ioshost_option
            if self.ioscommand_options:
                print self.ioscommand_options

        def get_and_assign_asa(event):
            self.asahost_option = self.asahost_select.get()
            self.asacommand_options = self.asacommand_select.get()
            if self.asahost_option:
                print self.asahost_option
            if self.asacommand_options:
                print self.asacommand_options
#
        self.ios_host_dropdown = OptionMenu(frame_content, self.ioshost_select, ioshosts[0], ioshosts[1], 
            ioshosts[2], command = get_and_assign_ios)
        self.ios_host_dropdown.config(width=24)
        self.ios_host_dropdown.grid(row=3, column=1)

#
        self.ios_command_dropdown = OptionMenu(frame_content, self.ioscommand_select, ioscommands[0], ioscommands[1], 
            ioscommands[2], ioscommands[3], command = get_and_assign_ios)
        self.ios_command_dropdown.config(width=24)
        self.ios_command_dropdown.grid(row=5, column=1)

        self.asa_host_dropdown = OptionMenu(frame_content, self.asahost_select, asahosts[0], asahosts[1], 
            asahosts[2], command = get_and_assign_asa)
        self.asa_host_dropdown.config(width=24)
        self.asa_host_dropdown.grid(row=3, column=6)

        self.asa_command_dropdown = OptionMenu(frame_content, self.asacommand_select, asacommands[0], asacommands[1], 
            asacommands[2], asacommands[3], command = get_and_assign_asa)
        self.asa_command_dropdown.config(width=24)
        self.asa_command_dropdown.grid(row=5, column=6)
#
####################################################################################
################## Define Actions for Buttons and Dropdown menu ####################
#
        button_frame = tk.Frame(self)
        button_frame.pack(padx=0, pady=20, anchor='e')

        def click_submit(*args):
            print "user clicked 'submit': \nUsername: {}\nPassword: {}".format(self.user_input.get(),  
                        self.pass_input.get())

            if self.asahost_select.get() == asahosts[0]:
                asahost0 = ssh(asahosts[0], self.user_input.get(), self.pass_input.get())
                asahost0.sendCommand('en' + '\n' + "terminal pager 0" +'\n' + self.asacommand_options + '\n' + "exit" + '\n')

            elif self.asahost_select.get() == asahosts[1]:
                asahost1 = ssh(asahosts[1], self.user_input.get(), self.pass_input.get())
                asahost1.sendCommand('en' + '\n' + "terminal pager 0" +'\n' + self.asacommand_options + '\n' + "exit" + '\n')

            elif self.asahost_select.get() == asahosts[2]:
                asahost2 = ssh(asahosts[2], self.user_input.get(), self.pass_input.get())
                asahost2.sendCommand('en' + '\n' + "terminal pager 0" +'\n' + self.asacommand_options + '\n' + "exit" + '\n')

            elif self.ioshost_select.get() == ioshosts[0]:
                ioshost0 = ssh(ioshosts[0], self.user_input.get(), self.pass_input.get())
                ioshost0.sendCommand('en' + '\n' + "terminal len 0" +'\n' + self.ioscommand_options + '\n' + "exit" + '\n')

            elif self.ioshost_select.get() == ioshosts[1]:
                ioshost1 = ssh(ioshosts[1], self.user_input.get(), self.pass_input.get())
                ioshost1.sendCommand('en' + '\n' + "terminal len 0" +'\n' + self.ioscommand_options + '\n' + "exit" + '\n')

            elif self.ioshost_select.get() == ioshosts[2]:
                ioshost2 = ssh(ioshosts[2], self.user_input.get(), self.pass_input.get())
                ioshost2.sendCommand('en' + '\n' + "terminal len 0" +'\n' + self.ioscommand_options + '\n' + "exit" + '\n')

        self.submit_button = tk.Button(button_frame, text = "submit", command=click_submit)
        self.submit_button.grid(row=6, column=1)
#
######################################################################################
#################### Define a new frame for dropdowon button clickns and actions ####################
#
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
#
#####################################################################################
####################### create the main function ####################################
#
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
#
#####################################################################################
####################### Run the Main Function #######################################
#
if __name__ == '__main__':
    main()
  
  
