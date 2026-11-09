"""
Master Audio Oscilloscope & Waveform Display Component for LangVoi Voice Studio Pro.
Features interactive click-to-play, click-and-drag scrubbing, dynamic real-time
waveform highlighting, precision decibel & time rulers, and neon laser playhead tracking.
"""

import tkinter as tk
import numpy as np
from app.theme import Theme


class OscilloscopeComponent(tk.Frame):
    def __init__(self, parent, on_seek_callback=None):
        super().__init__(parent, bg=Theme.BG_OSCILLOSCOPE, relief="sunken", bd=2)
        self.on_seek = on_seek_callback
        self.audio_raw = None
        self.duration = 0.0
        self.current_sec = 0.0
        self.bar_items = []
        self.bar_x_coords = []
        self.last_highlight_idx = 0

        # Assembly: Left dB ruler + Center Waveform canvas (with time ruler on top)
        self.db_ruler = tk.Frame(self, bg="#11141c", width=54)
        self.db_ruler.pack(side="left", fill="y")
        for val in ["+1.0 (0dB)", "+0.5 (-6dB)", " 0.0 (-inf)", "-0.5 (-6dB)", "-1.0 (0dB)"]:
            fg = Theme.COLOR_CYAN if "0.0" in val else Theme.TEXT_DIM
            tk.Label(self.db_ruler, text=val, font=("Consolas", 7), fg=fg, bg="#11141c").pack(expand=True, anchor="e", padx=2)

        # Waveform Canvas area
        self.canvas_wrap = tk.Frame(self, bg=Theme.BG_OSCILLOSCOPE)
        self.canvas_wrap.pack(side="left", fill="both", expand=True)

        # Time ruler
        self.time_ruler = tk.Canvas(self.canvas_wrap, bg="#11141c", height=14, highlightthickness=0)
        self.time_ruler.pack(side="top", fill="x")

        # Main canvas - flexible responsive height
        self.canvas = tk.Canvas(self.canvas_wrap, bg=Theme.BG_OSCILLOSCOPE, height=85, highlightthickness=0, cursor="crosshair")
        self.canvas.pack(side="top", fill="both", expand=True)

        # Bind events for instant interactive scrubbing and click-to-play
        self.canvas.bind("<Configure>", lambda e: self.redraw())
        self.canvas.bind("<Button-1>", self._handle_click)
        self.canvas.bind("<B1-Motion>", self._handle_drag)
        self.canvas.bind("<Motion>", self._handle_hover)
        self.canvas.bind("<Leave>", self._handle_leave)

    def set_audio(self, audio: np.ndarray, duration: float):
        """Set new audio data and trigger redraw."""
        self.audio_raw = audio
        self.duration = max(0.0, float(duration))
        self.current_sec = 0.0
        self.redraw()

    def set_playhead_time(self, seconds: float):
        """Update playhead position and waveform highlighting."""
        self.current_sec = max(0.0, min(self.duration, float(seconds)))
        self._update_playhead_and_highlights()

    def _handle_click(self, event):
        """Handle mouse click: jump playhead, highlight waveform, and start playing."""
        if self.duration <= 0 or self.audio_raw is None:
            return
        w = self.canvas.winfo_width()
        if w <= 1:
            return
        ratio = max(0.0, min(1.0, float(event.x) / float(w)))
        self.current_sec = ratio * self.duration
        self._update_playhead_and_highlights()
        if self.on_seek:
            # start_play=True starts audio playback instantly from clicked position!
            self.on_seek(self.current_sec, start_play=True)

    def _handle_drag(self, event):
        """Handle mouse drag (scrubbing): jump playhead and scrub audio in real time."""
        if self.duration <= 0 or self.audio_raw is None:
            return
        w = self.canvas.winfo_width()
        if w <= 1:
            return
        ratio = max(0.0, min(1.0, float(event.x) / float(w)))
        self.current_sec = ratio * self.duration
        self._update_playhead_and_highlights()
        if self.on_seek:
            self.on_seek(self.current_sec, start_play=False)

    def _handle_hover(self, event):
        """Draw faint hover guidelines and cursor timestamp."""
        if self.duration <= 0 or self.audio_raw is None:
            return
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        hx = max(0, min(w, event.x))
        hover_sec = (hx / max(1, w)) * self.duration

        # Update hover guide line
        self.canvas.coords("hover_line", hx, 0, hx, h)
        self.canvas.coords("hover_text", min(w - 30, max(30, hx)), 10)
        self.canvas.itemconfigure("hover_text", text=f"{hover_sec:.2f}s")
        self.canvas.tag_raise("hover_line")
        self.canvas.tag_raise("hover_text")
        self.canvas.tag_raise("playhead")
        self.canvas.tag_raise("playhead_cap_top")
        self.canvas.tag_raise("playhead_cap_bottom")

    def _handle_leave(self, event):
        """Hide hover guidelines when mouse leaves canvas."""
        self.canvas.coords("hover_line", -10, 0, -10, 0)
        self.canvas.coords("hover_text", -100, 0)

    def _update_playhead_and_highlights(self):
        """Fast 60-FPS update of laser playhead and played waveform highlights."""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 10 or h <= 10 or self.duration <= 0:
            return

        split_x = (self.current_sec / max(0.001, self.duration)) * w

        # Update laser playhead line & triangular caps
        self.canvas.coords("playhead", split_x, 0, split_x, h)
        self.canvas.coords("playhead_cap_top", split_x - 5, 0, split_x + 5, 0, split_x, 8)
        self.canvas.coords("playhead_cap_bottom", split_x - 5, h, split_x + 5, h, split_x, h - 8)

        # Update waveform highlights (Played = Bright Cyan, Unplayed = Slate Gray)
        if self.bar_items:
            target_idx = min(len(self.bar_items), int((split_x / max(1, w)) * len(self.bar_items)))
            if target_idx != self.last_highlight_idx:
                start = min(self.last_highlight_idx, target_idx)
                end = max(self.last_highlight_idx, target_idx)
                for i in range(start, end):
                    col = Theme.COLOR_CYAN if i <= target_idx else "#475569"
                    self.canvas.itemconfigure(self.bar_items[i], fill=col)
                self.last_highlight_idx = target_idx

    def redraw(self):
        """Full canvas repaint of time ruler, grid, waveform, and playhead."""
        self.canvas.delete("all")
        self.time_ruler.delete("all")
        self.bar_items = []
        self.bar_x_coords = []
        self.last_highlight_idx = 0

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 10 or h <= 10:
            return

        # 1. Draw Time Ruler Ticks
        rw = self.time_ruler.winfo_width()
        if self.duration > 0 and rw > 20:
            ticks = 9
            for i in range(ticks):
                x = (i / (ticks - 1)) * rw
                sec = (i / (ticks - 1)) * self.duration
                self.time_ruler.create_line(x, 7, x, 14, fill="#3d4556")
                self.time_ruler.create_text(x + 2, 6, text=f"{sec:.1f}s", fill=Theme.TEXT_DIM, font=("Consolas", 7), anchor="sw")

        # 2. Draw Center Grid & dB Guides
        cy = h / 2
        self.canvas.create_line(0, cy, w, cy, fill="#1a202c", width=1)
        for y_rat in [0.25, 0.75]:
            self.canvas.create_line(0, h * y_rat, w, h * y_rat, fill="#111622", width=1, dash=(2, 4))

        if self.audio_raw is None or len(self.audio_raw) == 0:
            self.canvas.create_text(w / 2, cy, text="[ No Voice Audio Loaded - Click 'Open File...' or 'Record Voice' ]", fill=Theme.TEXT_DIM, font=Theme.FONT_SUBTITLE)
            return

        # 3. Draw Waveform Peaks
        num_bars = min(w, 800)
        step = max(1, len(self.audio_raw) // num_bars)
        split_x = (self.current_sec / max(0.001, self.duration)) * w

        for i in range(num_bars):
            chunk = self.audio_raw[i * step : (i + 1) * step]
            if len(chunk) == 0:
                continue
            peak = float(np.max(np.abs(chunk)))
            bar_h = max(2, peak * (h * 0.88))
            x = (i / num_bars) * w

            col = Theme.COLOR_CYAN if x <= split_x else "#475569"
            line_id = self.canvas.create_line(x, cy - bar_h / 2, x, cy + bar_h / 2, fill=col, width=1)
            self.bar_items.append(line_id)
            self.bar_x_coords.append(x)

        self.last_highlight_idx = min(len(self.bar_items), int((split_x / max(1, w)) * len(self.bar_items)))

        # 4. Hover Guide line (hidden initially)
        self.canvas.create_line(-10, 0, -10, h, fill="#38bdf8", width=1, dash=(2, 2), tags="hover_line")
        self.canvas.create_text(-100, 0, text="0.00s", font=("Consolas", 7, "bold"), fill="#38bdf8", tags="hover_text")

        # 5. Playhead Laser Line & Pointer Caps
        self.canvas.create_line(split_x, 0, split_x, h, fill=Theme.COLOR_PLAYHEAD, width=2, tags="playhead")
        self.canvas.create_polygon(split_x - 5, 0, split_x + 5, 0, split_x, 8, fill=Theme.COLOR_PLAYHEAD, outline="", tags="playhead_cap_top")
        self.canvas.create_polygon(split_x - 5, h, split_x + 5, h, split_x, h - 8, fill=Theme.COLOR_PLAYHEAD, outline="", tags="playhead_cap_bottom")
