"""
LangVoi Voice Studio Pro - Main Desktop Entry Point.
Initializes High-Definition (HiDPI) Per-Monitor scaling and starts
the pure native desktop audio engineering workstation.
"""

import sys
import os
import ctypes
import tkinter as tk

# Ensure workspace root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import LangVoiMainWindow


def enable_windows_hidpi():
    """Enables Windows Per-Monitor High-DPI Awareness for razor-sharp HD rendering."""
    try:
        # Shcore API (Windows 8.1+) - Per-monitor DPI aware
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            # User32 API (Windows Vista+) - System DPI aware
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def main():
    enable_windows_hidpi()
    root = tk.Tk()
    app = LangVoiMainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
