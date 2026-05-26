from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageConfig:
    display_name: str
    whisper_code: str
    nllb_code: str
    xtts_code: str


KOREAN_LANGUAGE: LanguageConfig = LanguageConfig(
    display_name="Korean",
    whisper_code="ko",
    nllb_code="kor_Hang",
    xtts_code="ko",
)

FOREIGN_LANGUAGES: dict[str, LanguageConfig] = {
    "English": LanguageConfig("English", "en", "eng_Latn", "en"),
    "Japanese": LanguageConfig("Japanese", "ja", "jpn_Jpan", "ja"),
    "Chinese": LanguageConfig("Chinese", "zh", "zho_Hans", "zh-cn"),
    "Spanish": LanguageConfig("Spanish", "es", "spa_Latn", "es"),
    "French": LanguageConfig("French", "fr", "fra_Latn", "fr"),
    "German": LanguageConfig("German", "de", "deu_Latn", "de"),
}

DEFAULT_FOREIGN_LANGUAGE: str = "English"
DEFAULT_DIRECTION: str = "Korean to foreign language"
REVERSE_DIRECTION: str = "Foreign language to Korean"
WHISPER_MODEL_NAME: str = "large-v3-turbo"
WHISPER_FALLBACK_MODEL_NAME: str = "turbo"
TRANSLATION_MODEL_NAME: str = "facebook/nllb-200-distilled-600M"
TTS_MODEL_NAME: str = "tts_models/multilingual/multi-dataset/xtts_v2"
OUTPUT_AUDIO_SAMPLE_RATE: int = 24000
MAX_TRANSLATION_TOKENS: int = 256
