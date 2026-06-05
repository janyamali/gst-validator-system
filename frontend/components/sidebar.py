import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            width=260,
            corner_radius=0,
            fg_color="#08192D"
        )

        self.grid_rowconfigure(
            10,
            weight=1
        )

        logo = ctk.CTkLabel(
            self,
            text="GST Validator",
            font=("Arial", 28, "bold")
        )

        logo.pack(
            pady=(40, 30)
        )

        menu_items = [

            "Dashboard",

            "Upload Invoice",

            "My Invoices",

            "Validation",

            "Duplicates",

            "Claim Matching",

            "Reports",

            "Settings"
        ]

        for item in menu_items:

            btn = ctk.CTkButton(

                self,

                text=item,

                height=45,

                corner_radius=12,

                fg_color="transparent",

                hover_color="#123456",

                anchor="w",

                font=("Arial", 16)
            )

            btn.pack(
                fill="x",
                padx=20,
                pady=8
            )