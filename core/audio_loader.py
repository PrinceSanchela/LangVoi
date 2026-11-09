"""
Universal Audio Loader Engine for LangVoi Voice Studio Pro.
Supports all worldwide audio formats: MP3, M4A, AAC, WAV (PCM, IEEE float, 24-bit, RF64),
FLAC, OGG, OPUS, WMA, AIFF, and WEBM.
"""

import io
import os
import wave
import numpy as np


class AudioLoader:
    """Robust multi-format audio decoder and normalizer."""

    @classmethod
    def load(cls, source):
        """
        Loads an audio file from a file path or bytes/BytesIO.
        Returns:
            audio: np.ndarray (float32 normalized between -1.0 and 1.0, mono or 2D [samples, channels])
            sr: int (sample rate in Hz)
        """
        # If source is bytes, write to a temp file or BytesIO
        if isinstance(source, (bytes, bytearray)):
            # Check if it has a standard RIFF header first
            if source.startswith(b"RIFF") and b"WAVE" in source[:16]:
                try:
                    return cls._load_wave_bytes(source)
                except Exception:
                    pass
            # Try soundfile from BytesIO
            try:
                import soundfile as sf
                bio = io.BytesIO(source)
                data, sr = sf.read(bio, dtype="float32")
                return cls._normalize_audio_data(data), int(sr)
            except Exception:
                pass

            # Fallback to PyAV with BytesIO
            try:
                import av
                bio = io.BytesIO(source)
                return cls._load_av(bio)
            except Exception:
                pass

            raise ValueError("Unsupported audio data format or corrupted file.")

        # Source is a filepath string
        filepath = str(source)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Audio file does not exist: {filepath}")

        # Method 1: SoundFile (Super fast, handles WAV, MP3, FLAC, OGG, AIFF, RF64, etc.)
        try:
            import soundfile as sf
            data, sr = sf.read(filepath, dtype="float32")
            return cls._normalize_audio_data(data), int(sr)
        except Exception:
            pass

        # Method 2: PyAV (Universal decoder, handles M4A, AAC, AMR, WMA, MP4, WebM, etc.)
        try:
            import av
            return cls._load_av(filepath)
        except Exception:
            pass

        # Method 3: Standard library wave (fallback for standard WAVs)
        try:
            with open(filepath, "rb") as f:
                return cls._load_wave_bytes(f.read())
        except Exception as e:
            raise ValueError(f"Could not load audio file: {e}")

    @classmethod
    def _load_av(cls, source):
        """Decode any audio container/codec using PyAV (universal fallback)."""
        import av
        container = av.open(source)
        try:
            audio_stream = next((s for s in container.streams if s.type == "audio"), None)
            if not audio_stream:
                raise ValueError("No audio stream found in media file.")

            resampler = av.AudioResampler(format="fltp")
            frames_list = []
            sr = audio_stream.rate or 44100

            for frame in container.decode(audio_stream):
                resampled = resampler.resample(frame)
                if resampled:
                    for rf in resampled:
                        frames_list.append(rf.to_ndarray())

            flushed = resampler.resample(None)
            if flushed:
                for rf in flushed:
                    frames_list.append(rf.to_ndarray())
        finally:
            try:
                container.close()
            except Exception:
                pass

        if not frames_list:
            raise ValueError("Audio stream contains no decodable frames.")

        raw_data = np.concatenate(frames_list, axis=1)  # shape: (channels, samples)
        if raw_data.ndim == 2:
            raw_data = raw_data.T  # shape: (samples, channels)

        # If mono (1 channel), flatten to 1D
        if raw_data.ndim == 2 and raw_data.shape[1] == 1:
            raw_data = raw_data.flatten()

        return cls._normalize_audio_data(raw_data), int(sr)

    @classmethod
    def _normalize_audio_data(cls, data: np.ndarray) -> np.ndarray:
        """Ensure float32 dtype and proper shape."""
        if not isinstance(data, np.ndarray):
            data = np.array(data, dtype=np.float32)

        if data.dtype != np.float32:
            data = data.astype(np.float32)

        # Remove NaNs or Infs if any
        np.nan_to_num(data, copy=False)
        return data

    @classmethod
    def _load_wave_bytes(cls, wav_bytes: bytes):
        """Standard library wave fallback."""
        with io.BytesIO(wav_bytes) as bio:
            with wave.open(bio, "rb") as wf:
                channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                framerate = wf.getframerate()
                n_frames = wf.getnframes()
                raw_data = wf.readframes(n_frames)

        if sample_width == 1:
            audio = np.frombuffer(raw_data, dtype=np.uint8).astype(np.float32)
            audio = (audio - 128.0) / 128.0
        elif sample_width == 2:
            audio = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0
        elif sample_width == 3:
            raw_bytes = np.frombuffer(raw_data, dtype=np.uint8)
            num_samples = len(raw_bytes) // 3
            samples_24 = np.zeros(num_samples, dtype=np.int32)
            for i in range(num_samples):
                b0 = raw_bytes[i * 3]
                b1 = raw_bytes[i * 3 + 1]
                b2 = raw_bytes[i * 3 + 2]
                val = b0 | (b1 << 8) | (b2 << 16)
                if val & 0x800000:
                    val -= 0x1000000
                samples_24[i] = val
            audio = samples_24.astype(np.float32) / 8388608.0
        elif sample_width == 4:
            audio = np.frombuffer(raw_data, dtype=np.int32).astype(np.float32) / 2147483648.0
        else:
            audio = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0

        if channels > 1:
            audio = audio.reshape(-1, channels)

        return audio, framerate
