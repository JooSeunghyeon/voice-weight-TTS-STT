# Submission Draft

## Email

To: `kts123@kookmin.ac.kr`

Subject: `[과제 제출] Gradio 기반 Voice Translator 데모`

Body:

```text
안녕하세요.

Gradio 기반 음성 통역 데모 과제 제출드립니다.

1. Kaggle Notebook 주소
- 여기에 Public Kaggle Notebook URL을 입력

2. Public Gradio Demo 주소
- 여기에 Cloudflare trycloudflare URL을 입력

3. 설명 및 실행 스크린샷
- 첨부 파일 또는 본문 이미지로 실행 화면 스크린샷 첨부

4. 숙제 수행 내용 및 소감 요약
- Whisper large-v3-turbo로 음성 인식을 수행하고, NLLB-200 distilled 600M으로 외부 API 없이 로컬 번역을 구현했습니다.
- XTTS-v2를 사용해 입력 음성을 참조한 voice cloning TTS를 연결했습니다.
- Gradio UI에서 한국어와 6개 외국어 간 양방향 통역을 선택할 수 있게 구성했습니다.
- Kaggle GPU 환경에서 실행하고 Cloudflare Tunnel로 public URL을 생성하도록 노트북을 작성했습니다.
- STT, 번역, TTS 모델을 하나의 파이프라인으로 연결하며 음성 AI 서비스 구조를 이해할 수 있었습니다.

감사합니다.
```

## Screenshot Checklist

- Kaggle Notebook이 Public으로 설정된 화면
- GPU가 활성화된 상태 또는 `CUDA available: True` 출력
- Cloudflare `https://*.trycloudflare.com` URL 출력
- Gradio 데모 첫 화면
- 한국어 -> 외국어 실행 결과
- 외국어 -> 한국어 실행 결과
- Recognized text, Translated text, Translated voice 출력이 함께 보이는 화면

## Kaggle Public Checklist

1. Kaggle Notebook 우측 상단 `Share`를 클릭합니다.
2. Visibility 또는 Access 권한을 `Public`으로 변경합니다.
3. Notebook URL을 복사해 이메일의 `Kaggle Notebook 주소` 항목에 붙입니다.
4. Cloudflare URL은 Kaggle 세션 동안만 유지되므로 제출 직전에 다시 실행해 확인합니다.

## Demo Script

1. Gradio public URL에 접속합니다.
2. `Korean to foreign language`와 `English`를 선택합니다.
3. 한국어 음성을 업로드하거나 녹음합니다.
4. `Translate with cloned voice` 버튼을 누릅니다.
5. 인식 텍스트, 번역 텍스트, 합성된 영어 음성을 확인합니다.
6. `Foreign language to Korean`으로 변경한 뒤 영어 또는 일본어 음성으로 다시 테스트합니다.
