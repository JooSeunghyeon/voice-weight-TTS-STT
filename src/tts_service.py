from __future__ import annotations

import os
import tempfile
from pathlib import Path

from src.config import LanguageConfig, TTS_MODEL_NAME


class TextToSpeechService:
    def __init__(self) -> None:
        self._model: object | None = None

    def synthesize_speech(
        self,
        text: str,
        reference_audio_path: str,
        target_language: LanguageConfig,
    ) -> str:
        if not text.strip():
            raise ValueError("합성할 텍스트가 비어 있습니다.")
        if not Path(reference_audio_path).exists():
            raise FileNotFoundError("참조 음성 파일을 찾을 수 없습니다.")
        output_path: str = self._create_output_path()
        model: object = self._get_model()
        model.tts_to_file(
            text=text.strip(),
            speaker_wav=reference_audio_path,
            language=target_language.xtts_code,
            file_path=output_path,
        )
        return output_path

    def _get_model(self) -> object:
        if self._model is not None:
            return self._model
        os.environ.setdefault("COQUI_TOS_AGREED", "1")
        from TTS.api import TTS
        device: str = "cuda" if self._is_cuda_enabled() else "cpu"
        self._model = TTS(TTS_MODEL_NAME).to(device)
        return self._model

    def _is_cuda_enabled(self) -> bool:
        if os.getenv("FORCE_CPU", "0") == "1":
            return False
        try:
            import torch
            return bool(torch.cuda.is_available())
        except Exception:
            return False

    def _create_output_path(self) -> str:
        temporary_file = tempfile.NamedTemporaryFile(
            prefix="voice_translator_",
            suffix=".wav",
            delete=False,
        )
        temporary_file.close()
        return temporary_file.name
