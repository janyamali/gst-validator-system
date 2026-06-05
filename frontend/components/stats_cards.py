import customtkinter as ctk


class StatsCards(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        stats = [

            ("Invoices", "128"),

            ("Validated", "112"),

            ("Duplicates", "16"),

            ("Claims Matched", "98")
        ]

        for i, (title, value) in enumerate(stats):

            card = ctk.CTkFrame(

                self,

                width=250,

                height=140,

                corner_radius=20,

                fg_color="#102742"
            )

            card.grid(
                row=0,
                column=i,
                padx=15
            )

            card.grid_propagate(False)

            label = ctk.CTkLabel(

                card,

                text=title,

                font=("Arial", 18)
            )

            label.pack(
                pady=(30, 10)
            )

            value_label = ctk.CTkLabel(

                card,

                text=value,

                font=("Arial", 36, "bold")
            )

            value_label.pack()