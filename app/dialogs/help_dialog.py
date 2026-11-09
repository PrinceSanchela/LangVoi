"""
Comprehensive Interactive Help, User Manual & Architectural Overview Dialog.
High-Definition Studio Documentation for LangVoi Voice Studio Pro.
Designed & Engineered by Prince Sanchela.
Features:
- Single-instance (Singleton) Unified Knowledge Hub
- Screen-Aware Dynamic Auto-Sizing & Centering (No Manual Resizing Needed)
- Responsive Auto-Wrapping on Resize
- Integrated EULA & System Diagnostics
"""

import os
import sys
import platform
import tkinter as tk
from tkinter import ttk
from app.theme import Theme


class HelpDialog(tk.Toplevel):
    """Unified Single-Window Knowledge Center for LangVoi Voice Studio Pro."""
    _instance = None

    def __init__(self, parent, default_tab=0):
        super().__init__(parent)
        HelpDialog._instance = self

        self.title("LangVoi Voice Studio Pro — Official Documentation & Knowledge Hub")
        self.configure(bg=Theme.BG_ROOT)

        # -------------------------------------------------------------
        # 1. SMART SCREEN-AWARE AUTO-SIZING & CENTERING
        # -------------------------------------------------------------
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        # Responsive calculation based on physical screen resolution
        target_w = max(860, min(1200, int(screen_w * 0.78)))
        target_h = max(600, min(860, int(screen_h * 0.82)))

        pos_x = max(10, (screen_w - target_w) // 2)
        pos_y = max(10, (screen_h - target_h) // 2 - 25)

        self.geometry(f"{target_w}x{target_h}+{pos_x}+{pos_y}")
        self.minsize(780, 520)

        # Window Icon
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
        ico_path = os.path.join(assets_dir, "app_icon.ico")
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass

        # Registry for dynamic text auto-wrapping on resize
        self._wrapped_labels = []

        # -------------------------------------------------------------
        # 2. BRANDED HEADER BANNER
        # -------------------------------------------------------------
        banner = tk.Frame(self, bg=Theme.BG_HEADER, height=52, relief="raised", bd=1)
        banner.pack(side="top", fill="x")

        icon_lbl = tk.Label(banner, text="🎙️", font=("Segoe UI Emoji", 20), bg=Theme.BG_HEADER)
        icon_lbl.pack(side="left", padx=(16, 10))

        title_col = tk.Frame(banner, bg=Theme.BG_HEADER)
        title_col.pack(side="left", fill="both", expand=True, pady=6)
        tk.Label(
            title_col,
            text="LANGVOI VOICE STUDIO PRO — MASTER DOCUMENTATION & SYSTEM GUIDE",
            font=Theme.FONT_TITLE,
            fg=Theme.COLOR_CYAN,
            bg=Theme.BG_HEADER,
            anchor="w"
        ).pack(fill="x")
        tk.Label(
            title_col,
            text="Designed & Engineered by Prince Sanchela • Neural Whisper LID & Acoustic Biometrics",
            font=Theme.FONT_MONO,
            fg=Theme.TEXT_MUTED,
            bg=Theme.BG_HEADER,
            anchor="w"
        ).pack(fill="x")

        btn_close = tk.Button(
            banner,
            text="✕ Close",
            command=self._on_close,
            font=Theme.FONT_SUBTITLE,
            bg=Theme.BG_PANEL,
            fg=Theme.TEXT_MAIN,
            activebackground=Theme.COLOR_RED,
            activeforeground="#ffffff",
            relief="raised",
            bd=1,
            padx=12,
            pady=3
        )
        btn_close.pack(side="right", padx=16, pady=8)

        # -------------------------------------------------------------
        # 3. TABBED NOTEBOOK
        # -------------------------------------------------------------
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Help.TNotebook", background=Theme.BG_ROOT, borderwidth=0)
        style.configure(
            "Help.TNotebook.Tab",
            background=Theme.BG_PANEL,
            foreground=Theme.TEXT_MAIN,
            font=("Inter", 9, "bold"),
            padding=[10, 6]
        )
        style.map(
            "Help.TNotebook.Tab",
            background=[("selected", Theme.COLOR_BLUE)],
            foreground=[("selected", "#ffffff")]
        )

        self.nb = ttk.Notebook(self, style="Help.TNotebook")
        self.nb.pack(fill="both", expand=True, padx=8, pady=8)

        # Create all 8 unified documentation tabs
        self.tab_quickstart = self._create_scrollable_tab("🚀 Quick Start")
        self.tab_lid = self._create_scrollable_tab("🌐 Language Detection")
        self.tab_acoustics = self._create_scrollable_tab("📊 Acoustic Biometrics")
        self.tab_racks = self._create_scrollable_tab("🎛️ Studio Hardware Racks")
        self.tab_shortcuts = self._create_scrollable_tab("⌨️ Shortcuts & Hotkeys")
        self.tab_license = self._create_scrollable_tab("📜 License (EULA)")
        self.tab_about = self._create_scrollable_tab("ℹ️ About & Diagnostics")
        self.tab_faq = self._create_scrollable_tab("❓ FAQ & Support")

        # Build contents
        self._build_quickstart()
        self._build_lid()
        self._build_acoustics()
        self._build_racks()
        self._build_shortcuts()
        self._build_license()
        self._build_about()
        self._build_faq()

        self.select_tab(default_tab)

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.transient(parent)
        self.lift()
        self.focus_force()

    def select_tab(self, tab_index: int):
        """Switches directly to a specific tab index and focuses the window."""
        try:
            self.nb.select(tab_index)
        except Exception:
            pass

    def _on_close(self):
        HelpDialog._instance = None
        self.destroy()

    def _create_scrollable_tab(self, label: str) -> tk.Frame:
        wrapper = tk.Frame(self.nb, bg=Theme.BG_ROOT)
        self.nb.add(wrapper, text=label)

        canvas = tk.Canvas(wrapper, bg=Theme.BG_ROOT, highlightthickness=0)
        scrollbar = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Theme.BG_ROOT, padx=16, pady=12)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_frame, width=event.width)
            # Dynamically recalculate wraplength for perfect responsiveness
            content_w = max(380, event.width - 36)
            for lbl in self._wrapped_labels:
                try:
                    if lbl.winfo_exists():
                        lbl.configure(wraplength=content_w)
                except Exception:
                    pass

        canvas.bind("<Configure>", _on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        return scrollable_frame

    # =========================================================================
    # TAB 1: QUICK START
    # =========================================================================
    def _build_quickstart(self):
        f = self.tab_quickstart
        self._sec_title(f, "🚀 Quick Start: 3 Steps to Full Audio Intelligence")
        self._p(f, "LangVoi Voice Studio Pro is a high-definition audio engineering workstation designed & engineered by Prince Sanchela. It combines classic studio mastering with instant speech language identification and laboratory acoustic biometrics.")

        self._step(f, "Step 1: Import or Record Audio", [
            ("📁 Open Audio File", "Click '📁 Open' or press Ctrl+O. Universally decodes WAV, MP3, M4A, FLAC, OGG, AAC, WMA, OPUS, and WebM audio formats."),
            ("🔴 Live Microphone", "Select your physical microphone from the dropdown under 'LIVE STUDIO MICROPHONE RECORDER', then click 'Record Voice' to record speech live with animated peak meters."),
            ("⚡ Bundled Presets", "Click the '🇺🇸 EN', '🇪🇸 ES', or '🇨🇳 ZH' preset buttons on the top toolbar for instant demonstration with genuine spoken speech.")
        ])

        self._step(f, "Step 2: Automated Analysis & Language Identification", [
            ("⚡ Automatic Execution", "The moment audio is loaded or recorded, LangVoi automatically runs its 3-tier intelligence pipeline:"),
            ("1. Acoustic DSP", "Profiles RMS amplitude, peak decibels, fundamental frequency (F0 pitch), and vocal registers in milliseconds."),
            ("2. Neural Whisper LID", "Resamples speech to 16 kHz in memory and detects the spoken language across 90+ world languages with real-time transcription."),
            ("3. Visualization", "Updates the Oscilloscope waveform, Stereo VU meters, 8 Telemetry instruments, and 64-band FFT Spectrogram.")
        ])

        self._step(f, "Step 3: Export Formal Lab Reports", [
            ("📄 Exporting Results", "Click '📄 Export' or press Ctrl+P to open the Export Laboratory Report wizard:"),
            ("• HTML Report", "A comprehensive, beautifully styled printable document with tables and full telemetry."),
            ("• JSON Data", "Full machine-readable raw metrics dictionary for database storage and AI workflows."),
            ("• CSV Export", "Tabular metrics suitable for Excel, scientific spreadsheets, and R statistical analysis.")
        ])

    # =========================================================================
    # TAB 2: LANGUAGE IDENTIFICATION
    # =========================================================================
    def _build_lid(self):
        f = self.tab_lid
        self._sec_title(f, "🌐 LangVoi Neural Whisper Language Identification Engine")
        self._p(f, "LangVoi incorporates an in-memory neural language identification pipeline powered by deep acoustic transformer architecture.")

        self._card(f, "Tier 1: Neural Whisper LID Engine (Primary High-Accuracy & Speed)", [
            "• 90+ Worldwide Languages: Recognizes Latin, Devanagari, Hanzi, Arabic, Cyrillic, Kana, Greek, Thai, and Hangul scripts.",
            "• 100% In-Memory Streaming: No external subprocesses or temporary files on disk. Pure native in-process Python HTTP transport.",
            "• 30-Second Attention Window: Whisper audio encoder processes speech log-Mel spectrograms, decoding the language token (<|en|>, <|es|>, <|zh|>) in under 2 seconds.",
            "• Verified Speech Transcription: Outputs recognized words, word counts, and speech duration alongside language identity.",
            "• 98%+ Confidence Rating: High statistical confidence supported by cross-verified acoustic validation."
        ])

        self._card(f, "Tier 2: Multi-Model Speech Probing (Secondary Fallback)", [
            "• Concurrent Probing: If the primary neural engine is unreachable, LangVoi launches parallel speech model probes across prioritized global language families.",
            "• Script & Vocabulary Validation: Cross-references transcript words against native frequency dictionaries to confirm lexical authenticity."
        ])

        self._card(f, "Tier 3: Autonomous Acoustic & Prosodic Profiler (Offline Zero-Network Fallback)", [
            "• 100% Offline Guarantee: Operates without any internet connection.",
            "• Biometric Prosody: Measures pitch standard deviation (ΔF0), tonal contour, zero-crossing rate (ZCR), syllable rhythm timing, and vocalic ratios to classify language families (Romance, Germanic, Sinitic, Slavic, Semitic, etc.)."
        ])

    # =========================================================================
    # TAB 3: ACOUSTIC TELEMETRY GUIDE
    # =========================================================================
    def _build_acoustics(self):
        f = self.tab_acoustics
        self._sec_title(f, "📊 Scientific Acoustic Telemetry & Biometrics Guide")
        self._p(f, "The central Telemetry Rack houses 8 laboratory-calibrated instruments computed directly by NumPy DSP autocorrelation and spectral analysis:")

        telemetry_items = [
            ("1. Fundamental Frequency (F0 Pitch)", "The physical rate of vocal fold vibration. Computed via autocorrelation on Hann-windowed speech frames. Shows mean pitch in Hertz (Hz), closest musical note (e.g. C3, A4), and vocal register (Bass, Baritone, Tenor, Alto, Soprano)."),
            ("2. Pitch Dynamics & Stability (ΔF0)", "Standard deviation of pitch variation. Tonal languages (Mandarin, Thai, Vietnamese) exhibit high variation (> 40 Hz), whereas monotone or stress-timed speech shows focused stability (15-25 Hz)."),
            ("3. Voice Activity Detection (VAD Ratio)", "Percentage of active spoken voice versus background silence and pauses. Indicates conversational density, fluency, and speech-to-pause ratios."),
            ("4. Syllable Rate & Rhythm Timing", "Estimated speaking tempo measured in syllables per second. Differentiates between Syllable-timed (Spanish, French), Stress-timed (English, German, Russian), and Mora-timed (Japanese) speech."),
            ("5. Signal-to-Noise Ratio (SNR dB)", "Ratio between active voice power and background noise floor. Values > 35 dB indicate Studio Reference Grade; 24-35 dB indicates Broadcast Quality; < 16 dB indicates noisy background."),
            ("6. Dynamic Range (dB)", "Calculated as the spread between the 95th percentile peak energy and 5th percentile noise floor. Quantifies expressive vocal dynamics and compression."),
            ("7. Zero-Crossing Rate (ZCR)", "The rate at which the audio waveform crosses zero amplitude. High ZCR (> 0.08) corresponds to unvoiced fricatives ('s', 'sh', 'f'); low ZCR indicates voiced vowel resonances."),
            ("8. Vocalic Ratio & Timbre Resonance", "Estimated percentage of vocal tract formant resonances versus unvoiced consonants. Reflects openness of vowels and linguistic phonotactics.")
        ]

        for name, desc in telemetry_items:
            self._item(f, name, desc)

    # =========================================================================
    # TAB 4: STUDIO HARDWARE RACKS
    # =========================================================================
    def _build_racks(self):
        f = self.tab_racks
        self._sec_title(f, "🎛️ Studio Hardware Racks & Workstation Interface")
        self._p(f, "LangVoi is styled as an authentic audio mastering workstation with hardware-grade controls:")

        racks = [
            ("Master Oscilloscope & Decibel Calibrated Waveform", "Vertical calibrated dB scale (+1.0 to -1.0 / 0 dB to -inf). Interactive scrubbing bar — click or drag anywhere to seek immediately. Live red playhead synchronized to high-precision hardware audio timers."),
            ("Dual Stereo LED Peak Meters", "Calibrated stereo Left (L) and Right (R) meters featuring green (-48 to -12 dB), amber (-12 to -6 dB), and red (0 dB CLIP) warning indicators."),
            ("LID-9000 Multilingual Discriminator LCD", "Backlit matrix screen displaying detected country flag, language name, native writing script, ISO-639 code, confidence score, and top candidate probability ladder."),
            ("64-Band FFT Spectral Lab & Pitch Contour", "Multi-view canvas featuring a 64-band real-time audio spectrum, 2D spectral time-frequency heatmap, and pitch contour (F0) overlay."),
            ("Live Studio Microphone Recorder", "Universal PC device picker, live VU meter animations, and precise recording timecode (00:00.00)."),
            ("Translation & Speech-to-Text Workbench", "Integrated transcript display with 1-click clipboard copy and multilingual translation engine.")
        ]

        for title, body in racks:
            self._item(f, title, body)

    # =========================================================================
    # TAB 5: SHORTCUTS & HOTKEYS
    # =========================================================================
    def _build_shortcuts(self):
        f = self.tab_shortcuts
        self._sec_title(f, "⌨️ Keyboard Shortcuts & Workflow Reference")
        self._p(f, "Use these shortcuts to accelerate your workflow without lifting your hands from the keyboard:")

        shortcuts = [
            ("Space", "Play / Pause Audio Playback"),
            ("Ctrl + O", "Open Audio File (Universal Loader)"),
            ("F5", "Re-run Full Acoustic Profiling & Language Identification"),
            ("Ctrl + P", "Export Laboratory Report (HTML, JSON, CSV)"),
            ("Ctrl + C", "Copy Recognized Speech Transcript to Clipboard"),
            ("Ctrl + L", "Open 150+ World Languages Directory"),
            ("Esc", "Stop Playback & Rewind to Beginning"),
            ("Home", "Seek Playhead to 0.0s (Start of Audio)"),
            ("F1", "Open this Master Knowledge Hub & Documentation")
        ]

        table = tk.Frame(f, bg=Theme.BG_SUBRACK, relief="sunken", bd=1)
        table.pack(fill="x", pady=8)

        h_row = tk.Frame(table, bg=Theme.BG_HEADER, pady=4)
        h_row.pack(fill="x")
        tk.Label(h_row, text="KEYBOARD SHORTCUT", font=Theme.FONT_SUBTITLE, fg=Theme.COLOR_CYAN, bg=Theme.BG_HEADER, width=22, anchor="w").pack(side="left", padx=8)
        tk.Label(h_row, text="ACTION / COMMAND", font=Theme.FONT_SUBTITLE, fg=Theme.TEXT_MAIN, bg=Theme.BG_HEADER, anchor="w").pack(side="left", padx=8)

        for key, desc in shortcuts:
            row = tk.Frame(table, bg=Theme.BG_SUBRACK, pady=3)
            row.pack(fill="x")
            lbl_key = tk.Label(row, text=key, font=("Consolas", 8, "bold"), fg="#ffffff", bg=Theme.BG_HEADER, width=16, padx=4, relief="raised", bd=1)
            lbl_key.pack(side="left", padx=8)
            tk.Label(row, text=desc, font=Theme.FONT_TEXT, fg=Theme.TEXT_MAIN, bg=Theme.BG_SUBRACK, anchor="w").pack(side="left", padx=8)

    # =========================================================================
    # TAB 6: LICENSE (EULA)
    # =========================================================================
    def _build_license(self):
        f = self.tab_license
        self._sec_title(f, "📜 Software License Agreement (EULA)")
        self._p(f, "LangVoi Voice Studio Pro is proprietary software created and engineered by Prince Sanchela. Review the official terms below:")

        box_frame = tk.Frame(f, bg="#080a10", relief="sunken", bd=1)
        box_frame.pack(fill="both", expand=True, pady=4)

        scrollbar = ttk.Scrollbar(box_frame, orient="vertical")
        txt = tk.Text(
            box_frame,
            bg="#080a10",
            fg="#e2e8f0",
            font=("Consolas", 9),
            relief="flat",
            wrap="word",
            height=16,
            yscrollcommand=scrollbar.set,
            padx=12,
            pady=10
        )
        scrollbar.config(command=txt.yview)
        txt.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Load LICENSE.txt
        lic_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "LICENSE.txt")
        if os.path.exists(lic_path):
            try:
                with open(lic_path, "r", encoding="utf-8", errors="replace") as lp:
                    content = lp.read()
            except Exception:
                content = "Could not read LICENSE.txt"
        else:
            content = "LangVoi Voice Studio Pro End-User License Agreement.\nCreated & Engineered by Prince Sanchela.\nCopyright © 2026 Prince Sanchela."

        txt.insert("1.0", content)
        txt.config(state="disabled")

    # =========================================================================
    # TAB 7: ABOUT & DIAGNOSTICS
    # =========================================================================
    def _build_about(self):
        f = self.tab_about
        self._sec_title(f, "ℹ️ About LangVoi Voice Studio Pro & System Diagnostics")
        self._p(f, "Official engineering metadata and live workstation hardware diagnostics:")

        badge_card = tk.Frame(f, bg=Theme.BG_HEADER, relief="raised", bd=1, padx=14, pady=10)
        badge_card.pack(fill="x", pady=(0, 10))

        tk.Label(badge_card, text="LangVoi Voice Studio Pro [Build 2.2 — HD Native Edition]", font=("Inter", 12, "bold"), fg="#ffffff", bg=Theme.BG_HEADER, anchor="w").pack(fill="x")
        tk.Label(badge_card, text="Lead Architect & Creator: Prince Sanchela", font=("Inter", 10, "bold"), fg=Theme.COLOR_AMBER, bg=Theme.BG_HEADER, anchor="w").pack(fill="x", pady=(2, 0))
        tk.Label(badge_card, text="Copyright © 2026 Prince Sanchela. All Worldwide Rights Reserved.", font=Theme.FONT_MONO, fg=Theme.TEXT_MUTED, bg=Theme.BG_HEADER, anchor="w").pack(fill="x")

        # Diagnostics Table
        diag_box = tk.Frame(f, bg=Theme.BG_SUBRACK, relief="sunken", bd=1, padx=12, pady=10)
        diag_box.pack(fill="x", pady=4)

        specs = [
            ("Lead Architect", "Prince Sanchela"),
            ("Architecture", "100% Pure Native Win32 Desktop Application (.EXE)"),
            ("Python Runtime", f"v{sys.version.split()[0]} ({platform.architecture()[0]})"),
            ("OS Environment", f"Windows {platform.release()} (Build {platform.version()})"),
            ("Acoustic DSP Core", "NumPy Vectorized Autocorrelation F0, SNR & Spectral FFT"),
            ("LID Neural Engine", "LangVoi Neural Whisper LID Engine (Pure In-Memory)"),
            ("Audio Hardware I/O", "SoundDevice + PyAudio WASAPI Direct Audio Streaming"),
            ("Display Engine", "Native Tkinter + Canvas DSP with Per-Monitor DPI Awareness")
        ]

        for k, v in specs:
            row = tk.Frame(diag_box, bg=Theme.BG_SUBRACK)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{k}:", font=("Inter", 8, "bold"), fg=Theme.COLOR_CYAN, bg=Theme.BG_SUBRACK, width=20, anchor="w").pack(side="left")
            tk.Label(row, text=v, font=("Consolas", 8), fg="#ffffff", bg=Theme.BG_SUBRACK, anchor="w").pack(side="left", fill="x", expand=True)

    # =========================================================================
    # TAB 8: FAQ & SUPPORT
    # =========================================================================
    def _build_faq(self):
        f = self.tab_faq
        self._sec_title(f, "❓ Frequently Asked Questions & Troubleshooting")

        faqs = [
            ("Q: How many languages does LangVoi support?",
             "A: LangVoi includes acoustic metadata and directory entries for 150+ worldwide spoken languages. The LangVoi Neural Whisper LID Engine directly identifies 90+ spoken languages and dialects."),
            ("Q: What audio formats can I import?",
             "A: LangVoi supports all standard desktop audio formats: WAV (PCM 16/24/32-bit, IEEE Float, RF64), MP3, M4A, AAC, FLAC, OGG, OPUS, WMA, AIFF, and WebM."),
            ("Q: Does it work without an internet connection?",
             "A: Yes! If offline, LangVoi automatically switches to its Tier 3 Autonomous Acoustic & Prosodic Profiler, which computes pitch stability, vocalic ratio, rhythm, and spectral dynamics locally using NumPy."),
            ("Q: How do I get the most accurate language detection results?",
             "A: Provide at least 5 to 10 seconds of clear spoken speech. Avoid pure silence, background music, or synthetic sine waves, as speech recognition requires phonetic vowel and consonant formants."),
            ("Q: Can I share this software with other Windows users?",
             "A: Yes. You can share 'LangVoi_Studio_v2.2_Package.zip'. Recipients simply unzip and double-click 'LangVoi_Studio.exe' or 'Install_LangVoi.bat' for a complete Windows desktop setup.")
        ]

        for q, a in faqs:
            box = tk.Frame(f, bg=Theme.BG_SUBRACK, relief="sunken", bd=1, padx=10, pady=8)
            box.pack(fill="x", pady=4)
            tk.Label(box, text=q, font=Theme.FONT_SUBTITLE, fg=Theme.COLOR_AMBER, bg=Theme.BG_SUBRACK, anchor="w").pack(fill="x")
            lbl_a = tk.Label(box, text=a, font=Theme.FONT_TEXT, fg=Theme.TEXT_MAIN, bg=Theme.BG_SUBRACK, anchor="w", justify="left")
            lbl_a.pack(fill="x", pady=(3, 0))
            self._wrapped_labels.append(lbl_a)

    # =========================================================================
    # UI HELPER METHODS WITH RESPONSIVE WRAP TRACKING
    # =========================================================================
    def _sec_title(self, parent, text):
        tk.Label(parent, text=text, font=Theme.FONT_TITLE, fg=Theme.COLOR_CYAN, bg=Theme.BG_ROOT, anchor="w").pack(fill="x", pady=(4, 6))

    def _p(self, parent, text):
        lbl = tk.Label(parent, text=text, font=Theme.FONT_TEXT, fg=Theme.TEXT_MUTED, bg=Theme.BG_ROOT, anchor="w", justify="left")
        lbl.pack(fill="x", pady=(0, 10))
        self._wrapped_labels.append(lbl)

    def _item(self, parent, title, desc):
        wrap = tk.Frame(parent, bg=Theme.BG_SUBRACK, relief="sunken", bd=1, padx=10, pady=6)
        wrap.pack(fill="x", pady=3)
        tk.Label(wrap, text=f"● {title}", font=Theme.FONT_SUBTITLE, fg=Theme.COLOR_GREEN, bg=Theme.BG_SUBRACK, anchor="w").pack(fill="x")
        lbl = tk.Label(wrap, text=desc, font=Theme.FONT_TEXT, fg=Theme.TEXT_MAIN, bg=Theme.BG_SUBRACK, anchor="w", justify="left")
        lbl.pack(fill="x", pady=(2, 0))
        self._wrapped_labels.append(lbl)

    def _step(self, parent, title, items):
        wrap = tk.Frame(parent, bg=Theme.BG_SUBRACK, relief="groove", bd=1, padx=10, pady=8)
        wrap.pack(fill="x", pady=4)
        tk.Label(wrap, text=title, font=Theme.FONT_TITLE, fg=Theme.COLOR_AMBER, bg=Theme.BG_SUBRACK, anchor="w").pack(fill="x", pady=(0, 4))
        for sub_title, text in items:
            row = tk.Frame(wrap, bg=Theme.BG_SUBRACK)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"▸ {sub_title}:", font=("Inter", 8, "bold"), fg=Theme.COLOR_CYAN, bg=Theme.BG_SUBRACK, width=22, anchor="w").pack(side="left")
            lbl = tk.Label(row, text=text, font=Theme.FONT_TEXT, fg=Theme.TEXT_MAIN, bg=Theme.BG_SUBRACK, anchor="w", justify="left")
            lbl.pack(side="left", fill="x", expand=True)
            self._wrapped_labels.append(lbl)

    def _card(self, parent, title, bullets):
        box = tk.Frame(parent, bg=Theme.BG_PANEL, relief="ridge", bd=2, padx=10, pady=8)
        box.pack(fill="x", pady=4)
        tk.Label(box, text=title, font=Theme.FONT_SUBTITLE, fg=Theme.COLOR_CYAN, bg=Theme.BG_PANEL, anchor="w").pack(fill="x", pady=(0, 4))
        for b in bullets:
            lbl = tk.Label(box, text=b, font=Theme.FONT_TEXT, fg=Theme.TEXT_MAIN, bg=Theme.BG_PANEL, anchor="w", justify="left")
            lbl.pack(fill="x", pady=1)
            self._wrapped_labels.append(lbl)


def show_help_dialog(parent, default_tab=0):
    """
    Singleton Knowledge Hub Launcher.
    If the dialog is already open, brings it to the front and switches to default_tab.
    If not, creates and centers a dynamically sized, screen-aware window.
    """
    if HelpDialog._instance and HelpDialog._instance.winfo_exists():
        dlg = HelpDialog._instance
        dlg.select_tab(default_tab)
        dlg.deiconify()
        dlg.lift()
        dlg.focus_force()
        return dlg

    return HelpDialog(parent, default_tab=default_tab)
