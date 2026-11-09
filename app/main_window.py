"""
LangVoi Voice Studio Pro - Master Native Application Window.
Fully Responsive, High-Definition (HD) Scrollable Workbench with Native Windows Controls.
"""

import sys
import os
import time
import threading
import wave
import numpy as np

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from app.theme import Theme
from app.components import (
    OscilloscopeComponent,
    VUMetersComponent,
    LanguageRackComponent,
    TelemetryRackComponent,
    SpectralLabComponent,
    RecorderPanelComponent,
    ToolbarComponent,
    StatusBarComponent
)
from app.components.translation_panel import TranslationPanel
from app.dialogs import (
    show_languages_dialog,
    show_export_dialog,
    show_about_dialog,
    show_manual_dialog,
    show_license_dialog,
    show_help_dialog
)
from core.audio_engine import AudioEngine
from core.voice_analyzer import VoiceAnalyzer
from core.language_detector import LanguageDetector


class LangVoiMainWindow:
    """Master High-Definition Responsive & Scrollable Desktop Studio Window."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("LangVoi Voice Studio Pro - Native Desktop Audio Workstation")
        self.root.geometry("1280x720")
        self.root.minsize(960, 550)
        self.root.configure(bg=Theme.BG_ROOT)

        # Window & Taskbar Icon
        self._apply_app_icon()

        # Core State
        self.current_filename = "No file loaded"
        self.latest_metrics = None
        self.latest_analysis = None

        # Audio & Detection Engines
        self.audio_engine = AudioEngine()
        self.detector = LanguageDetector()

        # Build UI Architecture
        self._setup_ttk_styles()
        self._build_menu_bar()
        self._build_toolbar()
        self._build_status_bar()
        self._build_workbench()

        # Keyboard Bindings
        self._setup_shortcuts()

        # Start Real-time UI refresh loop (VU meters, playhead, timer)
        self._ui_refresh_loop()

    def _apply_app_icon(self):
        """Applies high-resolution minimal classic icon to window and Windows taskbar."""
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        ico_path = os.path.join(assets_dir, "app_icon.ico")
        png_path = os.path.join(assets_dir, "app_icon_256.png")
        if os.path.exists(ico_path):
            try:
                self.root.iconbitmap(ico_path)
            except Exception:
                pass
        if os.path.exists(png_path):
            try:
                self._icon_photo = tk.PhotoImage(file=png_path)
                self.root.iconphoto(True, self._icon_photo)
            except Exception:
                pass

    def _setup_ttk_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass
        style.configure("TProgressbar", thickness=6, troughcolor="#0b0e14", background="#0284c7")
        style.configure("TNotebook", background=Theme.BG_ROOT, borderwidth=0)
        style.configure("TNotebook.Tab", background=Theme.BG_HEADER, foreground="#cbd5e1", padding=[10, 4], font=Theme.FONT_SUBTITLE)
        style.map("TNotebook.Tab", background=[("selected", Theme.COLOR_BLUE)], foreground=[("selected", "#ffffff")])

    # =========================================================================
    # 1. NATIVE MENU BAR
    # =========================================================================
    def _build_menu_bar(self):
        mb = tk.Menu(self.root, bg=Theme.BG_PANEL, fg=Theme.TEXT_MAIN, activebackground=Theme.COLOR_BLUE, activeforeground="#ffffff", bd=1)

        # File
        m_file = tk.Menu(mb, tearoff=0, bg=Theme.BG_PANEL, fg=Theme.TEXT_MAIN, activebackground=Theme.COLOR_BLUE, activeforeground="#ffffff")
        m_file.add_command(label="Open Voice Audio File...", command=self.open_audio_file, accelerator="Ctrl+O")
        m_file.add_separator()
        m_file.add_command(label="Load Sample: English (Male)", command=lambda: self.load_sample("sample_english_male.wav"))
        m_file.add_command(label="Load Sample: Spanish (Female)", command=lambda: self.load_sample("sample_spanish_female.wav"))
        m_file.add_command(label="Load Sample: Tonal Mandarin", command=lambda: self.load_sample("sample_tonal_mandarin.wav"))
        m_file.add_separator()
        m_file.add_command(label="Export Laboratory Report...", command=self.export_report, accelerator="Ctrl+P")
        m_file.add_separator()
        m_file.add_command(label="Exit LangVoi Studio", command=self.root.quit, accelerator="Alt+F4")
        mb.add_cascade(label="File", menu=m_file)

        # Edit
        m_edit = tk.Menu(mb, tearoff=0, bg=Theme.BG_PANEL, fg=Theme.TEXT_MAIN, activebackground=Theme.COLOR_BLUE, activeforeground="#ffffff")
        m_edit.add_command(label="Copy Spoken Transcript", command=self.copy_transcript, accelerator="Ctrl+C")
        m_edit.add_separator()
        m_edit.add_command(label="Clear Audio & Reset", command=self.clear_audio)
        mb.add_cascade(label="Edit", menu=m_edit)

        # Transport
        m_trans = tk.Menu(mb, tearoff=0, bg=Theme.BG_PANEL, fg=Theme.TEXT_MAIN, activebackground=Theme.COLOR_BLUE, activeforeground="#ffffff")
        m_trans.add_command(label="Play / Pause", command=self.toggle_playback, accelerator="Space")
        m_trans.add_command(label="Stop & Rewind", command=self.stop_playback)
        m_trans.add_command(label="Start Microphone Recording", command=self.toggle_recording)
        m_trans.add_separator()
        m_trans.add_command(label="Toggle Loop Playback", command=self.toggle_loop)
        mb.add_cascade(label="Transport", menu=m_trans)

        # Analysis
        m_analysis = tk.Menu(mb, tearoff=0, bg=Theme.BG_PANEL, fg=Theme.TEXT_MAIN, activebackground=Theme.COLOR_BLUE, activeforeground="#ffffff")
        m_analysis.add_command(label="Run Full Acoustic Profiling", command=self.run_analysis, accelerator="F5")
        mb.add_cascade(label="Analysis", menu=m_analysis)

        # Languages
        m_lang = tk.Menu(mb, tearoff=0, bg=Theme.BG_PANEL, fg=Theme.TEXT_MAIN, activebackground=Theme.COLOR_BLUE, activeforeground="#ffffff")
        m_lang.add_command(label="Open World Languages Directory (150+)...", command=self.open_languages_directory)
        mb.add_cascade(label="Languages", menu=m_lang)

        # Help
        m_help = tk.Menu(mb, tearoff=0, bg=Theme.BG_PANEL, fg=Theme.TEXT_MAIN, activebackground=Theme.COLOR_BLUE, activeforeground="#ffffff")
        m_help.add_command(label="📖 Complete User Manual & Documentation...", command=lambda: self.open_help_tab(0), accelerator="F1")
        m_help.add_command(label="🚀 Quick Start & Studio Overview...", command=lambda: self.open_help_tab(0))
        m_help.add_command(label="🌐 LangVoi Neural Whisper LID Guide...", command=lambda: self.open_help_tab(1))
        m_help.add_command(label="📊 Acoustic Biometrics Reference Manual...", command=lambda: self.open_help_tab(2))
        m_help.add_command(label="🎛️ Studio Hardware Racks Guide...", command=lambda: self.open_help_tab(3))
        m_help.add_command(label="⌨️ Keyboard Shortcuts Reference...", command=lambda: self.open_help_tab(4))
        m_help.add_command(label="📜 End-User License Agreement (EULA)...", command=lambda: self.open_help_tab(5))
        m_help.add_command(label="ℹ️ About LangVoi Voice Studio Pro...", command=lambda: self.open_help_tab(6))
        m_help.add_command(label="❓ Frequently Asked Questions (FAQ)...", command=lambda: self.open_help_tab(7))
        mb.add_cascade(label="Help", menu=m_help)

        self.root.config(menu=mb)

    # =========================================================================
    # 2. EMBOSSED TOOLBAR
    # =========================================================================
    def _build_toolbar(self):
        actions = {
            "open": self.open_audio_file,
            "record": self.toggle_recording,
            "export": self.export_report,
            "play": self.play_audio,
            "pause": self.pause_audio,
            "stop": self.stop_playback,
            "loop": self.toggle_loop,
            "load_sample": self.load_sample,
            "open_languages": self.open_languages_directory,
            "open_help": lambda: self.open_help_tab(0)
        }
        self.toolbar = ToolbarComponent(self.root, actions)
        self.toolbar.pack(side="top", fill="x")

    # =========================================================================
    # 3. 100% RESPONSIVE WORKBENCH (NO SCROLLING - FITS COMPLETE SCREEN)
    # =========================================================================
    def _build_workbench(self):
        """Builds a 100% responsive, non-scrollable native DAW workstation layout."""
        workbench = tk.Frame(self.root, bg=Theme.BG_ROOT, padx=6, pady=4)
        workbench.pack(side="top", fill="both", expand=True)

        # 3 vertical responsive rows:
        # Row 0: Master Oscilloscope, Audio Ribbon & Transport (weight=3)
        # Row 1: Analytical Dashboard Split (weight=3)
        # Row 2: Translation Engine (weight=2)
        workbench.rowconfigure(0, weight=3)
        workbench.rowconfigure(1, weight=3)
        workbench.rowconfigure(2, weight=2)
        workbench.columnconfigure(0, weight=1)

        # ---------------------------------------------------------------------
        # TOP RACK: MASTER OSCILLOSCOPE, AUDIO I/O & TRANSPORT
        # ---------------------------------------------------------------------
        top_rack = tk.Frame(workbench, bg=Theme.BG_PANEL, relief="groove", bd=2)
        top_rack.grid(row=0, column=0, sticky="nsew", pady=(0, 4))

        # Header Bar
        hdr = tk.Frame(top_rack, bg=Theme.BG_HEADER, height=22)
        hdr.pack(side="top", fill="x")
        tk.Label(hdr, text="● MASTER AUDIO OSCILLOSCOPE & STEREO TRANSPORT [CH-1 / CH-2]", font=Theme.FONT_SUBTITLE, fg=Theme.COLOR_CYAN, bg=Theme.BG_HEADER).pack(side="left", padx=6)
        self.lbl_rack_specs = tk.Label(hdr, text="FILE: NONE • 44,100 Hz • 16-BIT • MONO", font=Theme.FONT_MONO, fg=Theme.TEXT_MUTED, bg=Theme.BG_HEADER)
        self.lbl_rack_specs.pack(side="right", padx=6)

        # Unified Audio Input Ribbon (Open File & Live Microphone on one sleek bar)
        input_ribbon = tk.Frame(top_rack, bg=Theme.BG_SUBRACK, pady=2, padx=6)
        input_ribbon.pack(side="top", fill="x", padx=4, pady=(2, 2))

        tk.Button(input_ribbon, text="📁 Open File...", command=self.open_audio_file, font=Theme.FONT_SUBTITLE, bg=Theme.COLOR_BLUE, fg="#ffffff", relief="raised", bd=1, padx=8, pady=1).pack(side="left", padx=(0, 6))
        tk.Label(input_ribbon, text="VOICE:", font=Theme.FONT_LABEL, fg=Theme.TEXT_MUTED, bg=Theme.BG_SUBRACK).pack(side="left", padx=(0, 4))
        self.lbl_loaded_name = tk.Label(input_ribbon, text="No voice file loaded. Click 'Open File...' or Record.", font=Theme.FONT_MONO, fg=Theme.TEXT_MAIN, bg=Theme.BG_SUBRACK)
        self.lbl_loaded_name.pack(side="left")

        self.recorder_panel = RecorderPanelComponent(input_ribbon, on_toggle_rec_callback=self.toggle_recording)
        self.recorder_panel.pack(side="right")

        # Oscilloscope & VU Meters (expands dynamically with available height)
        wf_assembly = tk.Frame(top_rack, bg=Theme.BG_OSCILLOSCOPE, relief="sunken", bd=1)
        wf_assembly.pack(side="top", fill="both", expand=True, padx=4, pady=2)

        self.oscilloscope = OscilloscopeComponent(wf_assembly, on_seek_callback=self._on_user_seek)
        self.oscilloscope.pack(side="left", fill="both", expand=True)

        self.vu_meters = VUMetersComponent(wf_assembly)
        self.vu_meters.pack(side="right", fill="y", padx=2, pady=2)

        # Transport Bar
        trans_bar = tk.Frame(top_rack, bg=Theme.BG_PANEL, height=28, relief="groove", bd=1)
        trans_bar.pack(side="top", fill="x", padx=4, pady=(0, 3))

        self.btn_play_main = tk.Button(trans_bar, text="▶ PLAY", command=self.play_audio, font=Theme.FONT_SUBTITLE, bg=Theme.COLOR_BLUE, fg="#ffffff", relief="raised", bd=1, padx=8, pady=1)
        self.btn_play_main.pack(side="left", padx=3, pady=2)

        self.btn_pause_main = tk.Button(trans_bar, text="⏸ PAUSE", command=self.pause_audio, font=Theme.FONT_SUBTITLE, bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, relief="raised", bd=1, padx=6, pady=1)
        self.btn_pause_main.pack(side="left", padx=2, pady=2)

        self.btn_stop_main = tk.Button(trans_bar, text="⏹ STOP", command=self.stop_playback, font=Theme.FONT_SUBTITLE, bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, relief="raised", bd=1, padx=6, pady=1)
        self.btn_stop_main.pack(side="left", padx=2, pady=2)

        self.btn_loop_main = tk.Button(trans_bar, text="🔁 LOOP", command=self.toggle_loop, font=Theme.FONT_SUBTITLE, bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, relief="raised", bd=1, padx=6, pady=1)
        self.btn_loop_main.pack(side="left", padx=2, pady=2)

        tk.Label(trans_bar, text="SPEED:", font=Theme.FONT_LABEL, fg=Theme.TEXT_DIM, bg=Theme.BG_PANEL).pack(side="left", padx=(10, 4))
        self.speed_btns = {}
        for spd in [0.5, 1.0, 1.25, 1.5, 2.0]:
            btn = tk.Button(trans_bar, text=f"{spd}x", command=lambda s=spd: self.set_speed(s), font=("Consolas", 8, "bold"), bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, relief="raised", bd=1, padx=3, pady=1)
            btn.pack(side="left", padx=1)
            self.speed_btns[spd] = btn
        self.speed_btns[1.0].config(bg=Theme.COLOR_BLUE, fg="#ffffff")

        # Volume slider with Mute button (Instant Real-time Audio Scaling)
        self.btn_mute = tk.Button(trans_bar, text="🔊", command=self.toggle_mute, font=("Inter", 9), bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, relief="flat", bd=0, padx=2)
        self.btn_mute.pack(side="right", padx=(2, 4))

        self.lbl_vol_val = tk.Label(trans_bar, text="100%", font=Theme.FONT_MONO, fg=Theme.TEXT_MUTED, bg=Theme.BG_PANEL, width=4)
        self.lbl_vol_val.pack(side="right")

        self.slider_vol = tk.Scale(trans_bar, from_=0, to=100, orient="horizontal", command=self._on_vol_change, bg=Theme.BG_PANEL, fg=Theme.TEXT_MAIN, highlightthickness=0, length=75, showvalue=0)
        self.slider_vol.set(100)
        self.slider_vol.pack(side="right", padx=2)

        tk.Label(trans_bar, text="VOL:", font=Theme.FONT_LABEL, fg=Theme.TEXT_DIM, bg=Theme.BG_PANEL).pack(side="right", padx=(6, 2))

        # ---------------------------------------------------------------------
        # BOTTOM SPLIT: MULTILINGUAL DISCRIMINATOR & TELEMETRY/SPECTRAL
        # ---------------------------------------------------------------------
        split_frame = tk.Frame(workbench, bg=Theme.BG_ROOT)
        split_frame.grid(row=1, column=0, sticky="nsew")

        split_frame.columnconfigure(0, weight=1)
        split_frame.columnconfigure(1, weight=1)
        split_frame.rowconfigure(0, weight=1)

        # Left Column: LID-9000 Multilingual Discriminator
        self.lang_rack = LanguageRackComponent(split_frame)
        self.lang_rack.grid(row=0, column=0, sticky="nsew", padx=(0, 3))

        # Right Column: Telemetry Matrix + Spectral Lab
        right_column = tk.Frame(split_frame, bg=Theme.BG_ROOT)
        right_column.grid(row=0, column=1, sticky="nsew", padx=(3, 0))

        right_column.rowconfigure(0, weight=0)
        right_column.rowconfigure(1, weight=1)
        right_column.columnconfigure(0, weight=1)

        self.telemetry_rack = TelemetryRackComponent(right_column)
        self.telemetry_rack.grid(row=0, column=0, sticky="nsew", pady=(0, 4))

        self.spectral_lab = SpectralLabComponent(right_column)
        self.spectral_lab.grid(row=1, column=0, sticky="nsew")

        # ---------------------------------------------------------------------
        # ROW 2: TRANSLATION ENGINE
        # ---------------------------------------------------------------------
        self.translation_panel = TranslationPanel(workbench, root_window=self.root)
        self.translation_panel.grid(row=2, column=0, sticky="nsew", pady=(4, 0))

    # =========================================================================
    # 4. MULTI-PANE STATUS BAR
    # =========================================================================
    def _build_status_bar(self):
        self.status_bar = StatusBarComponent(self.root)
        self.status_bar.pack(side="bottom", fill="x")

    def _setup_shortcuts(self):
        self.root.bind("<space>", lambda e: self.toggle_playback())
        self.root.bind("<Control-o>", lambda e: self.open_audio_file())
        self.root.bind("<Control-O>", lambda e: self.open_audio_file())
        self.root.bind("<Control-p>", lambda e: self.export_report())
        self.root.bind("<Control-P>", lambda e: self.export_report())
        self.root.bind("<Control-l>", lambda e: self.open_languages_directory())
        self.root.bind("<Control-L>", lambda e: self.open_languages_directory())
        self.root.bind("<F1>", lambda e: self.open_help_tab(0))
        self.root.bind("<F5>", lambda e: self.run_analysis())
        self.root.bind("<Escape>", lambda e: self.stop_playback())
        self.root.bind("<Home>", lambda e: self.seek_home())

    def open_help_tab(self, tab_index=0):
        from app.dialogs.help_dialog import show_help_dialog
        show_help_dialog(self.root, default_tab=tab_index)

    def seek_home(self):
        self.audio_engine.seek(0.0)
        self.oscilloscope.update_playhead(0.0)
        self.toolbar.update_timecode(0.0)

    # =========================================================================
    # AUDIO ACTIONS & PIPELINE
    # =========================================================================
    def open_audio_file(self):
        path = filedialog.askopenfilename(
            title="Open Voice Audio File",
            filetypes=[("Audio Files", "*.wav *.mp3 *.m4a *.flac *.ogg *.aac *.webm"), ("WAV Audio", "*.wav"), ("All Files", "*.*")]
        )
        if path:
            self.load_file(path)

    def load_sample(self, sample_filename: str):
        sample_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "samples", sample_filename)
        if os.path.exists(sample_path):
            self.load_file(sample_path)
        else:
            messagebox.showerror("Sample Not Found", f"Sample file not found at: {sample_path}")

    def load_file(self, filepath: str):
        try:
            self.audio_engine.stop_playback()
            self.status_bar.set_status(f"Loading {os.path.basename(filepath)}...")
            self.current_filename = os.path.basename(filepath)

            # Universal multi-format loader (MP3, M4A, AAC, WAV, FLAC, OGG, WMA, AIFF, WebM, etc.)
            audio, sr = VoiceAnalyzer.parse_audio(filepath)

            # Ensure mono audio for analysis and playback
            if audio.ndim > 1:
                mono_audio = np.mean(audio, axis=1).astype(np.float32)
                ch_text = f"{audio.shape[1]}-CH (STEREO)"
            else:
                mono_audio = audio.astype(np.float32)
                ch_text = "MONO"

            self.audio_engine.set_audio_data(mono_audio, sr)

            dur = self.audio_engine.duration
            ext = os.path.splitext(self.current_filename)[1].replace(".", "").upper() or "AUDIO"
            specs_text = f"FILE: {self.current_filename.upper()} • {ext} • {sr:,} Hz • 16-BIT • {ch_text} • {dur:.2f}s"
            self.lbl_rack_specs.config(text=specs_text)
            self.lbl_loaded_name.config(text=f"{self.current_filename} ({dur:.2f}s)")
            self.status_bar.set_format(f"{sr:,} Hz | 16-Bit | {ch_text}")

            # Update waveform
            self.oscilloscope.set_audio(mono_audio, dur)

            # Run Full Analysis
            self.run_analysis()

        except Exception as e:
            messagebox.showerror("Error Loading Audio", f"Could not load audio file:\n{str(e)}")
            self.status_bar.set_status("Error loading audio file.")

    def run_analysis(self):
        if self.audio_engine.audio_raw is None or len(self.audio_engine.audio_raw) == 0:
            messagebox.showinfo("No Audio", "Please open or record an audio file first.")
            return

        # 1. Immediately enter live scanning state and clear old results
        disp_name = getattr(self, "current_filename", "Audio File")
        self.lang_rack.set_loading_state(f"Scanning {disp_name} across 150+ languages...")
        self.telemetry_rack.set_loading_state()
        self.translation_panel.set_loading_state()
        self.status_bar.set_status("Analyzing voice acoustics & identifying spoken language...")
        self.root.update_idletasks()

        def _worker():
            try:
                # Step 1: Acoustic metrics
                self.root.after(0, lambda: self.status_bar.set_status("Step 1/3: Profiling acoustic biometrics, pitch & formants..."))
                metrics = VoiceAnalyzer.analyze_audio(self.audio_engine.audio_raw, self.audio_engine.sr)
                self.latest_metrics = metrics
                self.root.after(0, lambda: self.telemetry_rack.update_metrics(metrics))

                # Step 2: Speech-to-text and multilingual identification
                self.root.after(0, lambda: self.status_bar.set_status("Step 2/3: Transcribing speech & matching multilingual models..."))
                lang_res = self.detector.identify_language(
                    b'', metrics, audio_raw=self.audio_engine.audio_raw, sr_rate=self.audio_engine.sr
                )
                self.latest_analysis = lang_res

                # Step 3: Render final results
                self.root.after(0, lambda: self.status_bar.set_status("Step 3/3: Finalizing linguistic probabilities & report..."))
                self.root.after(0, self._render_results)
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.root.after(0, lambda: self.status_bar.set_status(f"Analysis error: {str(e)}"))

        threading.Thread(target=_worker, daemon=True).start()

    def _render_results(self):
        if not self.latest_metrics or not self.latest_analysis:
            return

        # Update language rack
        self.lang_rack.update_results(self.latest_analysis)

        # Update telemetry rack
        self.telemetry_rack.update_metrics(self.latest_metrics)

        # Update spectral lab
        self.spectral_lab.set_data(self.audio_engine.audio_raw, self.audio_engine.duration, self.latest_metrics)

        primary = self.latest_analysis.get("primary", {})
        transcript = self.latest_analysis.get("transcript", "")

        # Update translation panel with detected source language and recognized transcript
        self.translation_panel.set_source(
            primary.get("code", "auto"),
            primary.get("name", "Unknown"),
            transcript
        )

        self.status_bar.set_status(f"Analysis complete. Detected Language: {primary.get('name')} ({primary.get('probability_pct')}% confidence).")

    # =========================================================================
    # TRANSPORT & PLAYBACK
    # =========================================================================
    def toggle_playback(self):
        if self.audio_engine.is_playing:
            self.pause_audio()
        else:
            self.play_audio()

    def play_audio(self):
        if self.audio_engine.audio_raw is None or len(self.audio_engine.audio_raw) == 0:
            return
        self.audio_engine.play(on_ended_callback=self._on_playback_ended)
        self.btn_play_main.config(bg="#15803d", fg="#ffffff", text="▶ PLAYING")
        self.btn_pause_main.config(bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, text="⏸ PAUSE")
        self.toolbar.set_play_state(True, False)
        self.status_bar.set_status("Playing audio...")

    def pause_audio(self):
        self.audio_engine.pause()
        self.btn_play_main.config(bg=Theme.COLOR_BLUE, fg="#ffffff", text="▶ PLAY")
        self.btn_pause_main.config(bg=Theme.COLOR_AMBER, fg="#ffffff", text="⏸ PAUSED")
        self.toolbar.set_play_state(False, True)
        self.status_bar.set_status("Playback paused.")

    def stop_playback(self):
        self.audio_engine.stop_playback()
        self.btn_play_main.config(bg=Theme.COLOR_BLUE, fg="#ffffff", text="▶ PLAY")
        self.btn_pause_main.config(bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, text="⏸ PAUSE")
        self.toolbar.set_play_state(False, False)
        self.oscilloscope.set_playhead_time(0.0)
        self.toolbar.update_timecode(0.0)
        self.vu_meters.update_peaks(0.0, 0.0)
        self.status_bar.set_status("Playback stopped.")

    def toggle_loop(self):
        self.audio_engine.is_looping = not self.audio_engine.is_looping
        self.toolbar.set_loop_state(self.audio_engine.is_looping)
        if self.audio_engine.is_looping:
            self.btn_loop_main.config(bg=Theme.COLOR_BLUE, fg="#ffffff", text="🔁 LOOP ON")
        else:
            self.btn_loop_main.config(bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, text="🔁 LOOP")

    def toggle_mute(self):
        self.audio_engine.is_muted = not self.audio_engine.is_muted
        if self.audio_engine.is_muted:
            self.btn_mute.config(text="🔇", fg=Theme.COLOR_RED)
        else:
            self.btn_mute.config(text="🔊", fg=Theme.TEXT_MAIN)

    def set_speed(self, speed: float):
        self.audio_engine.set_speed(speed)
        for s, btn in self.speed_btns.items():
            if s == speed:
                btn.config(bg=Theme.COLOR_BLUE, fg="#ffffff")
            else:
                btn.config(bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN)

    def _on_vol_change(self, val):
        vol = float(val) / 100.0
        self.audio_engine.set_volume(vol)
        self.lbl_vol_val.config(text=f"{int(val)}%")
        if vol > 0 and self.audio_engine.is_muted:
            self.audio_engine.is_muted = False
            self.btn_mute.config(text="🔊", fg=Theme.TEXT_MAIN)

    def _on_user_seek(self, seconds: float, start_play: bool = False):
        """Called when user clicks or scrubs on the waveform visualizer."""
        self.audio_engine.seek(seconds, start_play=start_play)
        self.toolbar.update_timecode(seconds)
        if start_play:
            self.btn_play_main.config(bg="#15803d", fg="#ffffff", text="▶ PLAYING")
            self.btn_pause_main.config(bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, text="⏸ PAUSE")
            self.toolbar.set_play_state(True, False)

    def _on_playback_ended(self):
        """Called by audio engine worker when stream reaches the end."""
        def _reset_gui():
            self.btn_play_main.config(bg=Theme.COLOR_BLUE, fg="#ffffff", text="▶ PLAY")
            self.btn_pause_main.config(bg=Theme.BG_HEADER, fg=Theme.TEXT_MAIN, text="⏸ PAUSE")
            self.toolbar.set_play_state(False, False)
            self.oscilloscope.set_playhead_time(0.0)
            self.toolbar.update_timecode(0.0)
            self.vu_meters.update_peaks(0.0, 0.0)
            self.status_bar.set_status("Playback ended.")
        self.root.after(0, _reset_gui)

    # =========================================================================
    # RECORDING
    # =========================================================================
    def toggle_recording(self):
        if self.audio_engine.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        dev_id = self.recorder_panel.get_selected_device_id()
        self.recorder_panel.set_recording_state(True)

        def _live_cb(peak, frames):
            self.vu_meters.update_peaks(peak, peak * 0.94)

        self.audio_engine.start_recording(device_id=dev_id, live_peak_callback=_live_cb)

    def stop_recording(self):
        self.recorder_panel.set_recording_state(False)
        audio, sr = self.audio_engine.stop_recording()
        if audio is not None and len(audio) > 0:
            self.current_filename = f"Live_Record_{int(time.time())}.wav"
            dur = self.audio_engine.duration
            self.lbl_rack_specs.config(text=f"FILE: {self.current_filename.upper()} • {sr} Hz • 16-BIT • MONO • {dur:.2f}s")
            self.lbl_loaded_name.config(text=f"{self.current_filename} ({dur:.2f}s)")
            self.oscilloscope.set_audio(audio, dur)
            self.run_analysis()

    # =========================================================================
    # DIALOG ACTIONS
    # =========================================================================
    def export_report(self):
        show_export_dialog(self.root, self.current_filename, self.latest_metrics, self.latest_analysis)

    def open_languages_directory(self):
        show_languages_dialog(self.root)

    def copy_transcript(self):
        self.lang_rack._copy_transcript()

    def clear_audio(self):
        self.audio_engine.stop_playback()
        self.audio_engine.audio_raw = None
        self.audio_engine.duration = 0.0
        self.current_filename = "No file loaded"
        self.lbl_rack_specs.config(text="FILE: NONE • 44,100 Hz • 16-BIT • MONO")
        self.lbl_loaded_name.config(text="No voice file loaded.")
        self.oscilloscope.set_audio(np.array([]), 0.0)
        self.lang_rack.render_empty_candidates()
        self.lang_rack.lbl_flag.config(text="🌐")
        self.lang_rack.lbl_name.config(text="Awaiting Voice Input")
        self.lang_rack.lbl_native.config(text="Open file or record to analyze")
        self.lang_rack.lbl_badge.config(text="AWAITING AUDIO", fg="#000000", bg=Theme.LCD_TEXT)
        self.lang_rack.txt_transcript.delete("1.0", "end")
        self.lang_rack.txt_transcript.insert("1.0", "[ Spoken transcript will appear here when speech is identified. ]")
        self.telemetry_rack.update_metrics({})
        self.translation_panel.set_loading_state()
        self.status_bar.set_status("Audio cleared.")

    # =========================================================================
    # REAL-TIME UI REFRESH LOOP (40 FPS Smooth Playhead & Peak Meters)
    # =========================================================================
    def _ui_refresh_loop(self):
        if self.audio_engine.is_playing:
            cur_sec = self.audio_engine.get_current_time()
            self.oscilloscope.set_playhead_time(cur_sec)
            self.toolbar.update_timecode(cur_sec)

            # High-speed responsive VU meters animation during playback
            p_l, p_r = self.audio_engine.get_playback_peaks()
            self.vu_meters.update_peaks(p_l, p_r)

        elif self.audio_engine.is_recording:
            elapsed = time.time() - self.audio_engine.rec_start_time
            self.recorder_panel.update_timer(elapsed)

        self.root.after(25, self._ui_refresh_loop)
