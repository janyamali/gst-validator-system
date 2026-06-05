import customtkinter as ctk

from tkinter import filedialog

import requests


API_URL = "https://gst-validator-system.onrender.com"


class UploadSection(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(

            parent,

            height=300,

            corner_radius=20,

            fg_color="#0E223A"
        )

        self.pack_propagate(False)

        title = ctk.CTkLabel(

            self,

            text="Upload Invoice",

            font=("Arial", 30, "bold")
        )

        title.pack(
            pady=(30, 20)
        )

        self.result_label = ctk.CTkTextbox(

            self,

            width=800,

            height=250,

            corner_radius=15
        )

        self.result_label.pack(
            pady=20,
            padx=20
        )

        upload_btn = ctk.CTkButton(

            self,

            text="Choose PDF",

            width=220,

            height=55,

            corner_radius=15,

            font=("Arial", 18),

            command=self.upload_invoice
        )

        upload_btn.pack(
            pady=(10, 30)
        )

    def upload_invoice(self):

        file_path = filedialog.askopenfilename(

            filetypes=[("PDF files", "*.pdf")]
        )

        if not file_path:

            return

        with open(file_path, "rb") as file:

            files = {

                "file": file
            }

            response = requests.post(

                f"{API_URL}/upload",

                files=files
            )

        result = response.json()

        self.result_label.delete(
            "1.0",
            "end"
        )

        self.result_label.insert(
            "end",
            str(result)
        )