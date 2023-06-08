from tkinter import *
from PIL import ImageTk
import pyautogui
from easyocr import *
import os
import time
from translate import Translator

def St1():
    global escape
    escape = 0
    Start.destroy()
    time.sleep(0.2)

def quit_program(e):
   window.destroy()

def get_mouse_posn(event):
    global topy, topx

    topx, topy = event.x, event.y

def update_sel_rect(event):
    global rect_id
    global topy, topx, botx, boty

    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)  

def translate_text():
    text = w1
    translator = Translator(from_lang=from_lang_var.get(), to_lang=to_lang_var.get())
    translation = translator.translate(text)

    pole.insert(END, translation)

escape = 0
language1 = 'en'
language2 = 'ru'

while escape == 0:
    
    escape = 1
    Start = Tk()

    mainphoto = PhotoImage(file = "im\images.png")

    from_lang_var = StringVar()
    from_lang_var.set(language1)
    from_lang_menu = OptionMenu(Start, from_lang_var, "en", "ru", "fr", "es") 
    from_lang_menu.pack()
    
    to_lang_var = StringVar()
    to_lang_var.set(language2) 
    to_lang_menu = OptionMenu(Start, to_lang_var, "ru", "en", "fr", "es") 
    to_lang_menu.pack()
    
    Start.lift()
    Start.title('')
    
    Start.iconphoto(False, mainphoto)

    Start.wm_attributes("-topmost", True)

    Start.geometry('250x125')

    Start.resizable(width=False, height=False)

    btn = Button(Start, text="Сканировать экран",command=St1) 
    btn.pack()
    
    Start.mainloop()
    
    if escape == 0:
        topx, topy, botx, boty = 0, 0, 0, 0
        rect_id = None

        myScreenshot = pyautogui.screenshot()

        window = Tk()
        window.title("Select Area")
        window.attributes('-fullscreen',True)
        window.wm_attributes("-topmost", True)

        img = ImageTk.PhotoImage(myScreenshot)

        canvas = Canvas(window, width=img.width(), height=img.height(),borderwidth=0, highlightthickness=0)
        canvas.pack(expand=True)
        canvas.img = img 
        canvas.create_image(0, 0, image=img, anchor=NW)

        rect_id = canvas.create_rectangle(topx, topy, topx, topy, dash=(10,10), fill='', outline='green')

        canvas.bind('<Button-1>', get_mouse_posn)
        canvas.bind('<B1-Motion>', update_sel_rect)

        window.bind('<ButtonRelease-1>', quit_program)

        window.mainloop()

        if topx > botx:
            buf1 = topx
            topx = botx
            botx = buf1
        if topy > boty:
            buf2 = topy
            topy = boty
            boty = buf2

        screen = myScreenshot.crop((topx,topy,botx,boty))
        screen.save('delete.jpg')

        language1 = from_lang_var.get()
        reader = easyocr.Reader([language1])
        result = reader.readtext('delete.jpg', detail=0)

        os.remove('delete.jpg')

        w1 = str(' '.join(result))

        root = Tk()
        root.title('перевод')
        root.geometry('700x400')
        root.resizable(width=False, height=False)

        pole = Text(root, width=90, height=25, font='Arial, 10')
        pole.pack(pady=10) 

        mainphoto = PhotoImage(file = "im\images.png")

        root.iconphoto(False, mainphoto)

        translate_text()

        language2 = to_lang_var.get()
        
        root.mainloop()
       
    else:  
        break