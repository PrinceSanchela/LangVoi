"""
Translation Engine for LangVoi Voice Studio Pro.
Translates detected speech transcripts into any world language using Google Translate API.
Supports 100+ target languages with high accuracy.
"""

import urllib.request
import urllib.parse
import json
import threading


# Comprehensive world language codes for translation targets
TRANSLATION_LANGUAGES = {
    "en": "English",
    "hi": "Hindi (हिन्दी)",
    "es": "Spanish (Español)",
    "fr": "French (Français)",
    "de": "German (Deutsch)",
    "zh-CN": "Chinese Simplified (简体中文)",
    "zh-TW": "Chinese Traditional (繁體中文)",
    "ja": "Japanese (日本語)",
    "ko": "Korean (한국어)",
    "ar": "Arabic (العربية)",
    "ru": "Russian (Русский)",
    "pt": "Portuguese (Português)",
    "it": "Italian (Italiano)",
    "th": "Thai (ไทย)",
    "vi": "Vietnamese (Tiếng Việt)",
    "id": "Indonesian (Bahasa)",
    "ms": "Malay (Bahasa Melayu)",
    "tr": "Turkish (Türkçe)",
    "nl": "Dutch (Nederlands)",
    "pl": "Polish (Polski)",
    "uk": "Ukrainian (Українська)",
    "cs": "Czech (Čeština)",
    "ro": "Romanian (Română)",
    "hu": "Hungarian (Magyar)",
    "sv": "Swedish (Svenska)",
    "da": "Danish (Dansk)",
    "no": "Norwegian (Norsk)",
    "fi": "Finnish (Suomi)",
    "el": "Greek (Ελληνικά)",
    "he": "Hebrew (עברית)",
    "bn": "Bengali (বাংলা)",
    "ta": "Tamil (தமிழ்)",
    "te": "Telugu (తెలుగు)",
    "ur": "Urdu (اردو)",
    "fa": "Persian (فارسی)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "gu": "Gujarati (ગુજરાતી)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "ml": "Malayalam (മലയാളം)",
    "mr": "Marathi (मराठी)",
    "ne": "Nepali (नेपाली)",
    "si": "Sinhala (සිංහල)",
    "km": "Khmer (ភាសាខ្មែរ)",
    "my": "Myanmar (မြန်မာ)",
    "lo": "Lao (ລາວ)",
    "sw": "Swahili (Kiswahili)",
    "am": "Amharic (አማርኛ)",
    "bg": "Bulgarian (Български)",
    "hr": "Croatian (Hrvatski)",
    "sk": "Slovak (Slovenčina)",
    "sl": "Slovenian (Slovenščina)",
    "sr": "Serbian (Српски)",
    "ca": "Catalan (Català)",
    "fil": "Filipino (Tagalog)",
    "af": "Afrikaans",
    "sq": "Albanian (Shqip)",
    "et": "Estonian (Eesti)",
    "lv": "Latvian (Latviešu)",
    "lt": "Lithuanian (Lietuvių)",
    "mk": "Macedonian (Македонски)",
    "ga": "Irish (Gaeilge)",
    "cy": "Welsh (Cymraeg)",
    "is": "Icelandic (Íslenska)",
    "mt": "Maltese (Malti)",
    "ka": "Georgian (ქართული)",
    "hy": "Armenian (Հայերեն)",
    "az": "Azerbaijani (Azərbaycan)",
    "uz": "Uzbek (Oʻzbek)",
    "kk": "Kazakh (Қазақ)",
    "mn": "Mongolian (Монгол)",
    "zu": "Zulu (isiZulu)",
    "yo": "Yoruba (Èdè Yorùbá)",
    "ig": "Igbo (Asụsụ Igbo)",
    "ha": "Hausa",
    "la": "Latin (Latina)",
}


class Translator:
    """High-accuracy translator using Google Translate API."""

    ENDPOINT = "https://translate.googleapis.com/translate_a/single"

    @classmethod
    def translate(cls, text: str, source_lang: str = "auto", target_lang: str = "en") -> dict:
        """
        Translates text from source language to target language.

        Args:
            text: The text to translate.
            source_lang: ISO-639-1 source language code (or 'auto' for auto-detect).
            target_lang: ISO-639-1 target language code.

        Returns:
            dict with keys: translated_text, source_lang, target_lang, success, error
        """
        if not text or not text.strip():
            return {
                "translated_text": "",
                "source_lang": source_lang,
                "target_lang": target_lang,
                "success": False,
                "error": "No text to translate."
            }

        try:
            params = {
                "client": "gtx",
                "sl": source_lang,
                "tl": target_lang,
                "dt": "t",
                "q": text.strip(),
            }
            url = cls.ENDPOINT + "?" + urllib.parse.urlencode(params)
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode("utf-8"))

            translated_segments = []
            if data and data[0]:
                for segment in data[0]:
                    if segment and segment[0]:
                        translated_segments.append(segment[0])

            translated_text = "".join(translated_segments)

            # Auto-detected source language (if source was 'auto')
            detected_src = source_lang
            if len(data) > 2 and data[2]:
                detected_src = data[2]

            return {
                "translated_text": translated_text,
                "source_lang": detected_src,
                "target_lang": target_lang,
                "success": True,
                "error": None
            }

        except Exception as e:
            return {
                "translated_text": "",
                "source_lang": source_lang,
                "target_lang": target_lang,
                "success": False,
                "error": str(e)
            }

    @classmethod
    def translate_async(cls, text: str, source_lang: str, target_lang: str, callback):
        """Non-blocking translation. Calls callback(result_dict) when done."""
        def _worker():
            result = cls.translate(text, source_lang, target_lang)
            callback(result)
        threading.Thread(target=_worker, daemon=True).start()

    @classmethod
    def get_language_name(cls, code: str) -> str:
        """Returns the display name for a language code."""
        return TRANSLATION_LANGUAGES.get(code, code.upper())

    @classmethod
    def get_all_targets(cls) -> dict:
        """Returns all available translation target languages."""
        return TRANSLATION_LANGUAGES.copy()
