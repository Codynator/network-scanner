from customtkinter import CTkScrollableFrame
from OSadaptationHandler import get_mono_font


class ResultFrame(CTkScrollableFrame):
    """
    A scrollable frame containing by default only title.
    """
    def __init__(self, master, title, **kwargs) -> None:
        super().__init__(master, label_text=title, label_font=(get_mono_font(), 16), label_fg_color="transparent",
                         **kwargs)
