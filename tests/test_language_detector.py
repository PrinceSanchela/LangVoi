"""
Unit tests for LanguageDetector engine.
"""

import os
import unittest
from core.audio_loader import AudioLoader
from core.voice_analyzer import VoiceAnalyzer
from core.language_detector import LanguageDetector

SAMPLE_FILE = os.path.join(os.path.dirname(__file__), "..", "samples", "sample_english_male.wav")


class TestLanguageDetector(unittest.TestCase):
    def setUp(self):
        self.detector = LanguageDetector()

    def test_detect_script(self):
        self.assertEqual(self.detector.detect_script("Hello world"), "Latin")
        self.assertEqual(self.detector.detect_script("नमस्ते दुनिया"), "Devanagari")
        self.assertEqual(self.detector.detect_script("你好世界"), "Hanzi (Chinese)")
        self.assertEqual(self.detector.detect_script("مرحبا بالعالم"), "Arabic")
        self.assertEqual(self.detector.detect_script("Привет мир"), "Cyrillic")
        self.assertEqual(self.detector.detect_script(""), "Unknown")

    def test_match_text_to_language(self):
        code, conf = self.detector.match_text_to_language("Hello how are you today")
        self.assertEqual(code, "en")
        self.assertGreater(conf, 0.5)

        code_es, conf_es = self.detector.match_text_to_language("Hola como estas amigo gracias")
        self.assertEqual(code_es, "es")
        self.assertGreater(conf_es, 0.5)

    def test_acoustic_fallback_pipeline(self):
        audio, sr = AudioLoader.load(SAMPLE_FILE)
        metrics = VoiceAnalyzer.analyze_audio(audio, sr)
        res = self.detector.identify_language(
            wav_bytes=None,
            voice_metrics=metrics,
            audio_raw=audio,
            sr_rate=sr
        )
        self.assertIsInstance(res, dict)
        self.assertIn("primary", res)
        self.assertIn("candidates", res)
        self.assertIn("method", res)
        self.assertGreater(len(res["candidates"]), 0)


if __name__ == "__main__":
    unittest.main()
