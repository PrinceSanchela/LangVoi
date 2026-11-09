"""
Multi-Pane Windows Status Bar Component.
Displays real-time audio specs, language engine status, and keyboard lock indicators.
"""

import tkinter as tk
from app.theme import Theme


class StatusBarComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1a1e28", relief="sunken", bd=1, height=22)

        self.lbl_status = tk.Label(self, text="Ready. Multilingual acoustic discriminator active.", font=Theme.FONT_TEXT, fg=Theme.COLOR_GREEN, bg="#1a1e28", anchor="w")
        self.lbl_status.pack(side="left", fill="x", expand=True, padx=8)

        self.lbl_format = tk.Label(self, text="44,100 Hz | 16-Bit | Mono", font=Theme.FONT_MONO, fg=Theme.TEXT_MUTED, bg="#1a1e28", relief="ridge", bd=1, padx=6)
        self.lbl_format.pack(side="left", padx=2)

        self.lbl_langs = tk.Label(self, text="150+ World Languages Active", font=Theme.FONT_MONO, fg=Theme.TEXT_MUTED, bg="#1a1e28", relief="ridge", bd=1, padx=6)
        self.lbl_langs.pack(side="left", padx=2)

        tk.Label(self, text="NUM", font=("Consolas", 8, "bold"), fg=Theme.COLOR_CYAN, bg="#1a1e28", relief="ridge", bd=1, padx=4).pack(side="left", padx=2)

    def set_status(self, text: str):
        self.lbl_status.config(text=text)

    def set_format(self, text: str):
        self.lbl_format.config(text=text)
