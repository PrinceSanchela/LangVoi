# 📜 Changelog — LangVoi Voice Studio Pro

All notable changes to **LangVoi Voice Studio Pro** are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.2.0] — 2026-11-09

### ✨ Added
- **LangVoi Neural Whisper LID Engine**: Pure in-memory speech language identification pipeline capable of resolving 90+ spoken languages and dialects in real-time.
- **Multilingual Speech Transcripts**: Real-time spoken transcript generation, word count telemetry, and native writing script detection.
- **Unified 8-Instrument Telemetry Rack**: Added autocorrelation-based pitch tracking ($F_0$), closest musical note calculation (e.g. C3, A4), vocal register classification (Bass to Soprano), SNR computation, and rhythm classification.
- **150+ World Languages Directory**: Interactive searchable browser indexing world language ISO codes, linguistic families, speaker statistics, and geographic regions.
- **1-Click Native Windows Installer**: Created `Install_LangVoi.bat` and `install.ps1` for frictionless desktop installation, shortcut creation, and Windows uninstaller registration.
- **Inno Setup 6 Compiler Support**: Integrated professional script (`installer_script.iss`) for building self-contained standalone installers (`LangVoi_Studio_Setup_v2.2.exe`).
- **Comprehensive Test Suite**: Added 13 automated unit tests covering audio loading, DSP acoustics, database queries, and multi-tier LID fallbacks.
- **C# Native Launchers**: High-performance Win32 launcher binaries (`launcher.cs` and `installer.cs`) for silent execution without terminal console windows.

### 🛡️ Security & Privacy
- Zero telemetry spyware: 100% of audio processing and acoustic calculations occur locally in-memory.
- Added strict `.gitignore` safeguards preventing any private certificates or keys (`*.pfx`) from being committed to public repositories.

---

## [2.1.0] — 2026-11-08

### ✨ Added
- Multi-format audio loader supporting WAV (PCM, IEEE float, 24-bit, RF64), MP3, FLAC, OGG, and M4A via SoundFile and PyAV.
- Real-time stereo LED ladder VU peak meters with instantaneous dBFS tracking and 0 dB CLIP indicators.
- 64-band FFT spectral analyzer with real-time frequency heatmap visualization.

---

## [2.0.0] — 2026-11-01

### 🚀 Initial Public Architecture Release
- Modernized classic DAW user interface inspired by Sound Forge Pro and Adobe Audition.
- Built on Python 3.10+ native Tkinter with High-DPI Per-Monitor awareness.
- Vectorized NumPy DSP audio pipeline.
