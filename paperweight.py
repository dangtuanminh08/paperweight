import customtkinter as ctk
import pyperclip
import threading
import time

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Paperweight")
        self.overrideredirect(True) # Gets rid of the Windows title bar

        self.copy_history = [] 

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_bar = ctk.CTkFrame(
                        master=self,
                        height=35,
                        fg_color="transparent",
                        corner_radius=0
                    )
                
        self.title_bar.grid_propagate(False)
        self.title_bar.grid(row=0, column=0, sticky="ew")

        self.title_bar.bind("<ButtonPress-1>", self.drag_start)
        self.title_bar.bind("<B1-Motion>", self.drag_motion)

        self.copy_content_frame = ctk.CTkScrollableFrame(
                        master=self, 
                        width=400, 
                        height=320,
                        fg_color="transparent"
                    )
        
        self.copy_content_frame.grid(row=1, column=0, pady=16)

        self.render_content()
        self.start_thread()

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

        TODO: Pin button (copy will stay locally on the computer)
        """
        for widget in self.copy_content_frame.winfo_children():
            widget.destroy()

        for i, item in enumerate(self.copy_history):
            display = item[:100] + "..." if len(item) > 100 else item

            button_row = ctk.CTkFrame(self.copy_content_frame, fg_color="transparent")
            button_row.grid(row=i, column=0, sticky="ew", padx=4, pady=2)
            button_row.grid_columnconfigure(0, weight=1)

            copy_btn = ctk.CTkButton(
                button_row,
                text=display,
                anchor="w",
                fg_color="grey",
                text_color=("black", "white"),
                hover_color=("green", "blue"),
                command=lambda val=item: self.copy_content(val)
            )
            copy_btn.grid(row=i, column=0, sticky="ew", padx=3)

            delete_btn = ctk.CTkButton(
                button_row,
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
        """
        Deletes specified copied content from Paperweight's list
        """
        self.copy_history.remove(value)
        self.render_content()

    def copy_content(self, value):
        """
        Puts specified copied content to the computer's clipboard (to be pasted)
        """
        pyperclip.copy(value)
        
    def start_thread(self):
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
                except Exception as e:
                    print(e)
                    pass #TODO: Could not be copied notif
                time.sleep(0.5)
        t = threading.Thread(target=poll, daemon=True)
        t.start()

app = App()
app.mainloop()