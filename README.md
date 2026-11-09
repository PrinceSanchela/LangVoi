# 🎙️ LangVoi Voice Studio Pro [v2.2.0]

<div align="center">

[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6?logo=windows&logoColor=white)](https://github.com/PrinceSanchela/LangVoi)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-22c55e.svg)](LICENSE.txt)
[![Tests](https://img.shields.io/badge/Tests-13%2F13%20Passing-brightgreen.svg)](tests/)
[![Languages](https://img.shields.io/badge/Languages-99%2B%20World%20Languages-8B5CF6.svg)](core/languages_db.py)

<br/>

<a href="https://codeprince.itch.io/langvoi-voice-studio-pro">
  <img src="https://img.shields.io/badge/Download_Installer-itch.io-fa5c5c?style=for-the-badge&logo=itchdotio&logoColor=white" height="38" alt="Download on itch.io" />
</a>
&nbsp;&nbsp;
<a href="https://codeprince.gumroad.com/l/langvoi">
  <img src="https://img.shields.io/badge/Get_Pro_Package-Gumroad-FF90E8?style=for-the-badge&logo=gumroad&logoColor=black" height="38" alt="Download on Gumroad" />
</a>
&nbsp;&nbsp;
<a href="https://www.buymeacoffee.com/princesanchela">
  <img src="https://img.shields.io/badge/Buy_Me_A_Coffee-Donate_☕-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" height="38" alt="Buy Me A Coffee" />
</a>
&nbsp;&nbsp;
<a href="https://github.com/sponsors/PrinceSanchela">
  <img src="https://img.shields.io/badge/Sponsor-GitHub_Sponsors-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white" height="38" alt="GitHub Sponsors" />
</a>

</div>

> **Enterprise-Grade Native Windows Audio Workstation, Digital Signal Processing (DSP) & Real-Time Neural Whisper Spoken-Language Identification.**  
> **Conceptualized, Architected, and Engineered by Prince Sanchela.**

---

## ⚡ Direct 1-Click Installer (For Non-Developers)

If you want to install and use LangVoi on your Windows computer with zero setup, zero terminal commands, and zero Python required:

<div align="center">

| Distribution Channel | Description | Link |
| :--- | :--- | :---: |
| 🎮 **itch.io** | Single `LangVoi_Setup.exe` (Pay what you want / Free) | [**Download on itch.io**](https://codeprince.itch.io/langvoi-voice-studio-pro) |
| 🛍️ **Gumroad** | Pro Standalone Package & Commercial License | [**Get on Gumroad**](https://codeprince.gumroad.com/l/langvoi) |
| 📦 **GitHub Releases** | Official v2.2.0 Standalone Assets | [**GitHub Releases**](https://github.com/PrinceSanchela/LangVoi/releases/tag/v2.2.0) |

</div>

* **Single Executable Installer**: Download `LangVoi_Setup.exe` and double-click to install.
* **Zero Dependencies**: Bundles its own high-speed runtime, audio drivers, and neural speech models.
* **100% Offline & Private**: Zero external cloud calls — your audio stays strictly on your local PC.

---

## 📋 Table of Contents
1. [Overview & Philosophy](#-overview--philosophy)
2. [Workstation Interface](#-workstation-interface)
3. [Key Features](#-key-features)
4. [Developer Manual Setup Guide (From Source)](#-developer-manual-setup-guide-from-source)
5. [Automated Testing & Quality Assurance](#-automated-testing--quality-assurance)
6. [Codebase Architecture & Structure](#-codebase-architecture--structure)
7. [Supported Languages (99+ Global Languages)](#-supported-languages-99-global-languages)
8. [Keyboard Shortcuts Reference](#-keyboard-shortcuts-reference)
9. [Support, Sponsorship & Commercial Licensing](#-support-sponsorship--commercial-licensing)
10. [Community Supporters & Hall of Fame](#-community-supporters--hall-of-fame)
11. [Authorship & License](#-authorship--license)

---

## 🎯 Overview & Philosophy

**LangVoi Voice Studio Pro** is an open-source, high-performance audio workstation engineered by **Prince Sanchela**. 

Styled after classic mastering hardware and digital workstations (such as *Adobe Audition, Sound Forge Pro, and Cool Edit Pro*), it bridges hardware-level acoustic DSP with modern transformer speech artificial intelligence:

* **Universal Audio Codec Engine**: Direct streaming playback and decoding for WAV, MP3, M4A, AAC, FLAC, OGG, OPUS, WMA, AIFF, and WebM.
* **Low-Latency WASAPI Studio**: Low-jitter live microphone input with sample-accurate waveform visualization.
* **Neural Whisper LID Engine**: Ultra-fast, zero-cloud spoken-language identification resolving 99+ languages in under 2 seconds.
* **Laboratory Acoustic Biometrics**: Computes fundamental frequency ($F_0$), pitch stability (${\Delta}F_0$), vocal registers, Voice Activity Detection (VAD), dynamic range, and Signal-to-Noise Ratio (SNR).

---

## 🖥️ Workstation Interface

<img width="959" height="504" alt="Screenshot 2026-11-09 160155" src="https://github.com/user-attachments/assets/1e82d2a4-4100-4c0e-b9d1-8b47dcfa9bb0" />

## ✨ Key Features

### 1. 🧠 Neural Whisper LID Engine
* **In-Memory Streaming**: High-throughput neural language classification with zero disk writes.
* **99+ Global Languages**: Instant detection for English, Spanish, Hindi, French, German, Mandarin Chinese, Japanese, Russian, Arabic, Portuguese, Bengali, and 85+ others.
* **Confidence Scoring**: Probability distribution across top candidate languages.

### 2. 🎚️ Dual-Channel Master VU Meters
* Real-time Left and Right channel decibel monitors calibrated from **-60 dBFS to +6 dBFS**.
* High-precision peak indicators with smooth exponential decay ballistics.

### 3. 📊 64-Band Real-Time Spectral Lab
* Fast Fourier Transform (FFT) decomposing audio from 20 Hz to 20,000 Hz.
* Logarithmic frequency spacing matching the human ear's cochlear response.

### 4. 🔬 Acoustic Telemetry & Voice Biometrics
* **$F_0$ Pitch Tracking**: Real-time autocorrelation fundamental frequency tracking.
* **Vocal Register Classification**: Sub-bass, Bass, Baritone, Tenor, Alto, Mezzo-Soprano, Soprano.
* **Signal Metrics**: Voice Activity Detection (VAD), Zero-Crossing Rate (ZCR), Dynamic Range, and SNR.

---

## 🛠️ Developer Manual Setup Guide (From Source)

Developers, researchers, and audio engineers can run and modify LangVoi directly from the source code.

### Prerequisites
* **Operating System**: Windows 10 or Windows 11 (64-bit)
* **Python**: Python 3.10, 3.11, 3.12, 3.13, or 3.14
* **Git**: [Git for Windows](https://git-scm.com/download/win)

---

### Step-by-Step Installation:

#### 1. Clone the Repository
```powershell
git clone https://github.com/PrinceSanchela/LangVoi.git
cd LangVoi
```

#### 2. Create a Virtual Environment
```powershell
python -m venv .venv
```

#### 3. Activate the Virtual Environment
* On Windows PowerShell:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* On Windows Command Prompt (cmd):
  ```cmd
  .venv\Scripts\activate.bat
  ```

#### 4. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Launch LangVoi Voice Studio Pro
```powershell
python run.py
```
*(You can also run `python main.py` directly).*

---

## 🧪 Automated Testing & Quality Assurance

LangVoi includes a comprehensive automated test suite covering digital signal processing, audio loader codecs, neural language detection, and language database resolution.

Run all tests with:
```powershell
python -m unittest discover -s tests
```

Expected output:
```text
Ran 13 tests in 0.503s

OK
```

---

## 📂 Codebase Architecture & Structure

```text
LangVoi/
├── app/                        # Graphical User Interface (PyQt6)
│   ├── components/             # Reusable DAW Widgets & Racks
│   │   ├── oscilloscope.py     # Interactive waveform & timeline scrubber
│   │   ├── vu_meters.py        # Dual-channel peak/RMS VU meters
│   │   ├── spectral_lab.py     # 64-band FFT real-time spectrum analyzer
│   │   ├── language_rack.py    # Neural language detection display
│   │   ├── telemetry_rack.py   # Acoustic biometrics instruments
│   │   ├── recorder_panel.py   # Live microphone capture panel
│   │   ├── toolbar.py          # DAW transport controls
│   │   └── status_bar.py       # Engine status bar
│   ├── dialogs/                # Workstation Dialogs (About, Export, Help, Languages)
│   ├── main_window.py          # Master DAW Window & Event Bus
│   └── theme.py                # Midnight Slate / Cyan Hardware Styling
├── core/                       # Digital Signal Processing & Machine Learning Engine
│   ├── audio_engine.py         # Low-latency WASAPI audio playback & recording
│   ├── audio_loader.py         # Universal multi-format audio decoder
│   ├── language_detector.py    # Neural Whisper LID engine
│   ├── voice_analyzer.py       # Autocorrelation pitch tracking & acoustic DSP
│   └── languages_db.py         # Database of 99+ world languages & ISO-639 codes
├── assets/                     # High-resolution logos, badges, and application icons
├── samples/                    # Curated multi-lingual audio test samples (.wav)
├── tests/                      # Automated unit test suite (13 passing tests)
├── .github/                    # GitHub Actions workflows & FUNDING.yml
├── requirements.txt            # Production runtime dependencies
├── requirements-dev.txt        # Development & testing tooling
├── run.py                      # Main application bootstrap entrypoint
├── main.py                     # DAW engine coordinator
├── LICENSE.txt                 # MIT License & Terms of Service
└── README.md                   # Workstation documentation
```

---

## 🌐 Supported Languages (99+ Global Languages)

LangVoi detects and analyzes spoken audio across **99+ languages**, including:

| Region | Supported Languages |
| :--- | :--- |
| **Americas & Europe** | English, Spanish, French, German, Italian, Portuguese, Russian, Ukrainian, Polish, Dutch, Swedish, Norwegian, Danish, Finnish, Greek, Czech, Romanian, Hungarian, Bulgarian |
| **South Asia** | Hindi, Bengali, Punjabi, Gujarati, Marathi, Tamil, Telugu, Kannada, Malayalam, Urdu, Nepali, Sinhala |
| **East & Southeast Asia** | Mandarin Chinese, Cantonese, Japanese, Korean, Vietnamese, Thai, Indonesian, Malay, Tagalog/Filipino, Burmese, Khmer, Lao |
| **Middle East & Africa** | Arabic, Persian/Farsi, Hebrew, Turkish, Swahili, Amharic, Yoruba, Hausa, Zulu, Afrikaans |

---

## ⌨️ Keyboard Shortcuts Reference

| Shortcut | Action |
| :--- | :--- |
| `Ctrl + O` | Open Audio File (WAV, MP3, M4A, FLAC, OGG, OPUS, WMA, etc.) |
| `Space` | Toggle Audio Playback / Pause |
| `Ctrl + R` | Start / Stop Live Microphone Studio Recording |
| `Ctrl + L` | Re-run Neural Language Identification |
| `Ctrl + E` | Export Laboratory Telemetry & Voice Biometrics Report |
| `F1` | Open Interactive Help Documentation |
| `Ctrl + Q` | Safely Exit Application |

---

## 💖 Support, Sponsorship & Commercial Licensing

If LangVoi has helped your research, audio engineering, or production workflow, you can support ongoing development or purchase a commercial license:

<div align="center">

| Tier | Purpose | Link |
| :--- | :--- | :---: |
| ☕ **Buy Me a Coffee** | One-time tips, coffee donations, and supporter rewards | <a href="https://buymeacoffee.com/princesanchela"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-Donate_☕-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" height="32" alt="Buy Me A Coffee" /></a> |
| 🛍️ **Gumroad Pro Package** | Pre-built commercial standalone installer package | <a href="https://codeprince.gumroad.com/l/langvoi"><img src="https://img.shields.io/badge/Gumroad-Get_Pro_Package-FF90E8?style=for-the-badge&logo=gumroad&logoColor=black" height="32" alt="Gumroad" /></a> |
| 🎮 **itch.io Community** | Pay-what-you-want downloads & community donations | <a href="https://codeprince.itch.io/langvoi-voice-studio-pro"><img src="https://img.shields.io/badge/itch.io-Support_&_Download-FA5C5C?style=for-the-badge&logo=itchdotio&logoColor=white" height="32" alt="itch.io" /></a> |
| 💖 **GitHub Sponsors** | Monthly recurring sponsorship with avatar listed in Hall of Fame | <a href="https://github.com/sponsors/PrinceSanchela"><img src="https://img.shields.io/badge/Sponsor-GitHub_Sponsors-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white" height="32" alt="GitHub Sponsors" /></a> |

</div>

---

## 🏛️ Community Supporters & Hall of Fame

Special recognition to our community supporters and sponsors:

| Supporter | Tier | Contribution |
| :--- | :--- | :--- |
| **Prince Sanchela** | Founding Architect | Architectural design & neural LID DSP engine |
| *Your Name Here* | Community Sponsor | [Become a Sponsor](https://buymeacoffee.com/princesanchela) to get featured! |

---

## 👤 Authorship & Legal License

* **Lead Architect & Creator**: **Prince Sanchela**
* **Contact & Inquiries**: `contact.princesanchela@gmail.com`
* **Official Repository**: [https://github.com/PrinceSanchela/LangVoi](https://github.com/PrinceSanchela/LangVoi)
* **License**: Released under the **[MIT License](LICENSE.txt)**. Free for personal, academic, and commercial audio engineering use.
