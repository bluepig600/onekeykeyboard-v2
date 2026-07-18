from pynput import keyboard
import time
import tkinter as tk

control = keyboard.Controller()
Key = keyboard.Key
ignore = False
spaceTimes = []

def pressed(key):
    global ignore
    #print(key)
def released(key):
    """if key == Key.space:
        print("key released")
        control.release(key)"""
def win32_event_filter(msg, data):
    global ignore
    #print(data.flags)
    #print(msg, data.vkCode)
    if data.vkCode == 32 and not ignore:
        if msg != 257:
            spaceTimes.append(time.time())
        #print("space blocked")
        listener.suppress_event()
    elif not ignore:
        listener.suppress_event()
listener = keyboard.Listener(on_press=pressed,on_release=released,win32_event_filter=win32_event_filter)
listener.start()
chars = ["space","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
times = 0
hold = False
actions = []
happening = False
holdingMaybe = 0
def action(numOfSpaces):
    actions.append((0,numOfSpaces))
    #print("")
def holding(secs):
    actions.append((1,secs))
    #print(actions)
root = tk.Tk()
root.title("onekeykeyboard")
root.attributes('-topmost', True)
label = tk.Label(root, text="intalizing", font=("Arial", 40))
label.pack()
def checkkeypress(): 
    global times, hold, holdingMaybe, happening
    happening = len(spaceTimes) > 0
    if happening:
        times = time.time() - spaceTimes[-1]
        if len(spaceTimes) > 1:
            if spaceTimes[-1]-spaceTimes[-2] < 0.05 and not hold:
                hold = True
                #print("hold started")
    if times > 0.3:
        if hold:

            secs = time.time() - holdingMaybe - times
            #print("hold " + str(secs) + " seconds")
            holding(secs)
            holdingMaybe = 0
        else:
            amount = len(spaceTimes)
            #print(amount)
            action(amount)
            holdingMaybe = spaceTimes[-1]

        spaceTimes.clear()
        times = 0
        hold = False
    root.after(5, checkkeypress)

i = 1

def keyboardthing():
    global actions, hold, i, ignore
    if hold:
        i += 1
        if i > 27:
            i = 1
        root.after(100, keyboardthing)
    label.config(text=chars[i-1])
    if not hold:
        if len(actions) > 0:
            if actions[-1][0] == 0:
                #print("there is a tap action")
                root.after(300, keyboardthing2)
            else:
                root.after(100, keyboardthing)
        else:
            root.after(100, keyboardthing) 
    
    
def keyboardthing2():
    global actions, hold, i, ignore
    print("testing hold")
    if hold: 
        #print("leave")
        root.after(100, keyboardthing)
        return
    if actions[-1][1] == 1:
        ignore = True
        if i == 1:
            control.press(Key.space)
            control.release(Key.space)
        else:
            control.press(chars[i-1])
            control.release(chars[i-1])
        ignore = False
        actions = []
        i = 1 
    elif actions[-1][1] == 2:
        i += 1
        actions = []
    elif actions[-1][1] == 3:
        i -= 1
        actions = []
    root.after(100, keyboardthing)
root.after(1000, checkkeypress)
root.after(2000, keyboardthing)
root.mainloop()