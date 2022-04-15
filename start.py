from tkinter import Tk, Label, Button, filedialog as fd, Frame, font, LEFT, messagebox
from PIL import Image, ImageTk, ImageOps
import csv, webbrowser
from Edit import Edit
from lib import splash
from os import path, system
class Start:
    def __init__(self):

        self.root = Tk()
        self.root.resizable(0, 0)
        self.root.geometry("320x570+600+100")
        self.root.title("Layers")
        self.root.iconbitmap("./img/icon.ico")
        self.root.configure(background="#ebebeb")

        # background Image
        self.bg_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/open_bg.jpg"), (320, 570)))
        self.bg_label = Label(self.root, image=self.bg_img)
        self.bg_label.place(x=0, y=0)

        # logo image
        self.logo_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/Layers.png"), (266, 50)))
        self.logo_img_label = Label(self.root, image=self.logo_img, bg="white")
        self.logo_img_label.place(relx=0.5, rely=0.09, anchor="center")

        
        #Render Recent Frame
        self.render_recent_frame()

        # Open Button
        file_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/folder.png"), (48,48)))
        self.open_btn = Button(self.root, text="Open", image=file_img, compound=LEFT, width=250,  bg="#7BCDFF", borderwidth=0 , fg="white", font=("Belleza", 20), command=self.open_file_dialog)
        self.open_btn.place(relx=0.5, rely=0.8, anchor="center")
        
        self.root.mainloop()

    def render_recent_frame(self):
        
        self.recent_frame = Frame(self.root, bg="#ebebeb", width=320, height=285)
        self.recent_frame.place(relx=0.5, rely=0.45, anchor="center")

        try:
            with open("./data/recents.csv", "r") as file:
                reader = csv.reader(file)
                self.recent_file_list = []
                for i in reader:              
                    if i[0] != "":
                        self.recent_file_list.append(i[0])      
                                
                if len(self.recent_file_list) != 4:
                    self.recent_file_list = ["./img/stock_img1.jpg", "./img/stock_img2.jpg", "./img/stock_img3.jpg", "./img/stock_img4.jpg"]
                
                file.close()
        except:
            self.recent_file_list = ["./img/stock_img1.jpg", "./img/stock_img2.jpg", "./img/stock_img3.jpg", "./img/stock_img4.jpg"]
            return
            

        self.recent_label = Label(self.recent_frame, text="Recent Edits", bg="#ebebeb", fg="#032541", font=("Belleza", 20))
        self.recent_label.grid(row=0, column=0, sticky="nsew")
        try:
            self.recent_img_1 = ImageTk.PhotoImage(ImageOps.contain(Image.open(self.recent_file_list[0]), (350, 158)))
            self.recent_img_1_btn = Button(self.recent_frame, image=self.recent_img_1, bg="#ebebeb", border=0, command=lambda: self.open_file(self.recent_file_list[0]))  
            self.recent_img_1_btn.grid(row=1, column=0, sticky="nsew")

            self.inner_recent_frame = Frame(self.recent_frame, bg="#ebebeb")
            self.inner_recent_frame.grid(row=2, column=0, sticky="nsew")
            
            self.recent_img_2 = ImageTk.PhotoImage(ImageOps.fit(Image.open(self.recent_file_list[1]), (80, 80)))
            self.recent_img_2_btn = Button(self.inner_recent_frame, image=self.recent_img_2, bg="#ebebeb", border=0, command=lambda: self.open_file(self.recent_file_list[1]))
            self.recent_img_2_btn.grid(row=0, column=0, sticky="nsew")

            self.recent_img_3 = ImageTk.PhotoImage(ImageOps.fit(Image.open(self.recent_file_list[2]), (80, 80)))
            self.recent_img_3_btn = Button(self.inner_recent_frame, image=self.recent_img_3, bg="#ebebeb", border=0, command=lambda: self.open_file(self.recent_file_list[2]))
            self.recent_img_3_btn.grid(row=0, column=1, sticky="nsew")

            self.recent_img_4 = ImageTk.PhotoImage(ImageOps.fit(Image.open(self.recent_file_list[3]), (80, 80)))
            self.recent_img_4_btn = Button(self.inner_recent_frame, image=self.recent_img_4, bg="#ebebeb", border=0, command=lambda: self.open_file(self.recent_file_list[3]))
            self.recent_img_4_btn.grid(row=0, column=2, sticky="nsew")
        except:
            pass
             
    def open_file_dialog(self):
        try:
            filetypes = [("JPG Files", "*.jpg"),("PNG Files", "*.png")]
            filepath = fd.askopenfile(title = "Open an Image", initialdir="/", filetypes=filetypes)
            self.open_file(filepath.name)
        except AttributeError:
            pass

    def open_file(self, path):        
        if path in self.recent_file_list:
            self.recent_file_list.remove(path)
            self.recent_file_list.insert(0, path)
        else:
            self.recent_file_list.insert(0, path)
            self.recent_file_list.pop()
        try: 
            with open(r".\data\recents.csv","w",newline="\n") as csvfile:
                for i in range(4):
                    csvfile.write(self.recent_file_list[i] + "\n")
        except FileNotFoundError as e:
            pass   
        self.recent_frame.destroy()
        self.render_recent_frame()
        self.root.destroy()
        ed = Edit(path)     

if __name__ == "__main__":
    splash.Splash()
    start = Start()