from __future__ import annotations

from dataclasses import dataclass

from src.config import (
    DEFAULT_DIRECTION,
    FOREIGN_LANGUAGES,
    KOREAN_LANGUAGE,
    REVERSE_DIRECTION,
    LanguageConfig,
)
from src.stt_service import SpeechToTextService
from src.translation_service import TranslationService
from src.tts_service import TextToSpeechService


@dataclass(frozen=True)
class VoiceTranslationResult:
    source_language: str
    target_language: str
    recognized_text: str
    translated_text: str
    output_audio_path: str


class VoiceTranslationPipeline:
    def __init__(
        self,
        stt_service: SpeechToTextService,
        translation_service: TranslationService,
        tts_service: TextToSpeechService,
    ) -> None:
        self._stt_service = stt_service
        self._translation_service = translation_service
        self._tts_service = tts_service

    def translate_voice(
        self,
        audio_path: str,
        direction: str,
        foreign_language_name: str,
    ) -> VoiceTranslationResult:
        source_language, target_language = self._resolve_languages(direction, foreign_language_name)
        transcription = self._stt_service.transcribe_audio(audio_path, source_language)
        translated_text: str = self._translation_service.translate_text(
            transcription.text,
            source_language,
            target_language,
        )
        output_audio_path: str = self._tts_service.synthesize_speech(
            translated_text,
            audio_path,
            target_language,
        )
        return VoiceTranslationResult(
            source_language=source_language.display_name,
            target_language=target_language.display_name,
            recognized_text=transcription.text,
            translated_text=translated_text,
            output_audio_path=output_audio_path,
        )

    def _resolve_languages(
        self,
        direction: str,
        foreign_language_name: str,
    ) -> tuple[LanguageConfig, LanguageConfig]:
        foreign_language: LanguageConfig | None = FOREIGN_LANGUAGES.get(foreign_language_name)
        if foreign_language is None:
            raise ValueError("지원하지 않는 외국어입니다.")
        if direction == DEFAULT_DIRECTION:
            return KOREAN_LANGUAGE, foreign_language
        if direction == REVERSE_DIRECTION:
            return foreign_language, KOREAN_LANGUAGE
        raise ValueError("지원하지 않는 통역 방향입니다.")
