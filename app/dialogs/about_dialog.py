"""
Professional Branded About & Technical System Diagnostics Dialog.
LangVoi Voice Studio Pro.
Designed & Engineered by Prince Sanchela.
"""

from app.dialogs.help_dialog import show_help_dialog


def show_license_dialog(parent):
    """
    Classic, formal End-User License Agreement (EULA) reader.
    Routes seamlessly into the unified Knowledge Hub (Tab 5: License EULA).
    """
    return show_help_dialog(parent, default_tab=5)


def show_about_dialog(parent):
    """
    Branded About Dialog featuring Lead Architect Prince Sanchela.
    Routes seamlessly into the unified Knowledge Hub (Tab 6: About & Diagnostics).
    """
    return show_help_dialog(parent, default_tab=6)


def show_manual_dialog(parent):
    """
    Complete User Manual & Documentation.
    Routes seamlessly into the unified Knowledge Hub (Tab 0: Quick Start).
    """
    return show_help_dialog(parent, default_tab=0)
