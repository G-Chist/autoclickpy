import pynput.keyboard as ke
import pynput.mouse as mouse
import time
from tkinter import *

positions = []
recording = False
mousecontrol = mouse.Controller()

def on_click(x, y, button, pressed):
    global recording
    if button == mouse.Button.left and recording and pressed:
        positions.append((x, y))

def start_rec():
    #print("Started recording!")
    global recording
    recording = True

def stop_rec():
    #print("Stopped recording!")
    global recording
    recording = False

def start_click():
    #print("Started clicking!")
    global mousecontrol
    global positions
    global recording
    if recording:
        positions.pop()
        recording = False
    positions.pop()
    delay = lag.get()
    for i in positions:
        mousecontrol.position = i
        mousecontrol.click(mouse.Button.left, 1)
        time.sleep(delay / 1000)
    positions = []


listener = mouse.Listener(on_click = on_click)
listener.start()

root = Tk()
root.title('AutoClickPy')
root.geometry("300x400")
root.bind("<Escape>", lambda event: root.destroy())

recbtn = Button(root, width = 11, height = 2, text = "Start recording", command = start_rec)
recbtn.place(relx = 0.5, rely = 0.2, anchor = CENTER)

stopbtn = Button(root, width = 11, height = 2, text = "Stop recording", command = stop_rec)
stopbtn.place(relx = 0.5, rely = 0.35, anchor = CENTER)

lagtext = Label(root, text = "Delay between clicks (milliseconds)")
lagtext.place(relx = 0.5, rely = 0.5, anchor = CENTER)
lag = Scale(root, from_= 0, to = 2000, tickinterval = 500, length = 200, orient = HORIZONTAL)
lag.place(relx = 0.5, rely = 0.6, anchor = CENTER)


clickbtn = Button(root, width = 11, height = 2, text = "Start clicking", command = start_click)
clickbtn.place(relx = 0.5, rely = 0.8, anchor = CENTER)

root.mainloop()