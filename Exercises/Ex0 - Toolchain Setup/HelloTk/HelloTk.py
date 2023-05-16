from tkinter import *
import os
import wsl


print("Distro:\t", wsl.get_wsl_distro())
print("Host:\t", wsl.get_wsl_host())
print("Display:", os.environ['DISPLAY'])

root = Tk()
w = Label(root, text="Snakesssss")
w.pack()

root.mainloop()
