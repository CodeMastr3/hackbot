from tkinter import *
import createRoles as CR


class SubmitTokenRequest(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=W)
        self.grid_columnconfigure(0, minsize=965)
        # Button to launch pop up window
        Button(self, text="Generate Token", background="azure",
               command=lambda: self.generateToken()       # Executes after button has been pressed
               ).grid(row=0, column=0, sticky=E)

    def generateToken(self):
        roles = CR.SetAttributes.roles
        file = open("roles.txt", "w")
        file.write(str(roles))
        file.close()
