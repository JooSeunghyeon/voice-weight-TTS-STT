from __future__ import annotations

import os
from dataclasses import dataclass

from src.config import LanguageConfig, WHISPER_FALLBACK_MODEL_NAME, WHISPER_MODEL_NAME


@dataclass(frozen=True)
class TranscriptionResult:
    text: str
    detected_language: str
    language_probability: float


class SpeechToTextService:
    def __init__(self) -> None:
        self._model: object | None = None

    def transcribe_audio(self, audio_path: str, language: LanguageConfig) -> TranscriptionResult:
        model: object = self._get_model()
        segments, info = model.transcribe(
            audio_path,
            language=language.whisper_code,
            beam_size=5,
            vad_filter=True,
        )
        recognized_text: str = " ".join(segment.text.strip() for segment in segments).strip()
        if not recognized_text:
            raise ValueError("음성을 인식하지 못했습니다. 더 길고 또렷한 음성을 입력해 주세요.")
        return TranscriptionResult(
            text=recognized_text,
            detected_language=str(info.language),
            language_probability=float(info.language_probability),
        )

    def _get_model(self) -> object:
        if self._model is not None:
            return self._model
        from faster_whisper import WhisperModel
        device: str = "cuda" if self._is_cuda_enabled() else "cpu"
        compute_type: str = "float16" if device == "cuda" else "int8"
        try:
            self._model = WhisperModel(WHISPER_MODEL_NAME, device=device, compute_type=compute_type)
        except Exception:
            self._model = WhisperModel(WHISPER_FALLBACK_MODEL_NAME, device=device, compute_type=compute_type)
        return self._model

    def _is_cuda_enabled(self) -> bool:
        if os.getenv("FORCE_CPU", "0") == "1":
            return False
        try:
            import torch
            return bool(torch.cuda.is_available())
        except Exception:
            return False
