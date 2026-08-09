# 외부 서비스 설정

iRead는 로컬 Docker만으로 기본 화면과 저장 흐름을 확인할 수 있고, 실제 AI·음성·메일·시선 추적 기능은 외부 서비스 설정에 따라 활성화된다. 사용하지 않는 공급자의 키는 만들거나 입력할 필요가 없다.

## 1. 서비스 목록

| 서비스 | 사용 기능 | 로컬 대체 | 비밀값 또는 로컬 설정 |
| --- | --- | --- | --- |
| Azure AI Speech | 발음 평가, STT, TTS | Backend speech mock 또는 AI deterministic provider | `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION` |
| SSAFY GMS | 훈련·이야기 텍스트, 이미지 또는 STT | mock provider | `GMS_KEY` |
| OpenAI API | 훈련·이야기 텍스트 또는 이미지 | mock provider | `OPENAI_API_KEY` |
| Gemini API | 훈련·이야기 텍스트와 장면 이미지 | disabled/mock provider | `GEMINI_API_KEY` |
| SMTP | 비밀번호 재설정 이메일 | Docker의 Mailpit | SMTP 계정과 비밀번호 |
| Tobii | 실제 시선 좌표 | 마우스 pointer fallback 또는 simulation | 로컬 SDK·driver·장치 설정 |

키는 `services/ai/.env` 또는 배포 시스템의 secret manager에 저장한다. 실제 키를 `exec/`, `.env.example`, issue, commit, 로그와 화면 캡처에 넣지 않는다.

## 2. Backend와 AI 서비스 공통 인증

Backend는 AI 서비스의 모든 내부 API에 `X-API-Key`를 보낸다. 두 설정값은 반드시 같아야 한다.

루트 `.env`:

```text
AI_API_KEY=<32자 이상의 임의 공유 키>
```

`services/ai/.env`:

```text
AI_INTERNAL_API_KEY=<루트 AI_API_KEY와 같은 값>
```

공유 키가 다르면 Backend의 AI 요청은 HTTP 401로 실패한다.

## 3. Azure AI Speech

### 3.1 용도

- 한국어 scripted Pronunciation Assessment
- 이야기·훈련 음성 STT
- 이야기 문장과 학습 화면 TTS

### 3.2 리소스 준비

