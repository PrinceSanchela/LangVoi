"""
Spectral Laboratory Visualizer Component.
Provides real-time 64-band FFT Spectrum Analyzer,
2D Spectrogram Heatmap, and Pitch Melody Contour on a native canvas.
"""

import tkinter as tk
import numpy as np
from app.theme import Theme


class SpectralLabComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=Theme.BG_PANEL, relief="groove", bd=2)
        self.audio_raw = None
        self.duration = 0.0
        self.latest_metrics = None
        self.active_tab = "spectrum"

        # Header with Tab buttons
        hdr = tk.Frame(self, bg=Theme.BG_HEADER, height=22)
        hdr.pack(side="top", fill="x")

        tk.Label(hdr, text="● SPECTRAL LABORATORY VISUALIZER", font=Theme.FONT_SUBTITLE, fg=Theme.COLOR_GREEN, bg=Theme.BG_HEADER).pack(side="left", padx=6)

        self.tab_btns = {}
        for tab_id, tab_label in [("spectrum", "FFT Spectrum"), ("spectrogram", "2D Heatmap"), ("pitch", "Pitch Contour")]:
            btn = tk.Button(hdr, text=tab_label, font=("Inter", 8, "bold"), bg=Theme.BG_PANEL, fg=Theme.TEXT_MAIN, relief="raised", bd=1, padx=6, pady=1,
                            command=lambda t=tab_id: self.switch_tab(t))
            btn.pack(side="right", padx=2, pady=1)
            self.tab_btns[tab_id] = btn

        self.tab_btns["spectrum"].config(bg=Theme.COLOR_BLUE)

        # Canvas - flexible responsive height
        self.canvas = tk.Canvas(self, bg=Theme.BG_OSCILLOSCOPE, height=80, relief="sunken", bd=1, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=3, pady=3)
        self.canvas.bind("<Configure>", lambda e: self.redraw())

    def set_data(self, audio: np.ndarray, duration: float, metrics: dict):
        self.audio_raw = audio
        self.duration = duration
        self.latest_metrics = metrics
        self.redraw()

    def switch_tab(self, tab_id: str):
        self.active_tab = tab_id
        for tid, btn in self.tab_btns.items():
            btn.config(bg=Theme.COLOR_BLUE if tid == tab_id else Theme.BG_PANEL)
        self.redraw()

    def redraw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 10 or h <= 10:
            return

        if self.audio_raw is None or len(self.audio_raw) == 0:
            self.canvas.create_text(w / 2, h / 2, text="[ Spectral Visualizer Idle - Load Audio ]", fill=Theme.TEXT_DIM, font=Theme.FONT_SUBTITLE)
            return

        if self.active_tab == "spectrum":
            self._draw_fft_spectrum(w, h)
        elif self.active_tab == "spectrogram":
            self._draw_spectrogram_heatmap(w, h)
        elif self.active_tab == "pitch":
            self._draw_pitch_contour(w, h)

    def _draw_fft_spectrum(self, w, h):
        bars = 64
        bar_w = w / bars
        n_fft = 1024
        half = len(self.audio_raw) // 2
        segment = self.audio_raw[max(0, half - n_fft) : min(len(self.audio_raw), half + n_fft)]
        if len(segment) < n_fft:
            segment = np.pad(segment, (0, n_fft - len(segment)))

        fft_vals = np.abs(np.fft.rfft(segment * np.hanning(len(segment))))[:bars]
        max_val = np.max(fft_vals) + 1e-6

        for i in range(bars):
            norm = fft_vals[i] / max_val
            bar_h = norm * (h * 0.9)
            x0 = i * bar_w + 1
            x1 = x0 + bar_w - 2
            y0 = h - bar_h
            y1 = h

            color = Theme.COLOR_GREEN if norm < 0.6 else (Theme.COLOR_AMBER if norm < 0.85 else Theme.COLOR_RED)
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    def _draw_spectrogram_heatmap(self, w, h):
        if not self.latest_metrics or "spectrogram" not in self.latest_metrics:
            return
        matrix = self.latest_metrics["spectrogram"]
        t_bins = len(matrix)
        f_bins = len(matrix[0])
        cell_w = w / t_bins
        cell_h = h / f_bins

        for t in range(t_bins):
            for f in range(f_bins):
                val = matrix[t][f]
                x0 = t * cell_w
                y0 = h - (f + 1) * cell_h
                x1 = x0 + cell_w + 1
                y1 = y0 + cell_h + 1

                if val < 0.3:
                    r, g, b = int(val * 80), int(val * 150), int(100 + val * 400)
                elif val < 0.7:
                    r, g, b = int(30 + val * 200), int(80 + val * 200), int(200 - val * 100)
                else:
                    r, g, b = int(180 + val * 75), int(220 - val * 100), 40
                hex_col = f"#{min(255, r):02x}{min(255, g):02x}{min(255, b):02x}"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=hex_col, outline="")

    def _draw_pitch_contour(self, w, h):
        if not self.latest_metrics or "pitch_timeline" not in self.latest_metrics:
            return
        timeline = self.latest_metrics["pitch_timeline"]
        if not timeline:
            return

        min_f0, max_f0 = 60.0, 400.0
        for p in [100, 200, 300]:
            y = h - ((p - min_f0) / (max_f0 - min_f0)) * h
            self.canvas.create_line(0, y, w, y, fill="#1a2230", dash=(2, 4))
            self.canvas.create_text(25, y - 6, text=f"{p} Hz", fill=Theme.TEXT_DIM, font=("Consolas", 7))

        pts = []
        dur = max(0.001, self.duration)
        for pt in timeline:
            if pt["f0"] > 0:
                x = (pt["t"] / dur) * w
                y = h - ((pt["f0"] - min_f0) / (max_f0 - min_f0)) * h
                pts.extend([x, y])

        if len(pts) >= 4:
            self.canvas.create_line(pts, fill=Theme.COLOR_CYAN, width=2, smooth=True)
