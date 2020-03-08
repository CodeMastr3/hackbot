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
<<<<<<< HEAD


'''
import cx_Oracle
from tkinter import *
import tkinter as tk
import queryOperations as q
import tkinterScrollbar as tkS

# Global Vars for serverOperations, yes global vars are bad
cursor = None
#m = ""   # string carrying query result
#c = 0  # query count

# Method connecting user to the server
def makeConnection (username, password, ip):
    connStr = username + '/' + password + '@' + ip + ':1521'
    connection = cx_Oracle.connect(connStr)
    c = connection.cursor()
    global cursor
    cursor = c


class SQLResult (Frame):
    # Contructor method
    def __init__(self, m, c, master=None):
        Frame.__init__(self, master)
        self.grid(row=1, column=0, sticky="se")
        self.message = m
        self.count = c
        # tkinter LabelFrame
        self.lf = LabelFrame(self, text="Query " + str(self.count), background="gray80")
        # tkinter Scrollbars, with LabelFrame as it's master window
        self.xScroll = Scrollbar(self.lf, orient=HORIZONTAL)
        self.xScroll.pack(side=BOTTOM, fill=X)
        self.yScroll = Scrollbar(self.lf, orient=VERTICAL)
        self.yScroll.pack(side=RIGHT, fill=Y)
        # tkinter Text box, with LabelFrame as it's master window
        self.text = Text(self.lf, height=27, width=136, wrap=NONE, background="salmon")
        self.text.pack(side=LEFT, fill=Y)
        self.yScroll.config(command=self.text.yview)
        self.xScroll.config(command=self.text.xview)
        self.text.config(xscrollcommand=self.xScroll.set, yscrollcommand=self.yScroll.set)
        self.insertMsg()  # insert query result into LabelFrame window
        self.lf.grid(column=0)

    # Insert Message m into LabelFrame Text box
    def insertMsg (self):
        self.text.insert(END, self.message)


class SQLAccess (Frame):
    # Public members
    sql = ""
    count = 1
    queries = []
    dRow = 1
    qRow = 1
    var = None
    op = None
    QD = None

    # Constructor method
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=W)
        sqlLF = LabelFrame(master, background="azure")
        sqlLF.grid(sticky=W)
        #sqlLF.config(width=1000)
        sqlLF.grid_columnconfigure(3, minsize=614)
        # SQL Label and Entry
        Label(sqlLF, text="SQL>", background="azure").grid(row=0, column=0, sticky=E)
        self.sql = Entry(sqlLF)
        self.sql.grid(row=0, column=1, sticky=W)
        # Button to submit SQL command to server
        Button(sqlLF, text="Enter", bg="azure",
               command=lambda: self.execute()
               ).grid(row=0, column=2, sticky=W)
        self.var = StringVar()
        self.var.set("")
        self.op = OptionMenu(sqlLF, self.var, "--select one--", *self.queries)
        self.op.config(width=10)
        self.op.grid(row=0, column=3, sticky=E)
        Button(sqlLF, text="Download",
               command=lambda: self.download(),
               ).grid(row=0, column=4, sticky=E)


        queryLF = LabelFrame(master, background="gray60")
        queryLF.grid()
        scrollFrame = tkS.VerticalScrolledFrame(queryLF)
        scrollFrame.grid(sticky="we")
        self.QD = QueryDisplay(master=scrollFrame.interior)

    def execute(self): # need to implement refresh for queries option menu
        #i = self.count
        query = q.create(cursor, self.sql.get())  # Uses query create method to create query
        self.queries.append(query)
        self.QD.display(query, self.count)  # Display query result
        self.dRow += 1
        self.count += 1  # iterate query count

        self.var.set('')
        self.op['menu'].delete(0, 'end')
        for count in range(1, self.count):
            self.op['menu'].add_command(label="Query "+str(count), command=tk._setit(self.var, count))

    def download(self):
        idx = int(self.var.get()) - 1
        q.download(self.queries[idx], idx)

class QueryDisplay (Frame):
    # Public members
    count = 1
    dRow = 1
    qRow = 1

    # Constructor method
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=W)
        self.config(width=1000)

    # Display method that makes query result and query count global, creates new SQLResult instances
    def display(self, m, c):
        # New Frame for SQLResult to inhabit
        newFrame = Frame(self)
        newFrame.grid(row=self.qRow, column=2, sticky=W)
        self.qRow += 1
        # New instance of SQLResult, with newFrame as it's master window
        SQLResult(m, c, newFrame)

'''
=======
>>>>>>> 92a5a035c02027fe6559075df4173b03ef080827
