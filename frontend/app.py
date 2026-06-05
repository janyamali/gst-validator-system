import customtkinter as ctk

from components.sidebar import Sidebar
from components.dashboard import Dashboard


ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")


class GSTValidatorApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("GST Validator")

        self.geometry("1600x900")

        self.configure(
            fg_color="#061226"
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.sidebar = Sidebar(self)

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.dashboard = Dashboard(self)

        self.dashboard.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )


if __name__ == "__main__":

    app = GSTValidatorApp()

    app.mainloop()