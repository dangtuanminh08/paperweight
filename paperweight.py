import customtkinter as ctk
import pyperclip
import threading
import time


MAX_HISTORY = 50

class MyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)
        self.grid_columnconfigure(0, weight=1) # For parent grid system
        self.label = ctk.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Paperweight")

        self.history = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self, width=300, height=200)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20)

        self.render_content()
        self.start_thread() 

        self.btn = ctk.CTkButton(
            master=self.my_frame,
            text="Hello world!!",
            anchor="w",
            fg_color="transparent",
            text_color=("black", "white"),
            hover_color=("green", "blue"),
            command=lambda val="Hello world!!": self.copy_content(val)
        )
        self.btn.grid(row=0, column=0, sticky="ew")

    def render_content(self):
        for widget in self.my_frame.winfo_children():
            widget.destroy()

        for i, item in enumerate(self.history):
            display = item[:60] + "..." if len(item) > 60 else item
            self.btn = ctk.CTkButton(
                master=self.my_frame,
                text=display,
                anchor="w",
                fg_color="transparent",
                text_color=("black", "white"),
                hover_color=("green", "blue"),
                command=lambda val=item: self.copy_content(val)
            )

            self.btn.grid(row=i, column=0, sticky="ew")

    def copy_content(self, value):
        pyperclip.copy(value)
        
    def start_thread(self):
        self.last_clip = pyperclip.paste()
        def poll():
            while True:
                try:
                    current = pyperclip.paste()
                    if current != self.last_clip and current.strip():
                        self.last_clip = current
                    if current in self.history:
                        self.history.remove(current)
                    self.history.append(current)
                    if len(self.history) > MAX_HISTORY:
                        self.history.pop(0)
                    self.after(0, self.render_content)
                except Exception as e:
                    print(e)
                    pass
                time.sleep(0.5)
        t = threading.Thread(target=poll, daemon=True)
        t.start()

app = App()
app.mainloop()