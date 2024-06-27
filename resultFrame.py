from customtkinter import CTkScrollableFrame


class ResultFrame(CTkScrollableFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, label_text=title, label_font=("monospace", 16), label_fg_color="transparent",
                         **kwargs)
