"""
World Languages Directory Dialog (150+ Spoken Languages).
Searchable treeview table with flags, native scripts, ISO codes, and families.
Screen-aware responsive geometry, singleton pattern, and proportional column scaling.
"""

import os
import tkinter as tk
from tkinter import ttk
from app.theme import Theme
from core.languages_db import get_all_languages_list

_languages_instance = None


class LanguagesDialog(tk.Toplevel):
    """Screen-aware, responsive World Languages Directory dialog."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("World Languages Directory (150+ Spoken Languages) — LangVoi Studio")
        self.configure(bg=Theme.BG_ROOT)

        # 1. Screen-Aware Auto-Geometry & Centering
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        target_w = min(1100, max(840, int(screen_w * 0.70)))
        target_h = min(800, max(560, int(screen_h * 0.72)))

        pos_x = max(10, (screen_w - target_w) // 2)
        pos_y = max(10, (screen_h - target_h) // 2 - 20)

        self.geometry(f"{target_w}x{target_h}+{pos_x}+{pos_y}")
        self.minsize(780, 500)

        # Window Icon
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
        ico_path = os.path.join(assets_dir, "app_icon.ico")
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass

        # 2. Branded Header Banner
        banner = tk.Frame(self, bg=Theme.BG_HEADER, height=48, relief="raised", bd=1)
        banner.pack(side="top", fill="x")

        tk.Label(banner, text="🌍", font=("Segoe UI Emoji", 18), bg=Theme.BG_HEADER).pack(side="left", padx=(14, 8))
        hdr_txt = tk.Frame(banner, bg=Theme.BG_HEADER)
        hdr_txt.pack(side="left", fill="both", expand=True, pady=6)
        tk.Label(
            hdr_txt,
            text="WORLD LANGUAGES DIRECTORY & CLASSIFICATION DATABASE",
            font=Theme.FONT_TITLE,
            fg=Theme.COLOR_CYAN,
            bg=Theme.BG_HEADER,
            anchor="w"
        ).pack(fill="x")
        tk.Label(
            hdr_txt,
            text="Comprehensive 150+ Natural Spoken Languages • ISO-639-1 / 639-3 • Scripts & Linguistic Families",
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
            pady=3,
            cursor="hand2"
        )
        btn_close.pack(side="right", padx=14, pady=10)

        # 3. Search & Metrics Filter Bar
        s_frame = tk.Frame(self, bg=Theme.BG_SUBRACK, padx=12, pady=8, relief="groove", bd=1)
        s_frame.pack(fill="x", padx=12, pady=(10, 4))

        tk.Label(s_frame, text="🔍 Instant Search / Filter:", font=Theme.FONT_SUBTITLE, fg=Theme.COLOR_AMBER, bg=Theme.BG_SUBRACK).pack(side="left", padx=(0, 8))

        self.ent_search = tk.Entry(
            s_frame,
            font=("Consolas", 10),
            bg="#080a10",
            fg="#38bdf8",
            insertbackground="#ffffff",
            relief="sunken",
            bd=1
        )
        self.ent_search.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=3)
        self.ent_search.focus_set()

        self.lbl_count = tk.Label(s_frame, text="Showing: 0 languages", font=Theme.FONT_MONO, fg=Theme.TEXT_MUTED, bg=Theme.BG_SUBRACK)
        self.lbl_count.pack(side="right", padx=(8, 0))

        btn_clear = tk.Button(
            s_frame,
            text="Clear Filter",
            command=self._clear_filter,
            font=Theme.FONT_LABEL,
            bg=Theme.BG_PANEL,
            fg=Theme.TEXT_MAIN,
            relief="raised",
            bd=1,
            padx=8,
            pady=1
        )
        btn_clear.pack(side="right")

        # 4. Treeview Table Frame
        tree_frame = tk.Frame(self, bg=Theme.BG_ROOT)
        tree_frame.pack(fill="both", expand=True, padx=12, pady=6)

        columns = ("flag", "name", "native", "code", "family", "speakers")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("flag", text="Flag")
        self.tree.heading("name", text="Language Name", command=lambda: self._sort_by("name"))
        self.tree.heading("native", text="Native Script", command=lambda: self._sort_by("native"))
        self.tree.heading("code", text="ISO Code", command=lambda: self._sort_by("code"))
        self.tree.heading("family", text="Linguistic Family", command=lambda: self._sort_by("family"))
        self.tree.heading("speakers", text="Est. Native Speakers", command=lambda: self._sort_by("speakers"))

        self.tree.column("flag", width=55, minwidth=45, anchor="center", stretch=False)
        self.tree.column("name", width=180, minwidth=140, anchor="w", stretch=True)
        self.tree.column("native", width=160, minwidth=120, anchor="w", stretch=True)
        self.tree.column("code", width=75, minwidth=60, anchor="center", stretch=False)
        self.tree.column("family", width=220, minwidth=160, anchor="w", stretch=True)
        self.tree.column("speakers", width=140, minwidth=110, anchor="e", stretch=False)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Load data
        self.all_langs = get_all_languages_list()
        self._populate()

        self.ent_search.bind("<KeyRelease>", lambda e: self._populate(self.ent_search.get()))

        # 5. Bottom Status Bar
        footer = tk.Frame(self, bg=Theme.BG_HEADER, height=26, relief="raised", bd=1)
        footer.pack(side="bottom", fill="x")
        tk.Label(
            footer,
            text=f"Total Indexed: {len(self.all_langs)} Natural Languages • LangVoi Neural Whisper & Fallback Classifier Compatible",
            font=Theme.FONT_LABEL,
            fg=Theme.TEXT_MUTED,
            bg=Theme.BG_HEADER
        ).pack(side="left", padx=12, pady=4)

        tk.Button(
            footer,
            text="✓ Close Directory",
            command=self._on_close,
            font=Theme.FONT_SUBTITLE,
            bg=Theme.COLOR_BLUE,
            fg="#ffffff",
            padx=14,
            pady=2,
            relief="raised",
            bd=1
        ).pack(side="right", padx=12, pady=3)

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.transient(parent)
        self.lift()

    def _clear_filter(self):
        self.ent_search.delete(0, tk.END)
        self._populate("")

    def _populate(self, filter_str=""):
        for row in self.tree.get_children():
            self.tree.delete(row)
        q = filter_str.strip().lower()
        count = 0
        for l in self.all_langs:
            name = l.get("name", "")
            native = l.get("native_name", "")
            code = l.get("code", "")
            fam = l.get("family", "")
            spk = l.get("speakers", "")
            flag = l.get("flag", "🌐")

            if (not q or q in name.lower() or q in native.lower() or q in fam.lower() or q in code.lower()):
                self.tree.insert("", "end", values=(flag, name, native, code.upper(), fam, spk))
                count += 1

        self.lbl_count.config(text=f"Showing: {count} of {len(self.all_langs)} languages")

    def _sort_by(self, col):
        # Optional column sorting
        pass

    def _on_close(self):
        global _languages_instance
        _languages_instance = None
        self.destroy()


def show_languages_dialog(parent):
    """Opens or raises the singleton World Languages Directory dialog."""
    global _languages_instance
    if _languages_instance is not None:
        try:
            if _languages_instance.winfo_exists():
                _languages_instance.deiconify()
                _languages_instance.lift()
                _languages_instance.focus_force()
                return _languages_instance
        except Exception:
            _languages_instance = None

    dlg = LanguagesDialog(parent)
    _languages_instance = dlg
    return dlg
