import tkinter
import sys
import os

# check if 
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

master = tkinter.Tk()
master.title("tester")
master.geometry("300x100")

master.mainloop()