1. [Azure Portal](https://portal.azure.com/)에 로그인한다.
2. Speech service 리소스를 생성한다.
3. 시연 서버와 가까운 region을 선택한다. 현재 예시는 `koreacentral`이다.
4. 리소스의 `Keys and Endpoint`에서 key와 region을 확인한다.
5. key는 secret으로 보관하고 문서나 Git에 기록하지 않는다.

### 3.3 환경변수

`services/ai/.env`:

```text
AI_PRONUNCIATION_PROVIDER=azure
AI_SPEECH_PROVIDER=azure
AZURE_SPEECH_KEY=<발급받은 키>
AZURE_SPEECH_REGION=koreacentral
AZURE_SPEECH_LANGUAGE=ko-KR
AZURE_SPEECH_VOICE=ko-KR-SunHiNeural
```

루트 `.env`에서 실제 음성 호출을 사용할 기능을 `false`로 둔다.

```text
AI_MOCK_PRONUNCIATION=false
AI_MOCK_TRANSCRIBE=false
AI_MOCK_TTS=false
```

Backend 학습 화면 TTS voice는 `APP_TTS_VOICE`로 별도 지정할 수 있다. AI 서비스의 `AZURE_SPEECH_VOICE`와 같은 voice로 맞추면 화면별 목소리가 일치한다.

### 3.4 확인

```bash
docker compose up -d --build ai backend
docker compose logs --tail=100 ai
curl http://localhost:8081/health
```

음성 파일은 30초 미만의 한국어 발화를 사용한다. Azure key, SDK 원본 응답과 전체 음성 원본을 로그에 남기지 않는다.

## 4. 텍스트·이미지 생성 공급자

훈련과 이야기 텍스트, 이야기 장면 이미지는 각각 독립적으로 공급자를 선택한다. 하나의 기능에 여러 실제 공급자를 동시에 지정하지 않는다.

### 4.1 공통 선택 변수

`services/ai/.env`:

```text
# 훈련·추천 생성: mock, gms, gemini, openai
AI_GENERATION_PROVIDER=mock

# 이야기 텍스트: mock, gms, gemini, openai
STORY_TEXT_PROVIDER=mock
STORY_TEXT_MODEL=gpt-5.4-mini

# 이야기 이미지: disabled, gms, gemini, openai
STORY_IMAGE_PROVIDER=disabled
STORY_IMAGE_MODEL=gemini-2.5-flash-image
```

실제 공급자를 선택했다면 루트 `.env`의 해당 Backend mock switch도 `false`로 설정한다.

```text
AI_MOCK_GENERATE=false
AI_MOCK_STORY=false
AI_MOCK_IMAGE=false
```

공급자 호출 없이 결정적 시연 데이터를 사용할 때는 Backend mock switch를 `true`로 두고 AI provider도 `mock` 또는 `disabled`를 사용한다.

### 4.2 SSAFY GMS

1. SSAFY에서 안내한 GMS 서비스에 로그인한다.
2. 프로젝트에서 사용할 API key를 발급한다.
3. key의 사용 범위와 quota를 확인한다.
4. 다음 값을 `services/ai/.env`에 입력한다.

```text
GMS_KEY=<발급받은 키>
GMS_BASE_URL=https://gms.ssafy.io/gmsapi
AI_GENERATION_PROVIDER=gms
STORY_TEXT_PROVIDER=gms
```

GMS를 통한 Gemini 이미지가 필요하면 `STORY_IMAGE_PROVIDER=gms`를 사용한다. 모델과 quota는 시연 전에 GMS에서 실제 제공되는 값으로 확인한다.

### 4.3 OpenAI 직접 호출

1. [OpenAI API platform](https://platform.openai.com/)에서 프로젝트와 API key를 만든다.
2. 프로젝트 budget과 rate limit을 설정한다.
3. key를 `services/ai/.env`에 입력하고 사용할 기능의 provider를 `openai`로 바꾼다.

```text
OPENAI_API_KEY=<발급받은 키>
OPENAI_BASE_URL=https://api.openai.com/v1
AI_GENERATION_PROVIDER=openai
STORY_TEXT_PROVIDER=openai
```

사용할 수 없는 모델명을 지정하면 요청 시 공급자 오류가 발생한다. 시연 계정에서 접근 가능한 모델인지 먼저 확인한다.

### 4.4 Gemini 직접 호출

1. [Google AI Studio](https://aistudio.google.com/)에서 API key를 만든다.
2. key 제한과 quota를 확인한다.
3. 텍스트 또는 이미지에 사용할 provider만 `gemini`로 설정한다.

```text
GEMINI_API_KEY=<발급받은 키>
GEMINI_BASE_URL=https://generativelanguage.googleapis.com
GEMINI_OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
AI_GENERATION_PROVIDER=gemini
STORY_TEXT_PROVIDER=gemini
STORY_IMAGE_PROVIDER=gemini
```

이미지 생성은 응답 시간이 길고 요청·응답 크기가 크다. `.env.example`의 timeout과 최대 byte 제한을 유지하고 시연 전 이미지 1건을 미리 생성해 quota와 응답 형식을 확인한다.

### 4.5 생성 기능 확인

```bash
docker compose up -d --build ai backend
docker compose logs -f ai
```

교수자 앱에서 추천 커리큘럼 또는 교안 생성을 요청하거나 아동 앱에서 새 이야기를 시작한다. 성공하면 AI 로그에 key 값이 아닌 provider와 request 식별 정보만 남아야 한다.

## 5. SMTP와 Mailpit

### 5.1 로컬 시연

별도 가입 없이 Compose의 Mailpit을 사용한다.

```text
SMTP host: mailpit
SMTP port: 1025
Mailpit UI: http://localhost:8025
```

교수자 로그인 화면에서 비밀번호 재설정을 요청한 뒤 Mailpit 웹 화면에서 메일과 재설정 링크를 확인한다.

### 5.2 외부 SMTP

실제 이메일을 보낼 때 Backend 실행 환경에 다음 값을 설정한다.

```text
SMTP_HOST=<SMTP 서버>
SMTP_PORT=<포트>
SMTP_USERNAME=<계정>
SMTP_PASSWORD=<비밀번호 또는 앱 비밀번호>
SMTP_AUTH=true
SMTP_STARTTLS=true
AUTH_PASSWORD_RESET_FRONTEND_URL=https://<교수자-도메인>/reset-password
AUTH_PASSWORD_RESET_FROM=<발신 주소>
```

SMTP 가입 절차는 선택한 메일 사업자의 정책을 따른다. 발신 주소 인증, TLS 지원, 발송 quota와 스팸 정책을 시연 전에 확인한다.

## 6. Tobii Eye Tracker

### 6.1 준비

1. Windows PC에 Tobii Eye Tracker 5를 연결한다.
2. [Tobii Gaming 시작 페이지](https://gaming.tobii.com/getstarted/)에서 장치 driver와 Tobii Experience를 설치한다.
3. Tobii Experience에서 사용자 눈 보정을 완료한다.
4. 팀에 제공된 Tobii Game Integration SDK 9.0.4.26을 로컬에 압축 해제한다.
5. Visual Studio 2022 Build Tools에서 `Desktop development with C++` workload를 설치한다.

Tobii SDK, DLL과 빌드된 executable은 라이선스와 PC 환경에 종속되므로 GitLab 저장소에 넣지 않는다.

### 6.2 Native bridge 빌드

```powershell
cd services\eyetracking\native
.\build_native_with_vs2022.bat C:\path\to\tobii_gameintegration_9.0.4.26
```

환경변수 방식:

```powershell
$env:TOBII_GAMEINTEGRATION_SDK_DIR='C:\path\to\tobii_gameintegration_9.0.4.26'
.\build_native_with_vs2022.bat
```

성공하면 `services/eyetracking/native/build/tobii_native_bridge.exe`가 생성된다.

### 6.3 브리지 실행

```powershell
cd services\eyetracking
Copy-Item config.example.json config.json
.\run_server.bat
```

아동 앱이 `/gaze` WebSocket에 연결하면 브리지가 native executable 자동 시작을 시도한다. 장치나 executable이 없으면 simulation 상태가 되며 아동 앱은 마우스 pointer 기반 fallback으로 시연할 수 있다.

### 6.4 확인

```text
브리지 상태: http://localhost:8765/api/status
mode 변경:  http://localhost:8765/api/mode
WebSocket:  ws://localhost:8765/gaze
```

아동 앱 상단 장치 상태와 시선 calibration 화면을 확인한다. 실제 시선 좌표와 로컬 PC 경로가 포함된 로그나 `config.json`을 제출하지 않는다.

## 7. 시연 전 외부 서비스 점검표

- [ ] `AI_API_KEY`와 `AI_INTERNAL_API_KEY`가 같다.
- [ ] 실제로 사용하는 provider의 key만 설정했다.
- [ ] Azure Speech key와 region이 같은 리소스 값이다.
- [ ] 생성 모델이 계정에서 실제 사용 가능하다.
- [ ] 공급자 quota와 결제 한도를 확인했다.
- [ ] Mailpit 또는 외부 SMTP로 재설정 메일을 확인했다.
- [ ] Tobii 장치 사용 시 calibration과 native bridge 실행을 확인했다.
- [ ] `.env`, `config.json`, API key와 비밀번호가 Git에 포함되지 않았다.
