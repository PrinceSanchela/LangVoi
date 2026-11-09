"""
Unit tests for AudioLoader engine.
"""

import os
import unittest
import numpy as np
from core.audio_loader import AudioLoader

SAMPLE_FILE = os.path.join(os.path.dirname(__file__), "..", "samples", "sample_english_male.wav")


class TestAudioLoader(unittest.TestCase):
    def test_load_sample_file(self):
        self.assertTrue(os.path.exists(SAMPLE_FILE), f"Sample file not found: {SAMPLE_FILE}")
        audio, sr = AudioLoader.load(SAMPLE_FILE)
        self.assertIsInstance(audio, np.ndarray)
        self.assertGreater(sr, 0)
        self.assertGreater(len(audio), 0)
        # Check normalization
        self.assertLessEqual(np.max(np.abs(audio)), 1.05)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            AudioLoader.load("non_existent_audio_file.wav")


if __name__ == "__main__":
    unittest.main()
