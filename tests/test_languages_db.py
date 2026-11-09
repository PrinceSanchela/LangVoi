"""
Unit tests for LangVoi Languages Database.
"""

import unittest
from core.languages_db import LANGUAGES, get_language, search_languages, get_all_languages_list


class TestLanguagesDB(unittest.TestCase):
    def test_database_loaded(self):
        self.assertGreater(len(LANGUAGES), 50)

    def test_get_language_known(self):
        en = get_language("en")
        self.assertIsNotNone(en)
        self.assertEqual(en["name"], "English")
        self.assertEqual(en["flag"], "🇺🇸")

        es = get_language("es")
        self.assertIsNotNone(es)
        self.assertEqual(es["name"], "Spanish")

        hi = get_language("hi")
        self.assertIsNotNone(hi)
        self.assertEqual(hi["name"], "Hindi")
        self.assertEqual(hi["script"], "Devanagari")

    def test_get_language_unknown(self):
        unknown = get_language("nonexistent_code")
        self.assertIsNone(unknown)

    def test_search_languages(self):
        results = search_languages("Spanish")
        self.assertGreater(len(results), 0)
        self.assertTrue(any(r["code"] == "es" for r in results))

        results_by_code = search_languages("fr")
        self.assertTrue(any(r["code"] == "fr" for r in results_by_code))

    def test_get_all_languages_list(self):
        all_langs = get_all_languages_list()
        self.assertEqual(len(all_langs), len(LANGUAGES))
        self.assertTrue(all("code" in lang for lang in all_langs))


if __name__ == "__main__":
    unittest.main()
