"""
LangVoi Voice Studio Pro - Dialog Modules.
"""
from .languages_dialog import show_languages_dialog
from .export_dialog import show_export_dialog
from .about_dialog import show_about_dialog, show_manual_dialog, show_license_dialog
from .help_dialog import show_help_dialog

__all__ = [
    "show_languages_dialog",
    "show_export_dialog",
    "show_about_dialog",
    "show_manual_dialog",
    "show_license_dialog",
    "show_help_dialog"
]
