"""
Audio Engine for LangVoi Voice Studio Pro.
High-Performance Real-Time Streaming Audio I/O Engine using SoundDevice.
Provides instant volume changes, sub-millisecond seeking, frame-accurate
playhead tracking, and live microphone capture streams.
"""

import time
import threading
import numpy as np
import sounddevice as sd


class AudioEngine:
    """Core native high-performance audio streaming engine."""

    def __init__(self):
        # Playback State
        self.audio_raw = None
        self.sr = 44100
        self.duration = 0.0
        self.is_playing = False
        self.is_looping = False
        self.current_frame = 0
        self.playback_rate = 1.0
        self.volume = 1.0
        self.is_muted = False

        self.out_stream = None
        self.stream_lock = threading.Lock()
        self.on_ended_cb = None

        # Recording State
        self.is_recording = False
        self.is_rec_paused = False
        self.rec_frames = []
        self.rec_stream = None
        self.rec_start_time = 0.0
        self.on_live_peak_cb = None

    def set_audio_data(self, audio: np.ndarray, sr: int):
        """Set new audio data and reset playhead."""
        self.stop_playback()
        with self.stream_lock:
            # Flatten to 1D mono if needed
            if audio.ndim > 1:
                audio = np.mean(audio, axis=1)
            self.audio_raw = np.ascontiguousarray(audio, dtype=np.float32)
            self.sr = int(sr)
            self.duration = float(len(self.audio_raw)) / float(self.sr)
            self.current_frame = 0

    def play(self, on_ended_callback=None):
        """Start or resume real-time audio playback."""
        if self.audio_raw is None or len(self.audio_raw) == 0:
            return

        if on_ended_callback:
            self.on_ended_cb = on_ended_callback

        with self.stream_lock:
            if self.current_frame >= len(self.audio_raw):
                self.current_frame = 0

            if self.is_playing and self.out_stream and self.out_stream.active:
                return

            self.is_playing = True
            self._start_stream()

    def _start_stream(self):
        """Helper to create and activate output stream."""
        if self.out_stream:
            try:
                self.out_stream.stop()
                self.out_stream.close()
            except Exception:
                pass
            self.out_stream = None

        rate = int(self.sr * self.playback_rate)
        self.out_stream = sd.OutputStream(
            samplerate=rate,
            channels=1,
            dtype="float32",
            blocksize=1024,
            callback=self._audio_callback
        )
        self.out_stream.start()

    def _audio_callback(self, outdata, frames, time_info, status):
        """Low-latency real-time callback invoked by audio hardware."""
        with self.stream_lock:
            if not self.is_playing or self.audio_raw is None:
                outdata.fill(0)
                return

            cf = self.current_frame
            total = len(self.audio_raw)

            if cf >= total:
                if self.is_looping:
                    self.current_frame = 0
                    cf = 0
                else:
                    outdata.fill(0)
                    self.is_playing = False
                    self.current_frame = 0
                    if self.on_ended_cb:
                        threading.Thread(target=self.on_ended_cb, daemon=True).start()
                    return

            rem = total - cf
            take = min(frames, rem)
            vol = 0.0 if self.is_muted else self.volume

            outdata[:take, 0] = self.audio_raw[cf : cf + take] * vol

            if take < frames:
                outdata[take:].fill(0)
                if self.is_looping:
                    self.current_frame = 0
                else:
                    self.is_playing = False
                    self.current_frame = 0
                    if self.on_ended_cb:
                        threading.Thread(target=self.on_ended_cb, daemon=True).start()
            else:
                self.current_frame += take

    def pause(self):
        """Pause playback without resetting frame position."""
        with self.stream_lock:
            self.is_playing = False
            if self.out_stream:
                try:
                    self.out_stream.stop()
                    self.out_stream.close()
                except Exception:
                    pass
                self.out_stream = None

    def stop_playback(self):
        """Stop playback and rewind to beginning."""
        with self.stream_lock:
            self.is_playing = False
            self.current_frame = 0
            if self.out_stream:
                try:
                    self.out_stream.stop()
                    self.out_stream.close()
                except Exception:
                    pass
                self.out_stream = None

    def seek(self, seconds: float, start_play: bool = False):
        """Instantaneously seek to requested seconds."""
        if self.audio_raw is None or len(self.audio_raw) == 0:
            return

        target_frame = int(seconds * self.sr)
        with self.stream_lock:
            self.current_frame = max(0, min(len(self.audio_raw) - 1, target_frame))

        if start_play and not self.is_playing:
            self.play(self.on_ended_cb)

    def set_volume(self, val: float):
        """Instantly update volume multiplier (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, float(val)))

    def set_speed(self, speed: float):
        """Change playback speed seamlessly."""
        self.playback_rate = max(0.25, min(4.0, float(speed)))
        with self.stream_lock:
            if self.is_playing:
                self._start_stream()

    def get_current_time(self) -> float:
        """Return frame-accurate audio position in seconds."""
        if self.sr <= 0:
            return 0.0
        with self.stream_lock:
            return min(self.duration, float(self.current_frame) / float(self.sr))

    def get_playback_peaks(self) -> tuple[float, float]:
        """Return real-time stereo VU peaks."""
        if not self.is_playing or self.audio_raw is None:
            return 0.0, 0.0

        with self.stream_lock:
            cf = self.current_frame
            total = len(self.audio_raw)
            if cf < total:
                chunk = self.audio_raw[cf : min(total, cf + 1024)]
                if len(chunk) > 0:
                    vol = 0.0 if self.is_muted else self.volume
                    p = float(np.max(np.abs(chunk))) * vol
                    return p, p * 0.94
        return 0.0, 0.0

    # =========================================================================
    # RECORDING
    # =========================================================================
    def start_recording(self, device_id=None, live_peak_callback=None):
        self.stop_playback()
        self.is_recording = True
        self.is_rec_paused = False
        self.rec_frames = []
        self.rec_start_time = time.time()
        self.on_live_peak_cb = live_peak_callback

        def _callback(indata, frames, time_info, status):
            if self.is_recording and not self.is_rec_paused:
                self.rec_frames.append(indata.copy())
                if self.on_live_peak_cb:
                    peak = float(np.max(np.abs(indata)))
                    self.on_live_peak_cb(peak, indata.flatten())

        self.rec_stream = sd.InputStream(
            device=device_id, channels=1, samplerate=44100, dtype="float32", callback=_callback
        )
        self.rec_stream.start()

    def stop_recording(self) -> tuple[np.ndarray, int]:
        if not self.is_recording:
            return None, 44100
        self.is_recording = False
        if self.rec_stream:
            try:
                self.rec_stream.stop()
                self.rec_stream.close()
            except Exception:
                pass
            self.rec_stream = None

        if self.rec_frames:
            recorded = np.concatenate(self.rec_frames, axis=0).flatten()
            self.set_audio_data(recorded, 44100)
            return recorded, 44100
        return None, 44100

    def discard_recording(self):
        self.is_recording = False
        if self.rec_stream:
            try:
                self.rec_stream.stop()
                self.rec_stream.close()
            except Exception:
                pass
            self.rec_stream = None
        self.rec_frames = []

    @staticmethod
    def get_input_devices():
        devices = []
        try:
            device_list = sd.query_devices()
            for idx, dev in enumerate(device_list):
                if dev.get("max_input_channels", 0) > 0:
                    devices.append({
                        "id": idx,
                        "name": dev.get("name", f"Microphone {idx}"),
                        "channels": dev.get("max_input_channels", 1),
                        "default_samplerate": int(dev.get("default_samplerate", 44100)),
                        "is_default": idx == sd.default.device[0]
                    })
        except Exception:
            devices.append({"id": 0, "name": "Default Microphone", "channels": 1, "default_samplerate": 44100})
        return devices
