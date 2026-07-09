import customtkinter as ctk
import pyperclip
import threading
import time
from pynput import keyboard

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Paperweight")
        self.overrideredirect(True) # Gets rid of the Windows title bar

        self.app_font = ctk.CTkFont(family="Calibri", size=-13)
        self.button_colorset = ("white", "#333333")  
        self.text_colorset = ("black", "white")

        self.copy_history = [] 

        self.grid_columnconfigure(0, weight=1)

        # Title Bar
        self.title_bar = ctk.CTkFrame(
            master=self,
            height=35,
            fg_color="transparent",
            corner_radius=0
        )
        
        self.title_bar.grid_propagate(False)
        self.title_bar.grid(row=0, column=0, sticky="ew")
        self.title_bar.grid_columnconfigure(1, weight=1)
        self.title_bar.grid_rowconfigure(0, weight=1)

        self.close_btn = ctk.CTkButton(
            self.title_bar,
            text="❌",
            width=45,
            height=35,
            corner_radius=0,
            fg_color="transparent",
            text_color=self.text_colorset,
            hover_color="red",
            command=self.withdraw
        )

        self.close_btn.grid(row=0, column=1, sticky="ne")

        self.title_label = ctk.CTkLabel(
                self.title_bar,
                text="Paperweight",
                font=self.app_font,
                fg_color="transparent",
                text_color=self.text_colorset,
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=15)

        self.title_bar.bind("<ButtonPress-1>", self.drag_start)
        self.title_label.bind("<ButtonPress-1>", self.drag_start)
        self.title_bar.bind("<B1-Motion>", self.drag_motion)
        self.title_label.bind("<B1-Motion>", self.drag_motion)

        # Utility Bar
        self.utility_bar = ctk.CTkFrame(
            master=self,
            height=35,
            corner_radius=0,
            fg_color="transparent",
        )
        
        self.utility_bar.grid_propagate(False)
        self.utility_bar.grid(row=1, column=0, sticky="ew")
        self.utility_bar.grid_columnconfigure(1, weight=1)
        self.utility_bar.grid_rowconfigure(0, weight=1)

        self.clear_btn = ctk.CTkButton(
            self.utility_bar,
            text="Clear all",
            font=self.app_font,
            width=60,
            height=30,
            corner_radius=6,
            fg_color=self.button_colorset,
            text_color=self.text_colorset,
            hover_color="blue",
            command=self.clear_content
        )
        self.clear_btn.grid(row=0, column=1, sticky="e", padx=10, pady=6)

        # Copy Content
        self.copy_content_frame = ctk.CTkScrollableFrame(
            master=self, 
            width=400,
            height=320,
            fg_color="transparent"
        )
        self.copy_content_frame.grid(row=2, column=0, pady=16, sticky="ew")
        self.copy_content_frame._scrollbar.configure(width=12)
        self.copy_content_frame.grid_columnconfigure(0, weight=1)
        self.copy_content_frame.grid_rowconfigure(0, weight=1)
        
        self.render_content()
        self.start_clipboard_listener()
        self.start_hotkey_listener()

    def start_hotkey_listener(self):
        """
        Allows Paperweight to listen for a specific keybind that will open the window.
        """
        def on_press():
            def show():
                self.deiconify()
                self.lift()
                self.focus_force()
            self.after(0, show)
        
        def listen():
            with keyboard.GlobalHotKeys({"<ctrl>+<alt>+v": on_press}) as hotkey:
                hotkey.join()

        hotkey_thread = threading.Thread(target=listen, daemon=True)
        hotkey_thread.start()

    def drag_start(self, event):
        """
        Gets the coordinates of the cursor proportional to the window.
        These coordinates act as the starting position of dragging the window.
        """
        self.start_x = event.x
        self.start_y = event.y

    def drag_motion(self, event):
        """
        Changes the position of the window by comparing the starting position of the cursor drag to the current position.
        Both positions are relative to the window's position.
        """
        x = self.winfo_x() + event.x - self.start_x
        y = self.winfo_y() + event.y - self.start_y
        self.geometry(f"+{x}+{y}")

    def render_content(self):
        """
        Creates a row of buttons for each individual copied content.
        In a single row, there is the copy button and delete button.
        """
        for widget in self.copy_content_frame.winfo_children():
            widget.destroy()

        if not self.copy_history:
            # Shows up when no items are in the copy history
            empty_label = ctk.CTkLabel(
                self.copy_content_frame,
                text="Nothing copied yet!\nCopy (Ctrl+C) something and it will show up here.",
                font=self.app_font,
                justify="center",
                fg_color="transparent",
                text_color="grey",
            )
            empty_label.grid(row=1, column=0, pady=20,  sticky="nsew")
        
        else:
            for i, item in enumerate(self.copy_history):
                display = item.strip()[:150] + "..." if len(item) > 150 else item.strip()

                button_row = ctk.CTkFrame(self.copy_content_frame, fg_color="transparent")
                button_row.grid(row=i, column=0, sticky="ew", padx=4, pady=2)
                button_row.grid_columnconfigure(0, weight=1)

                copy_btn = ctk.CTkLabel(
                    button_row,
                    text=display,
                    font=self.app_font,
                    width=343,
                    height=90,
                    anchor="nw",      
                    justify="left",
                    fg_color=self.button_colorset,
                    text_color=self.text_colorset,
                    padx=7,
                    pady=7,
                    corner_radius=6
                )

                copy_btn.grid_propagate(False)
                copy_btn.grid(row=i+1, column=0, padx=3)
                # e is used to consume Events. Without it, val and btn would be of type Event instead of String or CTkButton
                copy_btn.bind("<Button-1>", lambda e, val=item: self.copy_content(val))
                copy_btn.bind("<Enter>", lambda e, btn=copy_btn: btn.configure(fg_color=("#F4F4F4", "#434343")))
                copy_btn.bind("<Leave>", lambda e, btn=copy_btn: btn.configure(fg_color=self.button_colorset))
                
                delete_btn = ctk.CTkButton(
                    button_row,
                    text="🗑",
                    width=25,
                    height=45,
                    fg_color=self.button_colorset,
                    text_color=self.text_colorset,
                    hover_color="red",
                    command=lambda val=item: self.delete_content(val)
                )
                delete_btn.grid(row=i+1, column=1)
            
    def clear_content(self):
        """
        Deletes all content from Paperweight's copy history
        """
        self.copy_history.clear()
        self.render_content()

    def delete_content(self, value):
        """
        Deletes specified copied content from Paperweight's copy history
        """
        self.copy_history.remove(value)
        self.render_content()

    def copy_content(self, value):
        """
        Puts specified copied content to the computer's clipboard (to be pasted)
        """
        pyperclip.copy(value)
        
    def start_clipboard_listener(self):
        """
        Allows Paperweight to listen for unique copy content that goes into the computer's clipboard
        without disrupting CustomTkinter's main loop.
        """
        self.last_clip = pyperclip.paste()
        def poll():
            while True:
                try:
                    current = pyperclip.paste()
                    if current != self.last_clip and current.strip():
                        self.last_clip = current
                        if current not in self.copy_history:
                            self.copy_history.append(current)
                        if len(self.copy_history) > 100:
                            self.copy_history.pop(0)
                        self.after(0, self.render_content)
                except pyperclip.PyperclipException as e:
                    print(e)
                    pass #TODO: Could not be copied notif
                time.sleep(0.5) # Rate at which Paperweight updates the copy history (NOT renders)
        clipboard_thread = threading.Thread(target=poll, daemon=True)
        clipboard_thread.start()

app = App()
app.mainloop()