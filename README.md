# Local Voice Translator.

Gradio 기반 음성 통역 웹 데모입니다. 사용자가 입력한 음성을 STT로 텍스트화하고, 로컬 번역 모델로 한국어와 외국어 사이를 번역한 뒤, 입력 음성을 참조 음성으로 사용해 비슷한 목소리의 번역 음성을 생성합니다.

## Features

- 한국어 -> 외국어, 외국어 -> 한국어 양방향 통역
- 외국어 6개 지원: English, Japanese, Chinese, Spanish, French, German
- 외부 번역 API 없이 Kaggle GPU에서 로컬 모델 실행
- Gradio 웹 UI 제공
- Cloudflare Tunnel을 통한 public URL 서빙

## Models

| Stage | Model | Purpose |
| --- | --- | --- |
| STT | `faster-whisper` + `large-v3-turbo` | 입력 음성을 텍스트로 변환 |
| Translation | `facebook/nllb-200-distilled-600M` | 한국어와 외국어 간 로컬 번역 |
| TTS | `tts_models/multilingual/multi-dataset/xtts_v2` | 참조 음성 기반 voice cloning TTS |

## Local Run

Python 3.10 환경과 CUDA GPU를 권장합니다.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

브라우저에서 `http://127.0.0.1:7860`에 접속합니다.

## Kaggle Run

1. Kaggle Notebook을 생성합니다.
2. Settings에서 Accelerator를 GPU로 설정합니다.
3. Kaggle 기본 Python이 `TTS` 패키지와 맞지 않을 수 있으므로, 노트북에서 Python 3.10 conda 환경을 만든 뒤 실행합니다.
4. [`notebooks/kaggle_voice_translator.ipynb`](notebooks/kaggle_voice_translator.ipynb)의 셀을 순서대로 실행합니다.
5. Cloudflare 셀에서 출력되는 `https://*.trycloudflare.com` 주소를 Gradio public URL로 사용합니다.
6. Share 설정에서 notebook 권한을 Public으로 변경합니다.

## Cloudflare Public Serving

노트북에는 아래 방식의 Cloudflare Tunnel 실행 셀이 포함되어 있습니다.

```bash
./cloudflared tunnel --url http://127.0.0.1:7860
```

출력 로그에서 `https://*.trycloudflare.com` URL을 확인한 뒤, 해당 주소를 제출 자료에 포함합니다.

## Demo Tips

- 첫 실행에서는 모델 다운로드 때문에 시간이 오래 걸립니다.
- Voice cloning 품질을 위해 6초 이상, 조용한 환경의 단일 화자 음성을 권장합니다.
- 한국어 -> 외국어와 외국어 -> 한국어를 각각 1회 이상 실행해 스크린샷을 남기세요.
- Kaggle 세션이 종료되면 Cloudflare public URL도 만료됩니다.

## File Structure

```text
.
├── app.py
├── requirements.txt
├── src
│   ├── config.py
│   ├── pipeline.py
│   ├── stt_service.py
│   ├── translation_service.py
│   └── tts_service.py
├── notebooks
│   └── kaggle_voice_translator.ipynb
├── docs
│   └── model_survey.md
└── SUBMISSION.md
```
