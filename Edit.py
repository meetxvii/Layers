from tkinter import Tk, ttk, Label, Button, Frame, Scale, TOP, LEFT, HORIZONTAL, SOLID, colorchooser, filedialog as fd, messagebox, Entry
from PIL import ImageOps, Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from os import path as pth, remove as rm
import time

class Edit:

    def __init__(self, path):

        if not pth.isfile(path):
            # If the file doesn't exist, open the start window
            from lib import message
            m1 = message.Message()
            m1.info("Failed to open file")
            self.open_start_window()
            return

        self.path = path        
        self.save_path = None
        self.history = []
        self.root = Tk()
        self.root.resizable(0, 0)
        self.root.title(f"{pth.basename(path)} || LAYERS")
        self.root.iconbitmap("./img/icon.ico")
        self.root.geometry("700x570+600+100")
        self.root.configure(background="white")

        self.top_navbar = Frame(self.root, bg="white", height=40, width=700)
        self.top_navbar.grid(row=0, column=0)

        self.home_btn_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/home_blue.png"), (32,32)))
        self.home_btn = Button(self.top_navbar, image=self.home_btn_img, bg="white", activebackground="white", borderwidth=0, command=self.open_start_window, cursor="hand2")
        self.home_btn.place(relx=0.1, rely=0.55, anchor="center")

        self.home_btn.bind("<Enter>", lambda event: self.change_home_btn(1))
        self.home_btn.bind("<Leave>", lambda event: self.change_home_btn(0))

        self.render_menu_bar()
        
        self.save_btn_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/save.png"), (32,32)))
        self.save_btn = Button(self.top_navbar, image=self.save_btn_img, bg="white", activebackground="white", borderwidth=0, command=self.save_img, cursor="hand2")
        self.save_btn.place(relx=0.9, rely=0.55, anchor="center")

        self.save_btn.bind("<Enter>", lambda event: self.change_save_btn(1))
        self.save_btn.bind("<Leave>", lambda event: self.change_save_btn(0))

        self.undo_btn_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/undo.png"), (32,32)))
        self.undo_btn_off_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/undo_off.png"), (32,32)))
        self.undo_btn = Button(self.root, bg="white", activebackground="white", borderwidth=0, command=self.undo, cursor="hand2")
        self.undo_btn.place(relx=0.1, rely=0.15, anchor="center")

        self.display_img = Image.open(path)
        self.set_new_image_in_display(self.display_img)
        

        self.filters_frame = Frame(self.root, bg="white", height=100, width=700)
        # self.filters_frame.place(relx=0.5, rely=0.9, anchor="center")
        self.set_filters_frame()

        self.enchance_frame = Frame(self.root, bg="white", height=100, width=700)
        # self.enchance_frame.place(relx=0.5, rely=0.9, anchor="center")
        self.set_enchance_frame()

        self.edit_frame = Frame(self.root, bg="white", height=100, width=700)
        # self.edit_frame.place(relx=0.5, rely=0.9, anchor="center")
        self.set_edit_frame()

        
        self.adjustment_frame = Frame(self.root, bg="white", height=50, width=700)
        self.adjustment_frame.place(relx=0.5, rely=0.95, anchor="center")

        self.display_filters_frame()
        self.preview_img = self.display_img
        self.root.mainloop()

    def change_home_btn(self, state):
        ''' toggle view of home button '''
        if state == 1:
            self.home_btn_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/home_filled.png"), (32,32)))
            self.home_btn.configure(image=self.home_btn_img)
        else:
            self.home_btn_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/home_blue.png"), (32,32)))
            self.home_btn.configure(image=self.home_btn_img)

    def change_save_btn(self, state):
        ''' toggle view of save button '''
        if state == 1:
            self.save_btn_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/save_filled.png"), (32,32)))
            self.save_btn.configure(image=self.save_btn_img)
        else:
            self.save_btn_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/save.png"), (32,32)))
            self.save_btn.configure(image=self.save_btn_img)

    def render_menu_bar(self):
        ''' creates and renders menu bar in EDIT UI '''
        self.menu_frame = Frame(self.top_navbar, height=40, width=350)
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.notch_img = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/notch.png"), (350,40)))
        self.notch_label = Label(self.menu_frame, image=self.notch_img, bg="white")
        self.notch_label.place(relx=0.5, rely=0.5, anchor="center")

        self.change_UI_btn_frame = Frame(self.menu_frame, height=40, width=40, bg="white")
        self.change_UI_btn_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.filter_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/filter.png"), (20,20)))
        self.change_to_filter_btn = Button(self.change_UI_btn_frame, text="FILTER", command=self.display_filters_frame,image=self.filter_icon, compound=LEFT, bg="#182e43", activeforeground="white", activebackground="#182e43", fg="white", padx=10, font= ("Arial Rounded MT bold", 13) , borderwidth=0, cursor="hand2")
        self.change_to_filter_btn.grid(row=0, column=0, sticky="nsew")

        self.enhance_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/enhance.png"), (20,20)))
        self.change_to_enhance_btn = Button(self.change_UI_btn_frame, text="ENHANCE", command=self.display_enhance_frame,image=self.enhance_icon, compound=LEFT,  bg="#182e43", activeforeground="white", activebackground="#182e43", fg="white", padx=10, font= ("Arial Rounded MT bold", 13) , borderwidth=0, cursor="hand2")
        self.change_to_enhance_btn.grid(row=0, column=2, sticky="nsew")

        self.edit_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/edit.png"), (20,20)))
        self.change_to_edit_btn = Button(self.change_UI_btn_frame, text="EDIT", command=self.display_edit_frame,image=self.edit_icon, compound=LEFT, bg="#182e43", activeforeground="white", activebackground="#182e43", fg="white", padx=10, font= ("Arial Rounded MT bold", 13) , borderwidth=0, cursor="hand2")
        self.change_to_edit_btn.grid(row=0, column=4, sticky="nsew")

    def open_start_window(self):
        ''' redirect to start window '''
        try:
            self.root.destroy()
        except:
            pass
        from start import Start
        Start()

    def set_new_image_in_display(self, image):
        ''' set new image in display '''
        if len(self.history) == 0:
            self.undo_btn.configure(image=self.undo_btn_off_icon)
        else:
            self.undo_btn.configure(image=self.undo_btn_icon)
        try:
            self.display_image_label.destroy()
        except:
            pass
        image = ImageTk.PhotoImage(ImageOps.contain(image, (500, 350)))
        self.display_image_label = Label(self.root, image=image, bg="white")
        self.display_image_label.image = image
        self.display_image_label.place(relx=0.5, rely=0.4, anchor="center")

    def set_filters_frame(self):
  
        self.blur_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/blur.png"), (32,32)))
        self.gaussian_blur_btn = Button(self.filters_frame, text="Gaussian\nBlur", command=self.clicked_guassian_blur, image=self.blur_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.gaussian_blur_btn.grid(row=0, column=0, sticky="n")

        self.grayscale_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/grayscale.png"), (32,32)))
        self.grayscale_btn = Button(self.filters_frame, text="Grayscale", command=self.clicked_grayscale, image=self.grayscale_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.grayscale_btn.grid(row=0, column=1, sticky="n")

        self.invert_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/invert.png"), (32,32)))
        self.invert_btn = Button(self.filters_frame, text="Invert", command=self.clicked_invert, image=self.invert_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.invert_btn.grid(row=0, column=2, sticky="n")

        self.posterize_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/posterize.png"), (32,32)))
        self.posterize_btn = Button(self.filters_frame, text="Posterize", command=self.clicked_posterize, image=self.posterize_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.posterize_btn.grid(row=0, column=3, sticky="n")

        self.colorize_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/colorize.png"), (32,32)))
        self.colorize_btn = Button(self.filters_frame, text="Colorise", command=self.clicked_colorize, image=self.colorize_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.colorize_btn.grid(row=0, column=4, sticky="n")

        # self.filter_adjustments_frame = Frame(self.filters_frame, bg="white", height=100, width=250)
        # self.filter_adjustments_frame.grid(row=0, column=5,sticky="n")

    def set_enchance_frame(self):

        self.brightness_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/brightness.png"), (32,32)))
        self.brightness_btn = Button(self.enchance_frame, text="Brightness", command=self.clicked_brightness, image=self.brightness_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.brightness_btn.grid(row=0, column=0, sticky="n")

        self.contrast_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/contrast.png"), (32,32)))
        self.contrast_btn = Button(self.enchance_frame, text="Contrast", command=self.clicked_contrast, image=self.contrast_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.contrast_btn.grid(row=0, column=1, sticky="n")

        self.saturation_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/saturation.png"), (32,32)))
        self.saturation_btn = Button(self.enchance_frame, text="Saturation", command=self.clicked_saturation, image=self.saturation_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.saturation_btn.grid(row=0, column=2, sticky="n")

        self.sharpness_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/sharpness.png"), (32,32)))
        self.sharpness_btn = Button(self.enchance_frame, text="Sharpness", command=self.clicked_sharpness, image=self.sharpness_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.sharpness_btn.grid(row=0, column=3, sticky="n")

        # self.enchance_adujustments_frame = Frame(self.enchance_frame, bg="white", height=100, width=250)
        # self.enchance_adujustments_frame.grid(row=0, column=4,sticky="n")
  
    def set_edit_frame(self):
        
        self.flip_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/flip.png"), (32,32)))
        self.flip_btn = Button(self.edit_frame, text="Flip", command=self.clicked_flip, image=self.flip_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.flip_btn.grid(row=0, column=0, sticky="n")

        self.mirror_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/mirror.png"), (32,32)))
        self.mirror_btn = Button(self.edit_frame, text="Mirror", command=self.clicked_mirror, image=self.mirror_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.mirror_btn.grid(row=0, column=1, sticky="n")

        self.rotate_clock_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/rotate_clockwise.png"), (32, 32)))
        self.rotate_clock_btn = Button(self.edit_frame, text="Rotate\nClockwise", command=self.clicked_rotate, image=self.rotate_clock_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.rotate_clock_btn.grid(row=0, column=2, sticky="n")

        self.rotate_counter_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/rotate_counterclockwise.png"), (32, 32)))
        self.rotate_counter_btn = Button(self.edit_frame, text="Rotate\nCounter\nClockwise", command=self.clicked_rotate_counter, image=self.rotate_counter_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.rotate_counter_btn.grid(row=0, column=3, sticky="n")

        self.watermark_icon = ImageTk.PhotoImage(ImageOps.contain(Image.open("./img/icons/watermark.png"), (32, 32)))
        self.watermark_btn = Button(self.edit_frame, text="Watermark", command=self.clicked_watermark, image=self.watermark_icon, compound=TOP,  bg="white", padx=15, activebackground="white", borderwidth=0, cursor="hand2")
        self.watermark_btn.grid(row=0, column=4, sticky="n")

        self.is_img_rotated = False
        
    
    def display_filters_frame(self):
        ''' hide other features frame and display filters features '''
        self.change_to_filter_btn.config(fg="#72cbff")
        self.change_to_enhance_btn.config(fg="white")
        self.change_to_edit_btn.config(fg="white")
        self.delete_prvious_adjustment_controls()
        self.set_new_image_in_display(self.display_img)
        self.enchance_frame.place_forget()
        self.edit_frame.place_forget()
        self.filters_frame.place(relx=0.5, rely=0.8, anchor="center")
    
    def display_enhance_frame(self):
        ''' hide other features frame and display enhance features '''
        self.change_to_enhance_btn.config(fg="#72cbff")
        self.change_to_filter_btn.config(fg="white")
        self.change_to_edit_btn.config(fg="white")
        self.delete_prvious_adjustment_controls()
        self.set_new_image_in_display(self.display_img)
        self.filters_frame.place_forget()
        self.edit_frame.place_forget()
        self.enchance_frame.place(relx=0.5, rely=0.8, anchor="center")
    
    def display_edit_frame(self):
        ''' hide other features frame and display edit features '''
        self.change_to_edit_btn.config(fg="#72cbff")
        self.change_to_filter_btn.config(fg="white")
        self.change_to_enhance_btn.config(fg="white")
        self.delete_prvious_adjustment_controls()
        self.set_new_image_in_display(self.display_img)
        self.filters_frame.place_forget()
        self.enchance_frame.place_forget()
        self.edit_frame.place(relx=0.5, rely=0.8, anchor="center")

    def delete_prvious_adjustment_controls(self):
        try:
            self.ajust_label.destroy()
        except:
            pass

        try:
            self.adjust_scale.destroy()
        except:
            pass

        try:
            self.apply_btn.destroy()
        except:
            pass

        try:
            self.adjust_value.destroy()
        except:
            pass

        try:
            self.discard_btn.destroy()
        except:
            pass

        try:
            self.choose_highlight_label.destroy()
        except:
            pass

        try:
            self.choose_shadow_label.destroy()
        except:
            pass

        try:
            self.shadow_color_picker.destroy()
        except:
            pass

        try:
            self.highlight_color_picker.destroy()
        except:
            pass

        try:
            self.watermark_text.destroy()
        except:
            pass
    
        try:
            self.show_btn.destroy()
        except:
            pass

    def render_adjust_label(self, text, row, column, padx=10):
        self.ajust_label = Label(self.adjustment_frame, text=text, bg="white", font=("Helvetica", 12))
        self.ajust_label.grid(row=row, column=column, sticky="n", padx=padx)

    def render_adjust_scale(self, min, max, initial, row, column, func):
        self.adjust_scale = ttk.Scale(self.adjustment_frame, value=initial, from_=min, to=max, orient=HORIZONTAL)
        self.adjust_scale.grid(row=row, column=column, sticky="n", padx=10)
        self.adjust_scale.bind("<ButtonRelease-1>", func)

    def render_adjust_value(self, text, row, column):
        self.adjust_value = Label(self.adjustment_frame, text=text, bg="white", font=("Helvetica", 12))
        self.adjust_value.grid(row=row, column=column, sticky="n", padx=10)
    
    def render_apply_btn(self, row, column):
        self.apply_btn = Button(self.adjustment_frame, text="Apply", command=self.apply_changes, bg="white", padx=15, activebackground="white", borderwidth=1, relief=SOLID, cursor="hand2")
        self.apply_btn.grid(row=row, column=column, sticky="n", padx=10)

    def render_discard_btn(self, row, column):
        self.discard_btn = Button(self.adjustment_frame, text="Discard", command=self.discard_changes, bg="white", padx=15, activebackground="white", borderwidth=1, relief=SOLID, cursor="hand2")
        self.discard_btn.grid(row=row, column=column, sticky="n", padx=10)

    def pick_shadow(self):
        color = colorchooser.askcolor(parent=self.root, title="Pick Shadow Color")
        if color[1] is not None:
            self.shadow_color = color[1]
            self.shadow_color_picker.config(bg=self.shadow_color)
            self.apply_colorize()
    
    def pick_highlight(self):
        color = colorchooser.askcolor(parent=self.root, title="Pick Highlight Color")
        if color[1] is not None:
            self.highlight_color = color[1]
            self.highlight_color_picker.config(bg=self.highlight_color)
            self.apply_colorize()

    def undo(self):
        self.display_filters_frame()
        if len(self.history) == 0:
            return
        if len(self.history) == 1:
            self.display_img = self.history[0]
        if len(self.history) > 1:
            self.display_img = self.history[-1]
        self.history.pop()
        self.set_new_image_in_display(self.display_img)
        

# Button functions

    def clicked_guassian_blur(self):
        self.set_new_image_in_display(self.display_img)
        self.delete_prvious_adjustment_controls()
        self.render_adjust_label("Blur Radius : ", 0, 0)
        self.render_adjust_scale(0, 100, 0, 0, 1, self.apply_gaussian_blur)
        self.render_adjust_value(self.adjust_scale.get(), 0, 2)
        self.render_apply_btn(0, 3)
        self.render_discard_btn(0, 4)

    def clicked_grayscale(self):
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()
        self.preview_img = ImageOps.grayscale(self.display_img)
        self.set_new_image_in_display(self.preview_img)
        self.render_apply_btn(0, 0)
        self.render_discard_btn(0, 1)

    def clicked_invert(self):
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()
        self.preview_img = ImageOps.invert(self.display_img)
        self.set_new_image_in_display(self.preview_img)
        self.render_apply_btn(0, 0)
        self.render_discard_btn(0, 1)

    def clicked_posterize(self):
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()
        self.render_adjust_label("Posterize Level : ", 0, 0)
        self.render_adjust_scale(2, 8, 8, 0, 1, self.apply_posterize)
        self.render_adjust_value(self.adjust_scale.get(), 0, 2)
        self.render_apply_btn(0, 3)
        self.render_discard_btn(0, 4)

    def clicked_colorize(self):
        
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()
        
        self.choose_shadow_label = Label(self.adjustment_frame, text="Choose Shadow Color : ", bg="white", font=("Helvetica", 12))
        self.choose_shadow_label.grid(row=0, column=0, sticky="n")

        self.shadow_color = "black"
        self.shadow_color_picker = Button(self.adjustment_frame, text="", command=self.pick_shadow, bg="black", padx=15, fg="black", activebackground="white", borderwidth=1, cursor="hand2")
        self.shadow_color_picker.grid(row=0, column=1, sticky="n")

        self.choose_highlight_label = Label(self.adjustment_frame, text="Choose Highlight Color : ", bg="white", font=("Helvetica", 12))
        self.choose_highlight_label.grid(row=0, column=2, sticky="n")

        self.highlight_color = "white"
        self.render_adjust_label("Choose Highlight color : ", 0, 2)
        self.highlight_color_picker = Button(self.adjustment_frame, text="", command=self.pick_highlight, bg="white", padx=15, fg="white", activebackground="white", borderwidth=1, cursor="hand2")
        self.highlight_color_picker.grid(row=0, column=3, sticky="n")
        self.render_apply_btn(0, 4)
        self.render_discard_btn(0, 5)

    def clicked_brightness(self):
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()
        self.render_adjust_label("Brightness : ", 0, 0)
        self.render_adjust_scale(0, 200, 100, 0, 1, self.apply_brightness)
        self.render_adjust_value(self.adjust_scale.get(), 0, 2)
        self.render_apply_btn(0, 3)
        self.render_discard_btn(0, 4)

    def clicked_contrast(self):
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()
        self.render_adjust_label("Contrast : ", 0, 0)
        self.render_adjust_scale(0, 200, 100, 0, 1, self.apply_contrast)
        self.render_adjust_value(self.adjust_scale.get(), 0, 2)
        self.render_apply_btn(0, 3)
        self.render_discard_btn(0, 4)

    def clicked_saturation(self):
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()
        self.render_adjust_label("Saturation : ", 0, 0)
        self.render_adjust_scale(0, 200, 100, 0, 1, self.apply_saturation)
        self.render_adjust_value(self.adjust_scale.get(), 0, 2)
        self.render_apply_btn(0, 3)
        self.render_discard_btn(0, 4)

    def clicked_sharpness(self):
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()
        self.render_adjust_label("Sharpness : ", 0, 0)
        self.render_adjust_scale(-100, 100, 0, 0, 1, self.apply_sharpness)
        self.render_adjust_value(self.adjust_scale.get(), 0, 2)
        self.render_apply_btn(0, 3)
        self.render_discard_btn(0, 4)

    def clicked_flip(self):
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()
        
        self.preview_img = ImageOps.flip(self.display_img)
        self.set_new_image_in_display(image=self.preview_img)

        self.render_apply_btn(0, 0)
        self.render_discard_btn(0, 1)

    def clicked_mirror(self):
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()
        
        self.preview_img = ImageOps.mirror(self.display_img)
        self.set_new_image_in_display(image=self.preview_img)

        self.render_apply_btn(0, 0)
        self.render_discard_btn(0, 1)

    def clicked_rotate(self):
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()
        
        if self.is_img_rotated is False:
            self.preview_img = self.display_img.rotate(-90, expand=True)
            self.is_img_rotated = True
        else:
            self.preview_img = self.preview_img.rotate(-90, expand=True)
        
        self.set_new_image_in_display(image=self.preview_img)

        self.render_apply_btn(0, 0)
        self.render_discard_btn(0, 1)

    def clicked_rotate_counter(self):
        self.set_new_image_in_display(self.display_img)
        
        self.delete_prvious_adjustment_controls()

        
        if self.is_img_rotated is False:
            self.preview_img = self.display_img.rotate(90, expand=True)
            self.is_img_rotated = True
        else:
            self.preview_img = self.preview_img.rotate(90, expand=True)
        self.set_new_image_in_display(image=self.preview_img)

        self.render_apply_btn(0, 0)
        self.render_discard_btn(0, 1)

    def clicked_watermark(self):
        self.set_new_image_in_display(self.display_img)
        self.delete_prvious_adjustment_controls()
        
        self.watermark_text = Entry(self.adjustment_frame, width=30)
        self.watermark_text.grid(row=0, column=0, sticky="n", padx=10)
        self.watermark_text.bind("<Return>", self.watermark_text_changed)

        self.show_btn = Button(self.adjustment_frame, text="Show", command=lambda : self.watermark_text_changed(event=None), bg="white", padx=15, fg="black", activebackground="white", borderwidth=1, cursor="hand2")
        self.show_btn.grid(row=0, column=1, sticky="n", padx=10)


# End of button functions

# edit image functions

    def apply_gaussian_blur(self, event):
        ''' applies gaussian blur '''
        self.preview_img = self.display_img.filter(ImageFilter.GaussianBlur(int(self.adjust_scale.get())))
        self.adjust_value.configure(text=int(self.adjust_scale.get()))
        self.set_new_image_in_display(self.preview_img)
    
    def apply_posterize(self, event):
        ''' applies posterize '''
        self.preview_img = ImageOps.posterize(self.display_img, int(self.adjust_scale.get()))
        self.adjust_value.configure(text=int(self.adjust_scale.get()))
        self.set_new_image_in_display(self.preview_img)

    def apply_colorize(self):
        ''' applies colorize '''
        self.preview_img = ImageOps.colorize(self.display_img.convert("L"), self.shadow_color, self.highlight_color)
        self.set_new_image_in_display(self.preview_img.convert("RGB"))
        
    def apply_brightness(self, event):
        ''' applies brightness '''
        self.preview_img = ImageEnhance.Brightness(self.display_img).enhance(float(self.adjust_scale.get())/100)
        self.adjust_value.configure(text=int(self.adjust_scale.get()))
        self.set_new_image_in_display(self.preview_img)

    def apply_contrast(self, event):
        ''' applies contrast '''
        self.preview_img = ImageEnhance.Contrast(self.display_img).enhance(float(self.adjust_scale.get())/100)
        self.adjust_value.configure(text=int(self.adjust_scale.get()))
        self.set_new_image_in_display(self.preview_img)

    def apply_saturation(self, event):
        ''' applies saturation '''
        self.preview_img = ImageEnhance.Color(self.display_img).enhance(float(self.adjust_scale.get())/100)
        self.adjust_value.configure(text=int(self.adjust_scale.get()))
        self.set_new_image_in_display(self.preview_img)

    def apply_sharpness(self, event):
        ''' applies sharpness '''
        self.preview_img = self.display_img.filter(ImageFilter.UnsharpMask(threshold=6,percent=int(self.adjust_scale.get())))
        self.adjust_value.configure(text=int(self.adjust_scale.get()))
        self.set_new_image_in_display(self.preview_img)

    def watermark_text_changed(self, event):
        ''' apply watermark on preview image and display it '''

        if self.watermark_text.get() == "":
            messagebox.showerror("Empty Text", "Please enter text to watermark")
            return

        self.preview_img = self.display_img.copy()
        self.preview_img.convert("RGB")

        img_width, img_height = self.preview_img.size

        wm_size = (int(img_width * 0.20), int(img_height * 0.25))
        wm_txt = Image.new("RGBA", wm_size, (255, 255, 255, 0))

        font_size = int(img_width / 20)
        font = ImageFont.truetype("arial.ttf", font_size, encoding="unic")
        d = ImageDraw.Draw(wm_txt)
        wm_text = self.watermark_text.get()
        left = (wm_size[0] - font.getsize(wm_text)[0]) / 2
        top = (wm_size[1] - font.getsize(wm_text)[1]) / 2
        alpha = 75
        d.text((left, top), wm_text, fill=(0, 0, 0, alpha), font=font)
        for i in range(0, img_width, wm_txt.size[0]):
            for j in range(0, img_height, wm_txt.size[1]):
                self.preview_img.paste(wm_txt, (i, j), wm_txt)
        
        self.set_new_image_in_display(self.preview_img)
        self.watermark_text.destroy()
        self.show_btn.destroy()
        self.render_apply_btn(0, 0)
        self.render_discard_btn(0, 1)


# End of edit image functions

    def apply_changes(self):    
        ''' applies changes to the image '''
        self.is_img_rotated = False
        self.history.append(self.display_img)
        self.display_img = self.preview_img
        self.set_new_image_in_display(self.display_img)
        self.delete_prvious_adjustment_controls()

    def discard_changes(self):
        ''' discards changes '''
        self.set_new_image_in_display(self.display_img)
        self.delete_prvious_adjustment_controls()

    def save_img(self):
        ''' saves the image '''
        try:
            if self.save_path is None:
                self.save_path = fd.asksaveasfilename(initialdir=self.path, title="Save Image", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg")))
            if self.save_path[-4:] != ".png":
                self.save_path += ".png"
            self.display_img.save(self.save_path)
            messagebox.showinfo("Success", "Image Saved Successfully")
        except:
            messagebox.showerror("Error", "Could not save image")
        self.root.title(f"{pth.basename(self.save_path)} || LAYERS")
        self.delete_prvious_adjustment_controls()

    