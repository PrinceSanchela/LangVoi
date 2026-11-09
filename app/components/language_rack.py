"""
LID-9000 Multilingual Discriminator Instrument Rack Component.
Displays backlit LCD screen with detected language, candidate ladder,
and recognized speech transcript.
"""

import tkinter as tk
from tkinter import ttk
from app.theme import Theme


class LanguageRackComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=Theme.BG_PANEL, relief="groove", bd=2)

        # Header
        hdr = tk.Frame(self, bg=Theme.BG_HEADER, height=22)
        hdr.pack(side="top", fill="x")
        tk.Label(hdr, text="● RACK: LID-9000 MULTILINGUAL ACOUSTIC DISCRIMINATOR", font=Theme.FONT_SUBTITLE, fg=Theme.COLOR_CYAN, bg=Theme.BG_HEADER).pack(side="left", padx=6)

        body = tk.Frame(self, bg=Theme.BG_PANEL, padx=6, pady=4)
        body.pack(fill="both", expand=True)

        # 1. Backlit LCD Matrix Screen
        self.lcd = tk.Frame(body, bg=Theme.BG_LCD, relief="sunken", bd=1, padx=8, pady=4)
        self.lcd.pack(fill="x", pady=(0, 4))

        top_row = tk.Frame(self.lcd, bg=Theme.BG_LCD)
        top_row.pack(fill="x")
        tk.Label(top_row, text="> PRIMARY DETECTED LANGUAGE:", font=("Consolas", 7, "bold"), fg=Theme.LCD_TEXT, bg=Theme.BG_LCD).pack(side="left")
        self.lbl_badge = tk.Label(top_row, text="AWAITING AUDIO", font=("Consolas", 7, "bold"), fg="#000000", bg=Theme.LCD_TEXT, padx=3)
        self.lbl_badge.pack(side="right")

        mid_row = tk.Frame(self.lcd, bg=Theme.BG_LCD)
        mid_row.pack(fill="x", pady=2)
        self.lbl_flag = tk.Label(mid_row, text="🌐", font=("Segoe UI Emoji", 20), bg=Theme.BG_LCD)
        self.lbl_flag.pack(side="left", padx=(0, 8))

        txt_col = tk.Frame(mid_row, bg=Theme.BG_LCD)
        txt_col.pack(side="left", fill="both", expand=True)
        self.lbl_name = tk.Label(txt_col, text="Awaiting Voice Input", font=("Inter", 12, "bold"), fg="#ffffff", bg=Theme.BG_LCD, anchor="w")
        self.lbl_name.pack(fill="x")
        self.lbl_native = tk.Label(txt_col, text="Open file or record to analyze", font=("Consolas", 8, "bold"), fg=Theme.LCD_TEXT, bg=Theme.BG_LCD, anchor="w")
        self.lbl_native.pack(fill="x")

        self.lbl_pills = tk.Label(self.lcd, text="Family: N/A • Script: N/A • Region: Worldwide", font=("Consolas", 7), fg=Theme.TEXT_MUTED, bg=Theme.BG_LCD)
        self.lbl_pills.pack(fill="x", pady=(2, 0))

        # 2. Candidate Probabilities Ladder
        tk.Label(body, text="MULTILINGUAL CANDIDATE PROBABILITIES (WORLDWIDE):", font=("Inter", 7, "bold"), fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL).pack(anchor="w", pady=(2, 1))

        self.ladder_box = tk.Frame(body, bg=Theme.BG_SUBRACK, relief="sunken", bd=1, padx=4, pady=3)
        self.ladder_box.pack(fill="x", pady=(0, 4))
        self.render_empty_candidates()

        # 3. Speech-to-Text Transcript Box (with internal scrollbar)
        t_hdr = tk.Frame(body, bg=Theme.BG_PANEL)
        t_hdr.pack(fill="x", pady=(2, 1))
        tk.Label(t_hdr, text="SPEECH-TO-TEXT & SCRIPT IDENTIFICATION:", font=("Inter", 7, "bold"), fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL).pack(side="left")
        self.btn_copy = tk.Button(t_hdr, text="📋 Copy", command=self._copy_transcript, font=("Inter", 7, "bold"), bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, relief="raised", bd=1, padx=5, pady=0)
        self.btn_copy.pack(side="right")

        t_box_wrap = tk.Frame(body, bg="#080a10")
        t_box_wrap.pack(fill="both", expand=True)
        t_scroll = ttk.Scrollbar(t_box_wrap, orient="vertical")
        self.txt_transcript = tk.Text(t_box_wrap, bg="#080a10", fg="#e2e8f0", font=Theme.FONT_MONO, height=3, relief="sunken", bd=1, wrap="word", yscrollcommand=t_scroll.set)
        t_scroll.config(command=self.txt_transcript.yview)
        self.txt_transcript.pack(side="left", fill="both", expand=True)
        t_scroll.pack(side="right", fill="y")
        self.txt_transcript.insert("1.0", "[ Spoken transcript will appear here when speech is identified. ]")

        # Telemetry footer under transcript
        self.lbl_transcript_meta = tk.Label(body, text="Words: 0 • Duration: 0s • Engine: LangVoi Neural Whisper LID", font=("Consolas", 7), fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL, anchor="w")
        self.lbl_transcript_meta.pack(fill="x", pady=(2, 0))
        self._active_pbar = None

    def set_loading_state(self, message="Scanning speech biometrics & transcribing speech..."):
        """Instantly clears old data and shows a live scanning state."""
        self.lbl_flag.config(text="🔄")
        self.lbl_name.config(text="Analyzing Spoken Voice...")
        self.lbl_native.config(text="Profiling acoustic prosody & matching 150+ language models...")
        self.lbl_badge.config(text="SCANNING & ANALYZING...", fg="#000000", bg="#f59e0b")
        self.lbl_pills.config(
            text="Pitch contour F0 • VAD analysis • Multilingual speech recognition & script detection"
        )

        for child in self.ladder_box.winfo_children():
            child.destroy()

        load_frame = tk.Frame(self.ladder_box, bg=Theme.BG_SUBRACK, pady=4)
        load_frame.pack(fill="x")
        self.lbl_ladder_status = tk.Label(load_frame, text=f"⚡ {message}", font=("Inter", 7, "bold"), fg=Theme.COLOR_CYAN, bg=Theme.BG_SUBRACK)
        self.lbl_ladder_status.pack(anchor="w", padx=4, pady=(0, 2))

        self._active_pbar = ttk.Progressbar(load_frame, mode="indeterminate", style="TProgressbar")
        self._active_pbar.pack(fill="x", expand=True, padx=4, pady=2)
        try:
            self._active_pbar.start(12)
        except Exception:
            pass

        self.txt_transcript.delete("1.0", "end")
        self.txt_transcript.insert("1.0", "[ Actively transcribing speech stream and decoding writing script across 150+ world languages... ]")
        self.lbl_transcript_meta.config(text="Words: Scanning... • Duration: Calculating... • Engine: LangVoi Neural Whisper LID")

    def update_results(self, lang_results: dict):
        if not lang_results:
            return

        if self._active_pbar:
            try:
                self._active_pbar.stop()
            except Exception:
                pass
            self._active_pbar = None

        primary = lang_results.get("primary", {})
        candidates = lang_results.get("candidates", [])

        self.lbl_flag.config(text=primary.get("flag", "🌐"))
        self.lbl_name.config(text=primary.get("name", "Unknown"))
        self.lbl_native.config(text=f"{primary.get('native_name', '')} • ISO: {primary.get('code', 'N/A').upper()}")
        self.lbl_badge.config(text=f"{primary.get('probability_pct', 0)}% CONFIDENCE", fg="#000000", bg=Theme.LCD_TEXT)
        self.lbl_pills.config(
            text=f"Family: {primary.get('family', 'N/A')} • Script: {primary.get('script', 'Latin')} • Region: {primary.get('region', 'Worldwide')}"
        )

        # Candidates ladder - display top 4 candidates cleanly
        for child in self.ladder_box.winfo_children():
            child.destroy()

        for cand in candidates[:4]:
            row = tk.Frame(self.ladder_box, bg=Theme.BG_SUBRACK, pady=1)
            row.pack(fill="x")

            txt = f"{cand.get('flag', '')} {cand.get('name', '')} ({cand.get('family', '')})"
            tk.Label(row, text=txt, font=("Inter", 7, "bold"), fg=Theme.TEXT_MAIN, bg=Theme.BG_SUBRACK, width=28, anchor="w").pack(side="left")

            pct = cand.get('probability_pct', 0)
            bar = ttk.Progressbar(row, maximum=100, value=pct, style="TProgressbar")
            bar.pack(side="left", fill="x", expand=True, padx=4)

            tk.Label(row, text=f"{pct}%", font=("Consolas", 7, "bold"), fg=Theme.COLOR_CYAN, bg=Theme.BG_SUBRACK, width=6, anchor="e").pack(side="right")

        # Transcript
        transcript_text = lang_results.get("transcript", "") or "[ No verbal speech transcript identified. Acoustic signature profiled. ]"
        self.txt_transcript.delete("1.0", "end")
        self.txt_transcript.insert("1.0", transcript_text)

        words = lang_results.get("word_count", 0)
        dur = lang_results.get("duration_sec", 0)
        method = lang_results.get("method", "LangVoi Neural Whisper LID")
        self.lbl_transcript_meta.config(text=f"Words: {words} • Duration: {dur}s • Engine: {method}")

    def render_empty_candidates(self):
        for child in self.ladder_box.winfo_children():
            child.destroy()
        tk.Label(self.ladder_box, text="[ No voice sample loaded. Please open a file or record. ]", font=("Inter", 8, "italic"), fg=Theme.TEXT_DIM, bg=Theme.BG_SUBRACK, pady=8).pack()

    def _copy_transcript(self):
        text = self.txt_transcript.get("1.0", "end").strip()
        if text and not text.startswith("[ No verbal"):
            self.clipboard_clear()
            self.clipboard_append(text)
            self.btn_copy.config(text="✓ Copied")
            self.after(1500, lambda: self.btn_copy.config(text="📋 Copy"))
