"""
Hardware Stereo Dual-Channel LED Ladder VU Peak Meters.
Calibrated decibel ticks (0 dB CLIP, -6 dB, -12 dB, -24 dB, -48 dB).
"""

import tkinter as tk
from app.theme import Theme


class VUMetersComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#11141c", width=68, padx=4, pady=4)

        tk.Label(self, text="L   dB   R", font=("Consolas", 8, "bold"), fg=Theme.TEXT_MUTED, bg="#11141c").pack(side="top")

        meter_row = tk.Frame(self, bg="#11141c")
        meter_row.pack(side="top", fill="both", expand=True)

        self.canvas_l = tk.Canvas(meter_row, bg="#05070a", width=12, height=60, highlightthickness=1, highlightbackground="#202738")
        self.canvas_l.pack(side="left", padx=2, fill="y", expand=True)

        db_ticks = tk.Frame(meter_row, bg="#11141c")
        db_ticks.pack(side="left", fill="y")
        for tick in ["0", "-6", "-12", "-24", "-48"]:
            tk.Label(db_ticks, text=tick, font=("Consolas", 6), fg=Theme.TEXT_DIM, bg="#11141c").pack(expand=True)

        self.canvas_r = tk.Canvas(meter_row, bg="#05070a", width=12, height=60, highlightthickness=1, highlightbackground="#202738")
        self.canvas_r.pack(side="right", padx=2, fill="y", expand=True)

    def update_peaks(self, left_peak: float, right_peak: float):
        for canvas, peak in [(self.canvas_l, left_peak), (self.canvas_r, right_peak)]:
            canvas.delete("all")
            h = canvas.winfo_height()
            w = canvas.winfo_width()
            if h <= 5:
                continue

            num_leds = 18
            active_leds = min(num_leds, int(peak * 1.5 * num_leds))
            led_h = h / num_leds

            for i in range(num_leds):
                y = h - (i + 1) * led_h
                if i < active_leds:
                    color = Theme.COLOR_GREEN if i < 11 else (Theme.COLOR_AMBER if i < 15 else Theme.COLOR_RED)
                else:
                    color = "#121620"
                canvas.create_rectangle(1, y + 1, w - 1, y + led_h - 1, fill=color, outline="")
