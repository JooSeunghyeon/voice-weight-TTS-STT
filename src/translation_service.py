from __future__ import annotations

import os

from src.config import LanguageConfig, MAX_TRANSLATION_TOKENS, TRANSLATION_MODEL_NAME


class TranslationService:
    def __init__(self) -> None:
        self._tokenizer: object | None = None
        self._model: object | None = None
        self._device: str | None = None

    def translate_text(
        self,
        text: str,
        source_language: LanguageConfig,
        target_language: LanguageConfig,
    ) -> str:
        if not text.strip():
            raise ValueError("번역할 텍스트가 비어 있습니다.")
        tokenizer, model, device = self._get_components()
        tokenizer.src_lang = source_language.nllb_code
        inputs = tokenizer(text.strip(), return_tensors="pt", truncation=True).to(device)
        forced_bos_token_id: int = int(tokenizer.convert_tokens_to_ids(target_language.nllb_code))
        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_new_tokens=MAX_TRANSLATION_TOKENS,
        )
        translated_text: str = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0].strip()
        if not translated_text:
            raise ValueError("번역 결과가 비어 있습니다. 입력 음성을 다시 확인해 주세요.")
        return translated_text

    def _get_components(self) -> tuple[object, object, str]:
        if self._tokenizer is not None and self._model is not None and self._device is not None:
            return self._tokenizer, self._model, self._device
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        self._device = "cuda" if self._is_cuda_enabled() else "cpu"
        torch_dtype = torch.float16 if self._device == "cuda" else torch.float32
        self._tokenizer = AutoTokenizer.from_pretrained(TRANSLATION_MODEL_NAME)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(
            TRANSLATION_MODEL_NAME,
            torch_dtype=torch_dtype,
        ).to(self._device)
        self._model.eval()
        return self._tokenizer, self._model, self._device

    def _is_cuda_enabled(self) -> bool:
        if os.getenv("FORCE_CPU", "0") == "1":
            return False
        try:
            import torch
            return bool(torch.cuda.is_available())
        except Exception:
            return False
