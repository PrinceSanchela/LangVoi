"""
Embossed 3D Toolbar Strip Component for LangVoi Voice Studio Pro.
Features action tools, synchronized transport controls, presets,
and glowing high-precision digital timecode readout.
"""

import tkinter as tk
from app.theme import Theme


class ToolbarComponent(tk.Frame):
    def __init__(self, parent, actions: dict):
        super().__init__(parent, bg=Theme.BG_PANEL, relief="raised", bd=1, height=44)
        self.actions = actions

        # Action Buttons
        self._create_btn("📁 Open", actions.get("open"))
        self.btn_record = self._create_btn("🔴 Record", actions.get("record"))
        self._create_btn("📄 Export", actions.get("export"))

        self._separator()

        # Transport Buttons
        self.btn_play = self._create_btn("▶ Play", actions.get("play"))
        self.btn_pause = self._create_btn("⏸ Pause", actions.get("pause"))
        self.btn_stop = self._create_btn("⏹ Stop", actions.get("stop"))
        self.btn_loop = self._create_btn("🔁 Loop", actions.get("loop"))

        self._separator()

        # Digital LED Timecode Box
        box = tk.Frame(self, bg="#000000", relief="sunken", bd=2, padx=8, pady=2)
        box.pack(side="left", padx=6, pady=4)
        tk.Label(box, text="TIME", font=("Inter", 8, "bold"), fg="#555555", bg="#000000").pack(side="left", padx=(0, 6))
        self.lbl_timecode = tk.Label(box, text="00:00:00.000", font=Theme.FONT_DIGITAL_LARGE, fg=Theme.LCD_TEXT, bg="#000000")
        self.lbl_timecode.pack(side="left")

        self._separator()

        # Presets
        tk.Label(self, text="PRESETS:", font=Theme.FONT_LABEL, fg=Theme.TEXT_DIM, bg=Theme.BG_PANEL).pack(side="left", padx=4)
        self._create_btn("🇺🇸 EN", lambda: actions.get("load_sample")("sample_english_male.wav"))
        self._create_btn("🇪🇸 ES", lambda: actions.get("load_sample")("sample_spanish_female.wav"))
        self._create_btn("🇨🇳 ZH", lambda: actions.get("load_sample")("sample_tonal_mandarin.wav"))

        self._separator()

        self._create_btn("🌍 150+ Languages", actions.get("open_languages"))
        self._create_btn("❓ Help & Guide", actions.get("open_help"))

    def _create_btn(self, text, command):
        btn = tk.Button(self, text=text, command=command, font=Theme.FONT_SUBTITLE, bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN,
                        activebackground="#4a5366", activeforeground="#ffffff", relief="raised", bd=1, padx=8, pady=2)
        btn.pack(side="left", padx=2, pady=4)
        return btn

    def _separator(self):
        sep = tk.Frame(self, width=2, bg=Theme.BORDER_DARK, relief="sunken", bd=1)
        sep.pack(side="left", fill="y", padx=5, pady=6)

    def set_play_state(self, is_playing: bool, is_paused: bool = False):
        if is_playing:
            self.btn_play.config(bg="#15803d", fg="#ffffff", text="▶ Playing")
            self.btn_pause.config(bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, text="⏸ Pause")
        elif is_paused:
            self.btn_play.config(bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, text="▶ Play")
            self.btn_pause.config(bg=Theme.COLOR_AMBER, fg="#ffffff", text="⏸ Paused")
        else:
            self.btn_play.config(bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, text="▶ Play")
            self.btn_pause.config(bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, text="⏸ Pause")

    def set_loop_state(self, is_looping: bool):
        if is_looping:
            self.btn_loop.config(bg=Theme.COLOR_BLUE, fg="#ffffff", text="🔁 Loop ON")
        else:
            self.btn_loop.config(bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, text="🔁 Loop")

    def update_timecode(self, seconds: float):
        seconds = max(0.0, float(seconds))
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        self.lbl_timecode.config(text=f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}")
