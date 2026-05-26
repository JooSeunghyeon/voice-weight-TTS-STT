from __future__ import annotations

import os
from functools import lru_cache

import gradio as gr

from src.config import DEFAULT_DIRECTION, DEFAULT_FOREIGN_LANGUAGE, FOREIGN_LANGUAGES, REVERSE_DIRECTION
from src.pipeline import VoiceTranslationPipeline
from src.stt_service import SpeechToTextService
from src.translation_service import TranslationService
from src.tts_service import TextToSpeechService


@lru_cache(maxsize=1)
def get_pipeline() -> VoiceTranslationPipeline:
    return VoiceTranslationPipeline(
        stt_service=SpeechToTextService(),
        translation_service=TranslationService(),
        tts_service=TextToSpeechService(),
    )


def translate_voice(
    audio_path: str | None,
    direction: str,
    foreign_language_name: str,
) -> tuple[str, str, str | None, str]:
    if audio_path is None:
        return "", "", None, "음성 파일을 업로드하거나 마이크로 녹음해 주세요."
    try:
        result = get_pipeline().translate_voice(
            audio_path=audio_path,
            direction=direction,
            foreign_language_name=foreign_language_name,
        )
        status_message: str = f"{result.source_language} -> {result.target_language} 통역이 완료되었습니다."
        return result.recognized_text, result.translated_text, result.output_audio_path, status_message
    except Exception as err:
        return "", "", None, f"처리 중 오류가 발생했습니다: {err}"


def build_demo() -> gr.Blocks:
    with gr.Blocks(title="Local Voice Translator") as demo:
        gr.Markdown(
            """
            # Local Voice Translator
            음성을 입력하면 로컬 모델로 STT, 번역, voice cloning TTS를 실행해 같은 목소리에 가까운 통역 음성을 생성합니다.
            번역은 외부 API 없이 `facebook/nllb-200-distilled-600M` 모델로 처리합니다.
            """
        )
        with gr.Row():
            direction = gr.Radio(
                choices=[DEFAULT_DIRECTION, REVERSE_DIRECTION],
                value=DEFAULT_DIRECTION,
                label="Translation direction",
            )
            foreign_language = gr.Dropdown(
                choices=list(FOREIGN_LANGUAGES.keys()),
                value=DEFAULT_FOREIGN_LANGUAGE,
                label="Foreign language",
            )
        audio_input = gr.Audio(
            sources=["microphone", "upload"],
            type="filepath",
            label="Input voice",
        )
        translate_button = gr.Button("Translate with cloned voice", variant="primary")
        with gr.Row():
            recognized_text = gr.Textbox(label="Recognized text", lines=4)
            translated_text = gr.Textbox(label="Translated text", lines=4)
        audio_output = gr.Audio(label="Translated voice", type="filepath")
        status = gr.Textbox(label="Status", interactive=False)
        translate_button.click(
            fn=translate_voice,
            inputs=[audio_input, direction, foreign_language],
            outputs=[recognized_text, translated_text, audio_output, status],
        )
        gr.Markdown(
            """
            ## Notes
            - 첫 실행에서는 Whisper, NLLB, XTTS-v2 모델 다운로드 때문에 시간이 오래 걸릴 수 있습니다.
            - Voice cloning 품질을 위해 6초 이상, 배경 소음이 적은 단일 화자 음성을 권장합니다.
            - Kaggle에서는 GPU Accelerator를 켠 뒤 실행하세요.
            """
        )
    return demo


if __name__ == "__main__":
    port: int = int(os.getenv("PORT", "7860"))
    build_demo().queue().launch(server_name="0.0.0.0", server_port=port, share=False)
