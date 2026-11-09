"""
Translation Panel Component for LangVoi Voice Studio Pro.
Provides a professional translation interface to translate detected speech
transcripts into any of 75+ world languages with high accuracy.
"""

import tkinter as tk
from tkinter import ttk
from app.theme import Theme
from core.translator import Translator, TRANSLATION_LANGUAGES


class TranslationPanel(tk.Frame):
    """Professional translation panel with language selector and translated output."""

    def __init__(self, parent, root_window=None):
        super().__init__(parent, bg=Theme.BG_PANEL, relief="groove", bd=2)
        self.root_window = root_window
        self._source_lang = "auto"
        self._source_text = ""

        # Header
        hdr = tk.Frame(self, bg=Theme.BG_HEADER, height=22)
        hdr.pack(side="top", fill="x")
        tk.Label(
            hdr, text="● REAL-TIME SPEECH TRANSLATION ENGINE",
            font=Theme.FONT_SUBTITLE, fg="#f59e0b", bg=Theme.BG_HEADER
        ).pack(side="left", padx=6)

        body = tk.Frame(self, bg=Theme.BG_PANEL, padx=6, pady=4)
        body.pack(fill="both", expand=True)

        # Control Row: Source Language | Arrow | Target Language Selector | Translate Button
        ctrl_row = tk.Frame(body, bg=Theme.BG_PANEL)
        ctrl_row.pack(fill="x", pady=(0, 4))

        # Source language indicator (auto-filled from detection)
        src_frame = tk.Frame(ctrl_row, bg=Theme.BG_SUBRACK, relief="sunken", bd=1, padx=6, pady=2)
        src_frame.pack(side="left")
        tk.Label(
            src_frame, text="SOURCE:", font=("Inter", 7, "bold"),
            fg=Theme.TEXT_DIM, bg=Theme.BG_SUBRACK
        ).pack(side="left")
        self.lbl_source_lang = tk.Label(
            src_frame, text="Auto-Detect", font=("Inter", 8, "bold"),
            fg=Theme.COLOR_CYAN, bg=Theme.BG_SUBRACK
        )
        self.lbl_source_lang.pack(side="left", padx=(4, 0))

        # Arrow
        tk.Label(
            ctrl_row, text="  ➤  ", font=("Segoe UI Emoji", 10),
            fg=Theme.COLOR_CYAN, bg=Theme.BG_PANEL
        ).pack(side="left")

        # Target language dropdown
        tgt_frame = tk.Frame(ctrl_row, bg=Theme.BG_SUBRACK, relief="sunken", bd=1, padx=6, pady=2)
        tgt_frame.pack(side="left")
        tk.Label(
            tgt_frame, text="TARGET:", font=("Inter", 7, "bold"),
            fg=Theme.TEXT_DIM, bg=Theme.BG_SUBRACK
        ).pack(side="left")

        # Build sorted language list for dropdown
        self._lang_items = sorted(TRANSLATION_LANGUAGES.items(), key=lambda x: x[1])
        self._lang_display = [f"{v}" for _, v in self._lang_items]
        self._lang_codes = [k for k, _ in self._lang_items]

        self.target_var = tk.StringVar(value="English")
        self.combo_target = ttk.Combobox(
            tgt_frame, textvariable=self.target_var,
            values=self._lang_display, state="readonly",
            width=28, font=("Inter", 8)
        )
        self.combo_target.pack(side="left", padx=(4, 0))
        self.combo_target.set("English")

        # Translate Button
        self.btn_translate = tk.Button(
            ctrl_row, text="🌐 TRANSLATE", font=("Inter", 8, "bold"),
            bg=Theme.COLOR_BLUE, fg="#ffffff", relief="raised", bd=2,
            padx=12, pady=2, command=self._on_translate_click,
            activebackground="#0369a1", activeforeground="#ffffff", cursor="hand2"
        )
        self.btn_translate.pack(side="left", padx=(10, 0))

        # Copy Translation Button
        self.btn_copy = tk.Button(
            ctrl_row, text="📋 Copy", font=("Inter", 7, "bold"),
            bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, relief="raised", bd=1,
            padx=5, pady=2, command=self._copy_translation
        )
        self.btn_copy.pack(side="right")

        # Translated Output Text Box (with scrollbar)
        out_hdr = tk.Frame(body, bg=Theme.BG_PANEL)
        out_hdr.pack(fill="x", pady=(2, 1))
        tk.Label(
            out_hdr, text="TRANSLATED OUTPUT:", font=("Inter", 7, "bold"),
            fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL
        ).pack(side="left")
        self.lbl_status = tk.Label(
            out_hdr, text="", font=("Consolas", 7),
            fg=Theme.TEXT_DIM, bg=Theme.BG_PANEL
        )
        self.lbl_status.pack(side="right")

        out_box = tk.Frame(body, bg="#080a10")
        out_box.pack(fill="both", expand=True)
        t_scroll = ttk.Scrollbar(out_box, orient="vertical")
        self.txt_output = tk.Text(
            out_box, bg="#080a10", fg="#e2e8f0", font=Theme.FONT_MONO,
            height=3, relief="sunken", bd=1, wrap="word",
            yscrollcommand=t_scroll.set
        )
        t_scroll.config(command=self.txt_output.yview)
        self.txt_output.pack(side="left", fill="both", expand=True)
        t_scroll.pack(side="right", fill="y")
        self.txt_output.insert("1.0", "[ Translation will appear here. Select a target language and click TRANSLATE. ]")

    def set_source(self, lang_code: str, lang_name: str, transcript: str):
        """Called by main window when detection is complete to set the source language and text."""
        self._source_lang = lang_code or "auto"
        self._source_text = transcript or ""
        display = f"{lang_name} ({lang_code.upper()})" if lang_name else "Auto-Detect"
        self.lbl_source_lang.config(text=display)
        self.lbl_status.config(text="", fg=Theme.TEXT_DIM)

    def set_loading_state(self):
        """Clear previous translation during new audio analysis."""
        self.lbl_source_lang.config(text="Detecting...")
        self._source_text = ""
        self._source_lang = "auto"
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("1.0", "[ Waiting for language detection to complete... ]")
        self.lbl_status.config(text="", fg=Theme.TEXT_DIM)

    def _on_translate_click(self):
        """Handle translate button click."""
        if not self._source_text or not self._source_text.strip():
            self.txt_output.delete("1.0", "end")
            self.txt_output.insert("1.0", "[ No transcript available. Please load an audio file first. ]")
            return

        # Get selected target language code
        selected_display = self.target_var.get()
        target_code = "en"
        for code, display in self._lang_items:
            if display == selected_display:
                target_code = code
                break

        if target_code == self._source_lang:
            self.txt_output.delete("1.0", "end")
            self.txt_output.insert("1.0", f"[ Source and target language are the same ({target_code.upper()}). No translation needed. ]")
            return

        # Show translating state
        self.btn_translate.config(text="⏳ Translating...", state="disabled", bg="#6b7280")
        self.txt_output.delete("1.0", "end")
        self.txt_output.insert("1.0", f"[ Translating from {self._source_lang.upper()} to {target_code.upper()}... ]")
        self.lbl_status.config(text="Processing...", fg="#f59e0b")

        # Run translation asynchronously
        def _on_result(result):
            if self.root_window:
                self.root_window.after(0, lambda: self._display_result(result, target_code))

        Translator.translate_async(
            self._source_text, self._source_lang, target_code, _on_result
        )

    def _display_result(self, result: dict, target_code: str):
        """Display translation result on the GUI thread."""
        self.btn_translate.config(text="🌐 TRANSLATE", state="normal", bg=Theme.COLOR_BLUE)

        self.txt_output.delete("1.0", "end")
        if result.get("success"):
            translated = result.get("translated_text", "")
            self.txt_output.insert("1.0", translated)
            target_name = Translator.get_language_name(target_code)
            self.lbl_status.config(
                text=f"✓ Translated to {target_name}",
                fg="#22c55e"
            )
        else:
            error = result.get("error", "Unknown error")
            self.txt_output.insert("1.0", f"[ Translation failed: {error} ]")
            self.lbl_status.config(text="✗ Translation failed", fg="#ef4444")

    def _copy_translation(self):
        """Copy translated text to clipboard."""
        text = self.txt_output.get("1.0", "end").strip()
        if text and not text.startswith("[ "):
            self.clipboard_clear()
            self.clipboard_append(text)
            self.btn_copy.config(text="✓ Copied")
            self.after(1500, lambda: self.btn_copy.config(text="📋 Copy"))
