import customtkinter as ctk
import pyperclip
import threading
import time


MAX_HISTORY = 100

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
        self.overrideredirect(True) 

        self.history = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self, width=320, height=320)
        self.my_frame.grid(row=0, column=0)

        self.render_content()
        self.start_thread() 

    def render_content(self):
        for widget in self.my_frame.winfo_children():
            widget.destroy()

        for i, item in enumerate(self.history):
            display = item[:100] + "..." if len(item) > 100 else item

            row = ctk.CTkFrame(self.my_frame, fg_color="transparent")
            row.grid(row=i, column=0, sticky="ew", padx=4, pady=2)
            row.grid_columnconfigure(0, weight=1)
            btn = ctk.CTkButton(
                row,
                text=display,
                anchor="w",
                fg_color="grey",
                text_color=("black", "white"),
                hover_color=("green", "blue"),
                command=lambda val=item: self.copy_content(val)
            )
            btn.grid(row=i, column=0, sticky="ew", padx=3)

            delete_btn = ctk.CTkButton(
                row,
                text="x",
                width=25,
                height=25,
                anchor="center",
                fg_color="red",
                text_color=("black", "white"),
                hover_color=("green", "blue"),
                command=lambda val=item: self.delete_content(val)
            )
            delete_btn.grid(row=i, column=1)
            
    def delete_content(self, value):
        self.history.remove(value)
        self.render_content()

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
                        if current not in self.history:
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