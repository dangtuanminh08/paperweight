import customtkinter as ctk

class MyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)
        self.label = ctk.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Paperweight")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self, width=300, height=200)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20)

        self.btn = ctk.CTkButton(
            master=self.my_frame,
            text="Hello world!!",
            anchor="w",
            fg_color="transparent",
            text_color=("black", "white"),
            hover_color=("green", "blue"),
            command=lambda: print("Hello!!")
        )

        self.btn.grid(row=0, column=0)
app = App()
app.mainloop()