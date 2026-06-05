import customtkinter as ctk

from components.upload_section import UploadSection

from components.stats_cards import StatsCards


class Dashboard(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        title = ctk.CTkLabel(

            self,

            text="Welcome back!",

            font=("Arial", 40, "bold")
        )

        title.pack(
            anchor="w",
            pady=(10, 20)
        )

        subtitle = ctk.CTkLabel(

            self,

            text="Smart. Fast. Accurate GST Validation.",

            font=("Arial", 18),

            text_color="#A0A0A0"
        )

        subtitle.pack(
            anchor="w",
            pady=(0, 30)
        )

        stats = StatsCards(self)

        stats.pack(
            fill="x",
            pady=(0, 30)
        )

        upload = UploadSection(self)

        upload.pack(
            fill="both",
            expand=True
        )