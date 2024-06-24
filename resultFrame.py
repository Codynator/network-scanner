from customtkinter import CTkScrollableFrame


class ResultFrame(CTkScrollableFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, label_text=title, label_font=("", 15), **kwargs)
        self.columnconfigure(0, weight=1)
