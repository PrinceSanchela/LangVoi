"""
Acoustic Biometrics & Voice Telemetry Rack Component.
Displays 8 Pro Hardware Telemetry KPI meters in a clean responsive grid.
"""

import tkinter as tk
from app.theme import Theme


class TelemetryRackComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=Theme.BG_PANEL, relief="groove", bd=2)

        # Header
        hdr = tk.Frame(self, bg=Theme.BG_HEADER, height=22)
        hdr.pack(side="top", fill="x")
        tk.Label(hdr, text="● ACOUSTIC BIOMETRICS & VOICE TELEMETRY MATRIX", font=Theme.FONT_SUBTITLE, fg=Theme.COLOR_GREEN, bg=Theme.BG_HEADER).pack(side="left", padx=6)

        body = tk.Frame(self, bg=Theme.BG_PANEL, padx=6, pady=4)
        body.pack(fill="both", expand=True)

        m_grid = tk.Frame(body, bg=Theme.BG_PANEL)
        m_grid.pack(fill="both", expand=True)

        self.kpi_labels = {}
        cards = [
            ("PITCH F0", "kpi_pitch", "0.0 Hz", "Range: 0 - 0 Hz"),
            ("VOCAL REGISTER", "kpi_register", "Unclassified", "Pitch Jitter: ±0 Hz"),
            ("SIGNAL-TO-NOISE (SNR)", "kpi_snr", "0.0 dB", "Studio Reference"),
            ("SPEAKING TEMPO", "kpi_tempo", "0 WPM", "0.0 syl/sec"),
            ("VOICE ACTIVITY (VAD)", "kpi_vad", "0.0%", "0 pauses (avg 0.0s)"),
            ("TIMBRE (CENTROID)", "kpi_timbre", "0 Hz", "Balanced Voice"),
            ("PEAK & RMS LOUDNESS", "kpi_loudness", "0.0 dBFS", "RMS: -0.0 dBFS"),
            ("DYNAMIC RANGE & ZCR", "kpi_dyn", "0.0 dB", "ZCR: 0.0000"),
        ]

        for i, (title, key, val, sub) in enumerate(cards):
            row = i // 4
            col = i % 4
            box = tk.Frame(m_grid, bg=Theme.BG_SUBRACK, relief="ridge", bd=1, padx=4, pady=2)
            box.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            m_grid.grid_columnconfigure(col, weight=1)
            m_grid.grid_rowconfigure(row, weight=1)

            tk.Label(box, text=title, font=("Inter", 7, "bold"), fg=Theme.TEXT_DIM, bg=Theme.BG_SUBRACK).pack(anchor="w")
            v_lbl = tk.Label(box, text=val, font=("Consolas", 10, "bold"), fg="#ffffff", bg=Theme.BG_SUBRACK)
            v_lbl.pack(anchor="w", pady=0)
            s_lbl = tk.Label(box, text=sub, font=("Consolas", 7), fg=Theme.TEXT_MUTED, bg=Theme.BG_SUBRACK)
            s_lbl.pack(anchor="w")
            self.kpi_labels[key] = (v_lbl, s_lbl)

    def set_loading_state(self):
        """Resets telemetry display to live calculating indicator during active analysis."""
        self._set_kpi("kpi_pitch", "Measuring...", "Autocorrelating F0 contour...")
        self._set_kpi("kpi_register", "Analyzing...", "Profiling vocal bands...")
        self._set_kpi("kpi_snr", "Measuring...", "Computing SNR & noise floor...")
        self._set_kpi("kpi_tempo", "Calculating...", "Tracking syllable cadence...")
        self._set_kpi("kpi_vad", "Scanning...", "Detecting speech frames...")
        self._set_kpi("kpi_timbre", "Analyzing...", "Computing spectral centroid...")
        self._set_kpi("kpi_loudness", "Measuring...", "Calculating peak & RMS...")
        self._set_kpi("kpi_dyn", "Measuring...", "Computing dynamic range...")

    def update_metrics(self, metrics: dict):
        if not metrics:
            return
        self._set_kpi("kpi_pitch", f"{metrics.get('avg_pitch_hz', 0)} Hz", f"Note: {metrics.get('musical_note', '--')} (Min/Max: {metrics.get('min_pitch_hz', 0)}-{metrics.get('max_pitch_hz', 0)} Hz)")
        self._set_kpi("kpi_register", metrics.get("vocal_register", "Unclassified"), f"Pitch Jitter: ±{metrics.get('pitch_std_hz', 0)} Hz")
        self._set_kpi("kpi_snr", f"{metrics.get('snr_db', 0)} dB", metrics.get("snr_quality", "Good"))
        self._set_kpi("kpi_tempo", f"{metrics.get('tempo_wpm', 0)} WPM", f"{metrics.get('syllables_per_sec', 0)} syl/s • {metrics.get('tempo_category', 'Moderate')}")
        self._set_kpi("kpi_vad", f"{metrics.get('speech_ratio_pct', 0)}%", f"{metrics.get('pauses_count', 0)} pauses (avg {metrics.get('avg_pause_sec', 0)}s)")
        self._set_kpi("kpi_timbre", f"{metrics.get('spectral_centroid_hz', 0)} Hz", metrics.get("timbre_profile", "Balanced"))
        self._set_kpi("kpi_loudness", f"{metrics.get('peak_dbfs', 0)} dBFS", f"RMS: {metrics.get('rms_dbfs', 0)} dBFS")
        self._set_kpi("kpi_dyn", f"{metrics.get('dynamic_range_db', 0)} dB", f"ZCR: {metrics.get('zero_crossing_rate', 0)}")

    def _set_kpi(self, key, val, sub):
        if key in self.kpi_labels:
            v_lbl, s_lbl = self.kpi_labels[key]
            v_lbl.config(text=val)
            s_lbl.config(text=sub)
