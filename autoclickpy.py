import pynput.keyboard as keyboard
import pynput.mouse as mouse
import time
from tkinter import *

clicker_actions = []
recording = False
mousecontrol = mouse.Controller()
keyboardcontrol = keyboard.Controller()

def isint(arg):
    try:
        arg = int(arg)
        return True
    except ValueError:
        return False

def islist(arg):
    try:
        arg1 = arg[0]
        return True
    except TypeError or ValueError:
        return False

def on_click(x, y, button, pressed):
    global recording
    if button == mouse.Button.left and recording and pressed:
        clicker_actions.append((x, y))

def on_press(key):
    if recording:
        try:
            clicker_actions.append(key.char)
        except AttributeError:
            #clicker_actions.append(key)
            pass

def start_rec():
    #print("Started recording!")
    global recording
    recording = True

def stop_rec():
    #print("Stopped recording!")
    global recording
    recording = False

def shownumber():
    global repeats
    repeats.place(relx = 0.5, rely = 0.72, anchor = CENTER)
    repeats.delete('0', 'end')
    repeats.insert(0, 'Number of repeats')

def hidenumber():
    global repeats
    repeats.place_forget()

def start_click():
    #print("Started clicking!")
    global mousecontrol, keyboardcontrol, recording, clicker_actions, repeats
    if recording:
        clicker_actions.pop()
        recording = False
    clicker_actions.pop()
    delay = lag.get()
    if not isint(repeats.get()) and len(repeats.get()) > 0:
        reps = 1
    elif len(repeats.get()) > 0:
        reps = int(repeats.get())
    else:
        reps = 1
    for i in range(reps):
        for i in clicker_actions:
            if type(i) is tuple:
                mousecontrol.position = i
                mousecontrol.click(mouse.Button.left, 1)
            else:
                keyboardcontrol.type(i)
            time.sleep(delay / 1000)
    clicker_actions = []


listenerm = mouse.Listener(on_click = on_click)
listenerm.start()
listenerk = keyboard.Listener(on_press = on_press)
listenerk.start()

root = Tk()
root.title('AutoClickPy')
root.geometry("300x450")
root.bind("<Escape>", lambda event: root.destroy())

recbtn = Button(root, width = 11, height = 2, text = "Start recording", command = start_rec)
recbtn.place(relx = 0.5, rely = 0.1, anchor = CENTER)

stopbtn = Button(root, width = 11, height = 2, text = "Stop recording", command = stop_rec)
stopbtn.place(relx = 0.5, rely = 0.25, anchor = CENTER)

lagtext = Label(root, text = "Delay between clicks (milliseconds)")
lagtext.place(relx = 0.5, rely = 0.37, anchor = CENTER)
lag = Scale(root, from_= 0, to = 2000, tickinterval = 500, length = 200, orient = HORIZONTAL)
lag.place(relx = 0.5, rely = 0.47, anchor = CENTER)

radiovar = BooleanVar()
radiovar.set(1)
finite = Radiobutton(text = 'Repeat X times',variable = radiovar, command = shownumber, value = 0)
infinite = Radiobutton(text = 'Repeat until ESC is pressed', variable = radiovar, command = hidenumber, value = 1)
finite.place(relx = 0.5, rely = 0.6, anchor = CENTER)
infinite.place(relx = 0.5, rely = 0.65, anchor = CENTER)
repeats = Entry(root,  width = 20)
repeats.bind("<FocusIn>", lambda args: repeats.delete('0', 'end') if not isint(repeats.get()) else args)
repeats.bind("<Button-1>", lambda args: repeats.delete('0', 'end') if not isint(repeats.get()) else args)

clickbtn = Button(root, width = 11, height = 2, text = "Start clicking", command = start_click)
clickbtn.place(relx = 0.5, rely = 0.9, anchor = CENTER)

root.mainloop()
