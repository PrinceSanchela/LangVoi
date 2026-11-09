"""
LangVoi Voice Studio Pro - Native UI Components.
"""
from .oscilloscope import OscilloscopeComponent
from .vu_meters import VUMetersComponent
from .language_rack import LanguageRackComponent
from .telemetry_rack import TelemetryRackComponent
from .spectral_lab import SpectralLabComponent
from .recorder_panel import RecorderPanelComponent
from .toolbar import ToolbarComponent
from .status_bar import StatusBarComponent

__all__ = [
    "OscilloscopeComponent",
    "VUMetersComponent",
    "LanguageRackComponent",
    "TelemetryRackComponent",
    "SpectralLabComponent",
    "RecorderPanelComponent",
    "ToolbarComponent",
    "StatusBarComponent"
]
