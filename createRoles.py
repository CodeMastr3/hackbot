from tkinter import *
import tkinterScrollbar as tkS


class Role(Frame):
    roleName = ""
    emojiName = ""
    msg = ""
    message = ""

    def __init__(self, r, e, m, master=None):
        Frame.__init__(self, master)
        self.config(width=880)
        self.lf = LabelFrame(master, background="azure")
        self.lf.grid(sticky=W)
        self.lf.config(width=880)
        self.lf.grid_columnconfigure(0, minsize=400)
        self.lf.grid_columnconfigure(1, minsize=100)
        self.text = Text(self.lf, height=1, width=100, wrap=NONE)
        self.text.pack()
        self.roleName = r
        self.emojiName = e
        self.msg = m
        self.message = self.roleName + "\t\t\t\t" + self.emojiName + "\t\t\t\t" + self.msg
        self.insertMsg()

    def insertMsg(self):
        self.text.insert(END, self.message)


class SetAttributes(Frame):
    roles = {}
    row = 1

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=W)
        self.config(width=880)
        self.lf = LabelFrame(self, text="Enter Role Name and Emoji Name", background="gray80")
        self.lf.grid(sticky=W)
        self.lf.config(width=880)
        Label(self.lf, text="Role Name", background="gray80").grid(row=0, column=0, sticky=E)
        self.e1 = Entry(self.lf)
        self.e1.grid(row=0, column=1, sticky=W)

        Label(self.lf, text="Emoji Name", background="gray80").grid(row=0, column=2, sticky=E)
        self.e2 = Entry(self.lf)
        self.e2.grid(row=0, column=3, sticky=W)

        Label(self.lf, text="Message", background="gray80").grid(row=0, column=4, sticky=E)
        self.e3 = Entry(self.lf)
        self.e3.grid(row=0, column=5, sticky=W)

        Button(self.lf, text="Add Role", background="gray80",
               command=lambda: self.execute()
               ).grid(row=0, column=6, sticky=W)

        LF = LabelFrame(master, background="gray60")
        LF.grid()
        scrollFrame = tkS.VerticalScrolledFrame(LF)
        scrollFrame.grid(sticky="we")
        self.RD = RoleDisplay(master=scrollFrame.interior)

    def execute(self):
        roleName = self.e1.get()
        emojiName = self.e2.get()
        msg = self.e3.get()
        if msg not in self.roles:
            # to unicode
            self.roles[msg] = {self.toUnicode(emojiName): roleName}
        else:
            self.roles[msg][self.toUnicode(emojiName)] = roleName
        self.RD.display(self.row, roleName, emojiName, msg)
        self.row += 1

    def toUnicode(self, emojiName):
        unicodes = open("discord_unicode_test.txt", "r")
        for line in unicodes.readlines():
            fields = line.strip().split()
            if fields[1] == emojiName:
                return fields[0]
        unicodes.close()


class RoleDisplay(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=W)
        self.config(width=880)

    def display(self, r, id, e, m):
        newFrame = Frame(self)
        newFrame.grid(row=r, column=0, sticky=W)
        Role(id, e, m, newFrame)

