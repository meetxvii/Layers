from tkinter import Tk, Label, Button, Frame, SOLID
from PIL import Image, ImageTk, ImageOps
class Message:
    def __init__(self):
        self.window = Tk()
        self.window.overrideredirect(True)
        self.window.geometry(f'350x200+{(self.window.winfo_screenwidth()//2) - (350//2) }+{(self.window.winfo_screenheight()//2) - (200//2)}')
        self.window.configure(background='#173041')
        self.return_val = None
        self.close_btn_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/close.png"), (20,20)))
        self.close_btn = Button(self.window, image= self.close_btn_img, command=self.clicked_close, bg='#173041', borderwidth=0, activebackground='#173041', height=25, width=25,highlightthickness=0)
        self.close_btn.place(x=5, y=5)
        
        self.msg_frame = Frame(self.window, bg='#173041')
        self.msg_frame.place(relx=0.5, rely=0.5, anchor="center")

    def clicked_close(self):
        self.return_val = "CLOSE"
        self.window.destroy()
    
    def clicked_no(self):
        self.return_val = "NO"
        self.window.destroy()
    
    def clicked_yes(self):
        self.return_val = "YES"
        self.window.destroy()


    def info(self, message):
        self.warning_logo = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/warning.png"), (64,64)))
        self.warning_logo_label = Label(self.msg_frame, image=self.warning_logo, bg='#173041')
        self.warning_logo_label.grid(row=0, column=0, sticky="nsew")
        self.label = Label(self.msg_frame, text=message, bg='#173041', fg='#ffffff', font=('Belleza', 25))
        self.label.grid(row=0, column=1, sticky="nsew")
        self.window.mainloop()
        return self.return_val

    def confirm(self, message):
        self.confirm_logo = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/confirm.png"), (64,64)))
        self.confirm_logo_label = Label(self.msg_frame, image=self.confirm_logo, bg='#173041')
        self.confirm_logo_label.grid(row=0, column=0, sticky="nsew")
        self.label = Label(self.msg_frame, text=message, bg='#173041', padx=15, fg='#ffffff', font=('Belleza', 20))
        self.label.grid(row=0, column=1, sticky="nsew")
        
        self.inner_frame = Frame(self.msg_frame, bg='#173041', height=60)
        self.inner_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.no_btn = Button(self.inner_frame, text="No", bg='#173041', fg='#ffffff', font=('Belleza', 10),relief=SOLID, borderwidth=1, padx=20, pady=5, command=self.clicked_no)
        self.no_btn.place(relx=0.25, rely=0.5, anchor="center")
        self.yes_btn = Button(self.inner_frame, text="Yes", bg='#173041', fg='#ffffff', font=('Belleza', 10),relief=SOLID, borderwidth=1, padx=20, pady=5, command=self.clicked_yes)
        self.yes_btn.place(relx=0.75, rely=0.5, anchor="center")
        self.window.mainloop()
        return self.return_val    