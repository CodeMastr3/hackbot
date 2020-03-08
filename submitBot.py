from tkinter import *


class SubmitTokenRequest(Frame):
    botName = ""

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=W)  # , padx=25, pady=10)
        Label(self, text="Bot Name:").grid(row=0, column=0, sticky=W)
        self.botName = Entry(self)
        self.botName.grid(row=0, column=1, sticky=W)
        # Button to launch pop up window
        Button(self, text="Generate Token", background="azure",
               command=lambda: None       # Executes after button has been pressed, submit token create function here
               ).grid(row=0, column=3, sticky=W)
'''
from tkinter import *
import serverOperations as SO


class UbuntuConnector (Frame):
    # Public members
    ip = ""
    username = ""
    password = ""
    cursor = None

    # Constructor method
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=W)#, padx=25, pady=10)
        self.connectMsg = Text(self, height=1, width=138, background="azure")  # Text box confirming connection
        self.connectMsg.grid(row=0, column=1, sticky=E)
        # Button to launch pop up window
        Button(self, text="Connect", background="azure",
               command=lambda: self.popup()  # Executes after button has been pressed
               ).grid(row=0, column=0, sticky=W)

    # Pop up method
    def popup(self):
        self.window = Toplevel(background="azure")  # tkinter object
        self.window.wm_title("Connect to Ubuntu")
        # IP Address Label and Entry
        Label(self.window, text="IP Address: ", background="azure").grid(row=0, column=0, sticky=E)
        self.ip = Entry(self.window)
        self.ip.grid(row=0, column=1, sticky=W)
        # Username Label and Entry
        Label(self.window, text="Username: ", background="azure").grid(row=1, column=0, sticky=E)
        self.username = Entry(self.window)
        self.username.grid(row=1, column=1, sticky=W)
        # Password Label and Entry
        Label(self.window, text="Password: ", background="azure").grid(row=2, column=0, sticky=E)
        self.password = Entry(self.window, show='*')
        self.password.grid(row=2, column=1, sticky=W)
        # Button to submit values and connect to server
        Button(self.window, text="Enter", background="azure",
               command=lambda: self.connect()
               ).grid(row=3, column=1, sticky=E)

    # Connection method
    def connect(self):
        # calls the makeConnection method in Server Operations
        self.cursor = SO.makeConnection(self.username.get(), self.password.get(), self.ip.get())
        self.display()  # Display confirmation
        self.window.destroy()  # Delete pop up window

    # Confirmation display method
    def display(self):
        msg = "Connected to ubuntu@" + self.ip.get() + " as " + self.username.get()
        self.connectMsg.delete('1.0', END)  # replace previous message if necessary
        self.connectMsg.insert(END, msg)
'''