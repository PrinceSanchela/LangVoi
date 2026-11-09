"""
Unit tests for VoiceAnalyzer DSP engine.
"""

import os
import unittest
import numpy as np
from core.audio_loader import AudioLoader
from core.voice_analyzer import VoiceAnalyzer

SAMPLE_FILE = os.path.join(os.path.dirname(__file__), "..", "samples", "sample_english_male.wav")


class TestVoiceAnalyzer(unittest.TestCase):
    def test_hz_to_note(self):
        self.assertEqual(VoiceAnalyzer.hz_to_note(440.0), "A4")
        self.assertEqual(VoiceAnalyzer.hz_to_note(261.63), "C4")
        self.assertEqual(VoiceAnalyzer.hz_to_note(0), "N/A")
        self.assertEqual(VoiceAnalyzer.hz_to_note(-10), "N/A")

    def test_classify_vocal_register(self):
        self.assertEqual(VoiceAnalyzer.classify_vocal_register(100), "Bass (Low Male)")
        self.assertEqual(VoiceAnalyzer.classify_vocal_register(130), "Baritone (Mid Male)")
        self.assertEqual(VoiceAnalyzer.classify_vocal_register(180), "Tenor / Low Female")
        self.assertEqual(VoiceAnalyzer.classify_vocal_register(0), "Unclassified")

    def test_analyze_audio(self):
        audio, sr = AudioLoader.load(SAMPLE_FILE)
        metrics = VoiceAnalyzer.analyze_audio(audio, sr)
        self.assertIsInstance(metrics, dict)
        self.assertIn("avg_pitch_hz", metrics)
        self.assertIn("musical_note", metrics)
        self.assertIn("vocal_register", metrics)
        self.assertIn("snr_db", metrics)
        self.assertIn("speech_ratio_pct", metrics)
        self.assertGreater(metrics["duration_sec"], 0)


if __name__ == "__main__":
    unittest.main()
