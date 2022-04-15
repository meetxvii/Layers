from tkinter import Tk, Label, Frame
from PIL import Image, ImageTk, ImageOps
import webbrowser
class Splash:
    def __init__(self):
        splash = Tk()
        splash.geometry("400x400")
        width = splash.winfo_screenwidth()
        height = splash.winfo_screenheight()
        x = (width/2) - (400/2)
        y = (height/2) - (400/2)
        splash.geometry("+%d+%d" % (x, y))
        splash.configure(bg="white")
        splash.overrideredirect(True)

        logo_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/Layers.png"), (300, 100)))
        logo_img_label = Label(splash, image=logo_img, bg="white")
        logo_img_label.place(relx=0.5, rely=0.5, anchor="center")

        info_frame = Frame(splash, bg="white", width=400, height=100)
        info_frame.place(relx=0.5, rely=0.8, anchor="center")
        
        info_text = "Layers, Image Editing tool"
        info_label = Label(info_frame, text=info_text, bg="white", fg="#77cbff", font=("Arial Rounded MT Bold", 20))
        info_label.place(relx=0.5, rely=0.5, anchor="center")

        dev_label = Label(info_frame, text="Developed by: Meet Makwana", bg="white", fg="#77cbff", font=("Arial Rounded MT Bold", 12), cursor="hand2")
        dev_label.place(relx=0.65, rely=0.8, anchor="center")
        dev_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/meetxvii"))

        splash.after(3000, lambda: splash.destroy())
        splash.mainloop()

if __name__ == "__main__":
    Splash()