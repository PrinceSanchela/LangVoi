"""
Studio Microphone Recorder Subrack Component.
Manages microphone selection, live digital recording timer,
and real-time audio oscilloscope capture.
"""

import tkinter as tk
from tkinter import ttk
from app.theme import Theme
from core.audio_engine import AudioEngine


class RecorderPanelComponent(tk.Frame):
    def __init__(self, parent, on_toggle_rec_callback=None):
        super().__init__(parent, bg=Theme.BG_SUBRACK, relief="sunken", bd=1, padx=6, pady=3)
        self.on_toggle = on_toggle_rec_callback

        row = tk.Frame(self, bg=Theme.BG_SUBRACK)
        row.pack(fill="x")

        tk.Label(row, text="MIC INPUT:", font=Theme.FONT_LABEL, fg=Theme.TEXT_MUTED, bg=Theme.BG_SUBRACK).pack(side="left", padx=(0, 6))

        self.cbo_devices = ttk.Combobox(row, width=26, state="readonly")
        self.cbo_devices.pack(side="left", padx=(0, 8))
        self.populate_devices()

        self.btn_rec = tk.Button(row, text="● Record Voice", command=self._on_click, font=Theme.FONT_SUBTITLE, bg="#991b1b", fg="#ffffff", relief="raised", bd=1, padx=10, pady=1)
        self.btn_rec.pack(side="left", padx=4)

        self.lbl_timer = tk.Label(row, text="00:00.00", font=("Consolas", 11, "bold"), fg=Theme.COLOR_RED, bg=Theme.BG_SUBRACK)
        self.lbl_timer.pack(side="left", padx=8)

        self.lbl_hint = tk.Label(row, text="Speak in any worldwide language", font=("Inter", 8, "italic"), fg=Theme.TEXT_DIM, bg=Theme.BG_SUBRACK)
        self.lbl_hint.pack(side="left")

    def populate_devices(self):
        devices = AudioEngine.get_input_devices()
        dev_strings = [f"#{d['id']}: {d['name'][:28]}" for d in devices]
        self.cbo_devices["values"] = dev_strings
        if dev_strings:
            self.cbo_devices.current(0)

    def get_selected_device_id(self):
        sel = self.cbo_devices.get()
        if sel and sel.startswith("#"):
            try:
                return int(sel.split(":")[0].replace("#", ""))
            except:
                pass
        return None

    def _on_click(self):
        if self.on_toggle:
            self.on_toggle()

    def set_recording_state(self, is_recording: bool):
        if is_recording:
            self.btn_rec.config(text="■ Stop & Analyze", bg="#dc2626")
            self.lbl_hint.config(text="🔴 RECORDING IN PROGRESS... Speak in any worldwide language")
        else:
            self.btn_rec.config(text="● Record Voice", bg="#991b1b")
            self.lbl_hint.config(text="Processing recording and analyzing acoustics...")

    def update_timer(self, elapsed_sec: float):
        m = int(elapsed_sec // 60)
        s = int(elapsed_sec % 60)
        cs = int((elapsed_sec % 1) * 100)
        self.lbl_timer.config(text=f"{m:02d}:{s:02d}.{cs:02d}")
