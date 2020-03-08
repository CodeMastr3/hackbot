from tkinter import *
from tkinter import ttk
import submitBot as SB
import createRoles as CR
#import ubuntuConnector as UC
#import serverOperations as SO
#import comparisonMaker as CM

# Establishes root GUI Frame as Tk() object (a GUI)
root = Tk()
root.title("Bot Factory")
finalSubmit = SB.SubmitTokenRequest(root)
# Instantiate a ttk Notebook object with root as it's master window
nb = ttk.Notebook(root, width=900)
# Create Tabs in Notebook as new Frames
f1 = ttk.Frame(nb)
#f2 = ttk.Frame(nb)
#f3 = ttk.Frame(nb)
# Add Tabs to Notebook with titles
nb.add(f1, text="Create Roles")
#nb.add(f2, text="Add Emoji")
#nb.add(f3, text="Create Roles")

CR.SetAttributes(f1)

nb.pack(fill="both", expand=True)
nb.grid()
credit = Label(root, text="Joel Aguilar, Cody Evans, and James Howell 2019").grid()
# Loop to keep program running until user closes program
root.geometry("1000x500")
root.mainloop()
