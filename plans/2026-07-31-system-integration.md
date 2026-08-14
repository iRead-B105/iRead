---
type: Execution Plan
title: "iRead 5개 서브모듈 시스템 통합"
description: "5개 서브모듈(backend·ai·frontend-web·frontend-app·eyetracking)을 한 환경에서 종단 동작시키기 위한 통합 실행 계획. 6개 핵심 흐름(실력도전·학습·시선·스토리·음성·인증)의 코드 줄 단위 진단 결과를 의존순 단계로 정리한다."
tags: [plan, system-integration, backend, frontend-app, ai, eyetracking, gaze, auth]
timestamp: 2026-07-31T00:00:00+09:00
---
# iRead 5개 서브모듈 시스템 통합

- 상태: draft
- 작성일: 2026-07-31
- 근거 문서: [시스템 통합 작업용 하네스](../docs/architecture/system-integration-harness.md)

> 이 계획은 코드를 직접 수정하지 않고, 6개 흐름을 코드 줄 단위로 끝까지 추적한 진단 결과를 바탕으로 작성했다. 각 작업 항목에는 구현 에이전트가 바로 점프할 수 있도록 `file:line` 근거를 붙였다. 서브모듈 코드는 수정 중일 수 있으니 작업 시 최신 코드로 교차 확인할 것.

## 배경 · 목표

사용자가 제기한 증상 — **“실력 도전에서 테스트를 다 해도 결과가 백엔드를 거쳐 아동 DB에 업데이트되지 않는다”** — 는 단일 버그가 아니라 **여러 흐름이 서로 다른 원인으로 끊겨 있는** 상태의 대표 사례다. 진단 결과, 5개 서브모듈을 한 환경에서 종단 동작시키려면 아래가 모두 필요하다.

1. **기동 경로 단일화** — `compose.yml`과 `start-all-local.bat`이 서로 다른 DB·JWT·포트·AI 구현을 가리키고, bat은 백엔드조차 띄우지 않는다.
2. **데이터 반영 결함 수정** — 실력도전 완료가 프로필/성장을 갱신하지 않는 코드 누락, 시선 분석 결과가 저장되지 않는 호출 누락, 가짜 데이터가 진짜처럼 DB에 쓰이는 mock 토글 기본값.
3. **실제 AI 서비스 진입** — `services/ai`가 compose에 없고(WireMock 빈 매핑), evaluate/transcribe/synthesize 엔드포인트가 AI에 없다.
4. **시선 통합** — eyetracking→백엔드 직송 경로가 인증·호출순서·페이로드 4중 결함으로 단 한 건도 성공 못 함.
5. **교사↔아동 연동 · 운영 배포 준비** — 두 프론트 세션이 단절되어 있고, 운영 배포 시 CORS/쿠키가 실패한다.

**목표**: 데모(mock) 모드 → 실제 AI → 시선 통합 → 운영 준비의 단계적 경로에서, 각 단계 끝에 “이 단계가 동작한다”를 검증 가능한 상태로 만든다.

## 범위

**포함**
- 기동 정본 확정 및 환경(credentials·JWT·브랜치) 정합
- 6개 흐름의 데이터 반영 결함 수정(실력도전·학습·시선·스토리·음성·인증)
- `services/ai`의 compose 진입과 안전 엔드포인트 실연동
- eyetracking↔백엔드 시선 체인 정합
- 교사↔아동 세션 연동 설계와 운영 CORS/쿠키 준비

**제외**
- 실제 LLM 기반 콘텐츠 생성 엔진 도입(현재 `services/ai`는 결정적 mock + Azure 발음뿐). mock 품질 개선과 엔드포인트 구현까지만.
- 프로덕션 인프라(S3·CDN·Kubernetes) 구성 — 본 계획은 로컬/데모 통합이 목표.
- 테스트 코드 전면 재작성 — 각 결함에 대한 회귀 검증만 추가.

## 진단 요약 (결함 → 단계 매핑)

| 결함 | 근거 | 심각도 | 처리 단계 |
| --- | --- | --- | --- |
| **실력도전 완료가 프로필/성장 미갱신** | `AppTestService.java:476-558`에 `studentFeatureProfileService.recalculate` 누락(일반 훈련 `TrainingService.java:344`는 호출) | **P0** | Phase 2 |
| `start-all-local.bat`이 백엔드 미기동 + 두 compose credentials/포트/JWT 충돌 | `start-all-local.bat:26-27` vs `services/backend/docker-compose.yml:1-75`; `compose.yml:8-13,72` | **P0** | Phase 0 |
| eyetracking→백엔드 직송 경로 4중 결함(인증·순서·페이로드·비활성) | `backend_gaze_client.py:60-72,86-103`; `GazeService.java:163-165,275-287`; `gaze_payloads.py:138-167` | **P0** | Phase 4 |
| gaze 분석 결과 미저장 → 교사 앱 404 | 프론트가 `analysis-results` 미호출(`apiLearnerGazeRepository.ts`에 메서드 없음) | **P0** | Phase 2 |
| `services/ai` compose 누락(빈 WireMock) + 미구현 엔드포인트 3종 | `compose.yml:42-50`; AI `app.py`에 evaluate/transcribe/synthesize 없음 | **P0** | Phase 3 |
| 가짜 gaze/음성이 진짜처럼 DB 저장 | `VITE_MOCK_*` 기본 `true`(`mockDeviceSubmissions.ts:13-24`) | **P1** | Phase 2 |
| AI_MOCK_EVALUATE=false 시 학습 완료 롤백 | `TrainingService.java:328-335` → AI evaluate(미구현) 404 → 롤백 | **P1** | Phase 3 |
| TTS 10바이트 스텁 → 재생 불가 / 분기 STT 항상 고정값 | `MockSpeechProcessor.java:11-28` | **P1** | Phase 3 |
| 스토리 문장 발음 평가 UI 미호출 → STORY word_attempt_logs 0건 | `StoryReaderView`에 `transcribeLine` 호출 없음 | **P1** | Phase 2 |
| 교사(web)↔아동(app) 세션 완전 단절 | `linkedStudents` 자체 나열, 핸드오프 코드 0건 | **P1** | Phase 5 |
| 운영 배포 시 CORS/쿠키 실패 | `SecurityConfig.java:80-87`; `AuthCookieService.java:41-42` localhost·SameSite=Strict·Secure=false | **P1** | Phase 5 |
| TRACE/시선 문항 word_attempt_logs 미기록 / saveWordAttemptLogs no-op | `AppTrainingService.java:286-369`; `TrainingService.java:436-564` | **P2** | Phase 2 |
| 장치 상태 SoT 2중 / simulation 프레임 무시 | `GazeService.java:49-57`; `useTobiiGazeBridge.ts:553-555` | **P2** | Phase 4 |
| 서브모듈 브랜치 불일치(detached·feature 혼재) | `git submodule status` | **P1** | Phase 0 |

> 흐름별 상세 진단은 각 에이전트 보고(본 세션)를 참조. 본 문서는 실행 관점으로 압축했다.

## 통합 의존 그래프

```
Phase 0  기동 정본 확정 + 브랜치/환경 정합
   │
   ▼
Phase 1  데모 체인 가동(compose + mock AI + 두 프론트)  ← verify_realtime_demo.mjs
   │
   ▼
Phase 2  데이터 반영 결함 수정(test 프로필·gaze 분석·mock 토글·story 발음)  ← 사용자 제기 문제 핵심
   │
   ├──────────────┐
   ▼              ▼
Phase 3       Phase 4
실제 AI 진입   시선(gaze) 통합
   │              │
   └──────┬───────┘
          ▼
Phase 5  교사↔아동 연동 + 운영 CORS/쿠키 + 통합 E2E CI
```

Phase 3과 Phase 4는 서로 독립이나 모두 Phase 2(데이터 반영) 이후에 실행한다. Phase 4의 eyetracking→백엔드 연동은 Phase 3의 AI 토글 정책과 충돌하지 않는다(gaze는 AI 비의존).

---

## Phase 0 — 기동 정본 확정 & 환경 정합

**목표**: 통합 작업의 출발점을 하나로 고정한다. 두 기동 경로 충돌과 브랜치 불일치를 먼저 끝낸다.

**작업**
- [ ] **P0-A. 루트 `compose.yml`을 통합 정본으로 확정** — `start-all-local.bat`이 `services/backend/docker-compose.yml`을 가리키는데 거기엔 `backend` 서비스도 `demo` profile도 없다(`services/backend/docker-compose.yml:1-75`, `start-all-local.bat:26-27`). 루트 compose만 백엔드를 띄운다. 결정을 ADR(또는 메모)로 남기고, bat은 “eyetracking 로컬 helper + 프론트 로컬 실행 전용”으로 라벨링.
- [ ] **P0-B. 서브모듈 detach 해제 + 브랜치 정합** — backend/ai/frontend-web은 detached at origin/HEAD이므로 `develop` 체크아웃.
  - **frontend-app (결정 M1)**: `feature/learner-ui-design-refresh`(develop 대비 16커밋, develop 최신 이미 머지, 시선 token 보정 포함)를 **develop로 머지해 통합 베이스로 채택**. 작업 트리가 dirty(`TrainingLessonView` 관련 + `developer/` 치트 도구, 다른 에이전트 수정 중)이므로 **정리 후 머지**.
  - **eyetracking (결정 M2)**: `feature/tobii-gaze-calibration-sync`(백엔드 연동 +4커밋, 새 `backend_gaze_client.py`/`gaze_payloads.py`)를 **체크아웃해 통합 베이스로 채택**. 경로C(eyetracking→백엔드 직송) 코드 확보, Phase 4에서 4중 결함 수정.
- [ ] **P0-C. JWT 시크릿 단일 출처화** — 현재 3곳에서 각각 다른 값: `compose.yml:72`, `application-local.properties:15`, `start-all-local.bat:6`. 루트 `.env`로 단일화하고 compose가 읽도록 수정.
- [ ] **P0-D. credentials/포트 충돌 해소** — 루트 compose(MySQL 3307/`iread_demo`/`iread`)와 backend compose(3306/`iread`/`ssafy`)가 상호 배타. 정본(compose.yml) 기준으로 `application-demo.properties` datasource가 맞물리는지 확인.
- [ ] **P0-E. `frontend-app` 작업트리 정리** — `TrainingCurriculumPath.vue` 등 dirty 파일 커밋/스태시. (다른 에이전트가 동시 수정 중일 수 있으니 조정 필수)

**검증**
- `git submodule status`가 모두 브랜치(detached 아님)를 가리킨다.
- `docker compose -f compose.yml config`가 유효하고, backend 서비스가 정의에 있다.
- JWT 시크릿이 단일 출처에서 주입된다(grep으로 한 곳만).

**의존**: 없음(최우선). 단 M1/M2 결정이 선행.

---

## Phase 1 — 데모 통합 체인 가동 (mock 기반)

**목표**: 현재 `compose.yml` 파일 그대로 백엔드 + 두 프론트 + DB가 mock 모드로 종단 동작함을 확인한다. 진단상 demo 프로필(`ai.mock-*=true`)에서는 빈 WireMock이어도 AI 호출을 안 하므로 이미 거의 동작한다.

**작업**
- [ ] **P1-A. `ai-mock` healthcheck 추가** — `compose.yml:42-50`에 healthcheck 블록이 없다. `depends_on: ai-mock: service_healthy`가 있지만 healthcheck 미정의 서비스는 즉시 healthy로 간주된다. WireMock `/health` 추가.
- [ ] **P1-B. 통합 기동** — `docker compose up -d` 후 7컨테이너(mysql/redis/ai-mock/mailpit/backend/frontend-web/frontend-app) running/healthy 확인.
- [ ] **P1-C. 로그인 검증** — 교사 `demo@iread.local`/`demo1234`(frontend-web:5173), 아동 학생 로그인 studentId=2001(frontend-app:5174).
- [ ] **P1-D. 실시간 검증** — `node tools/verify_realtime_demo.mjs` 통과(교사↔아동 SSE 각 ≤3000ms).
- [ ] **P1-E. mock 모드 학습/스토리 종단 확인** — 학습 레슨 1개 완료, 스토리 1편 완료(캐릭터 생성)가 2xx로 성공하는지. 이 단계에서는 AI가 mock이므로 발음/생성은 가짜값이어도 흐름은 완료되어야 한다.

**검증**
- `GET http://localhost:8080/swagger-ui.html` 응답.
- 교사/아동 로그인 각각 access 토큰 + refresh 쿠키 획득.
- `verify_realtime_demo.mjs` 종료 코드 0.
- 학습 완료 후 `trainings.status=COMPLETED` 조회.

**의존**: Phase 0 완료. eyetracking/실제 AI는 이 단계에서 제외(Phase 3·4).

---

## Phase 2 — 데이터 반영 결함 수정 (사용자 제기 핵심)

**목표**: 아동 활동 결과가 DB에 정확히 반영되고 교사가 볼 수 있게 한다. **사용자 증상(실력도전 DB 미반영)의 근본 수정이 이 단계의 1순위다.**

> 진단 결론: 실력도전 complete는 2xx로 성공하지만 `AppTestService.complete`에 `studentFeatureProfileService.recalculate(student)` 호출이 빠져 있어 프로필/성장 DB가 갱신되지 않는다(일반 훈련 `TrainingService.completeTraining:344`와 비대칭). 또한 `students` 테이블에 growth/accuracy 컬럼 자체가 없고 `student_feature_profiles`만 있는데, 이를 갱신하는 경로가 test에 없다. mock 토글 탓이 아니다.

**작업**
- [ ] **P2-A. [P0] 실력도전 완료 프로필 갱신** — `AppTestService.java:476-558`(complete)에서 `test.complete()`/`testCurriculum.complete()` 이후 `studentFeatureProfileService.recalculate(test.getStudent())` 호출 추가. 생성자(`AppTestService.java:83-116`)에 `StudentFeatureProfileService`(필요시 `GrowthService`) 의존성 주입, 테스트용 생성자(`:118-139`)도 동일하게 맞춤. `TrainingService.java:344`와 동일 계약.
- [ ] **P2-B. [P0] test 결과 성장 집계 포함 (결정 M3)** — `GrowthService.java:29-`의 `getGrowth`가 현재 `trainings` 기반만(`GrowthArea.fromTemplateId`). **test 결과를 성장 이력에 포함**하도록 확장. `ReportService.java:194-199`가 이미 `tests.accuracy`를 growth history로 쓰는 패턴 참고. P2-A(recalculate)로 갱신되는 `student_feature_profiles`와 연동.
- [ ] **P2-C. [P0] gaze 분석 결과 저장(교사 앱 404 해결)** — 프론트 경로B가 `analysis-results`를 호출하지 않아 `gaze_analysis_results`가 비고 교사 `GazeAdminController`(`GazeAdminController.java:17-35`)가 404. `apiLearnerGazeRepository.ts`에 `submitAnalysis(sessionId, payload)` 메서드 추가하고 `TrainingLessonView.vue:797`(end 이후)에서 호출. 백엔드는 `GazeService.saveAnalysisResult`(`GazeService.java:159-187`)가 이미 구현되어 있으므로, **end로 COMPLETED를 만든 뒤** analysis를 보내야 함(순서 주의 — Phase 4 D1 참조).
- [ ] **P2-D. [P1] mock 토글 기본값 false** — `mockDeviceSubmissions.ts:13-24`의 `VITE_MOCK_DEVICE_SUBMISSIONS/VOICE/GAZE` 최상위 기본값을 `false`로. `.env.example`·`.env.test`·`.env.local` 점검. 프로덕션 빌드에서 가짜 gaze/음성이 DB에 쓰이는 것을 차단(`TrainingLessonView.vue:786-789` 분기).
- [ ] **P2-E. [P1] 스토리 문장 발음 평가 UI 연결** — `StoryReaderView`가 `learnerStoryRepository.transcribeLine`(→`POST .../speech`)을 호출하지 않아 STORY `word_attempt_logs`가 0건(dead 경로). `StoryService.transcribeStoryLine`(`StoryService.java:253-305`)가 이미 word_attempt 저장 로직을 가지므로 UI만 연결. 단 AI `/speech` 엔드포인트가 없으므로 Phase 3 완료 후 활성화(또는 mock 발음으로 임시). 프론트 `LearnerStorySpeechResult`(`repository.ts:10-14`)가 백엔드 발음 점수를 버리는 스키마 불일치도 정리.
- [ ] **P2-F. [P2] TRACE/시선 문항 word_attempt_logs 기록** — `AppTrainingService.saveSelection`(`AppTrainingService.java:286-369`)이 `result.submissions`만 갱신하고 gaze 단어 시도를 안 남김. GAZE-only 문항의 단어 시도를 `word_attempt_logs(use_location=TRAINING)`에 정합(또는 의도적 분리면 문서화).
- [ ] **P2-G. [P2] `saveWordAttemptLogs` dead 경로 정리** — `TrainingService.java:436-564`가 정상 흐름에서 한 건도 안 쓰는 no-op. `wordAttemptLogId` 있는 항목 skip(`:444-446`) 때문. 비활성 경로 제거 또는 활성화 결정.
- [ ] **P2-H. [P2] 신규 커리큘럼 즉시 생성 옵션** — `CurriculumGenerationScheduler.java:21`가 매일 03:00만 실행 → 오늘 다 끝내도 다음 커리큘럼이 내일 03:00까지 NOT_READY. 완료 시점(`TrainingService.java:345-347` `createNextIfAbsent`)에 데이터 생성을 트리거하거나 온디맨드 생성 도입.

**검증**
- **[사용자 증상 직접 검증]** 실력도전 1문항 완료 → `complete` 2xx → `tests.status=COMPLETED` **및** `student_feature_profiles` 행 갱신을 직접 쿼리로 확인(P2-A).
- 교사 웹에서 해당 아동의 시선 분석(`GET /api/admin/test/{sid}/{testId}/gaze-analysis`)이 200(P2-C).
- `VITE_MOCK_GAZE_SUBMISSIONS=false` 환경에서 gaze 세션이 실제 샘플로 저장(P2-D).
- 스토리 한 문장 읽기 후 `word_attempt_logs(use_location=STORY)` 1건 이상(P2-E, Phase 3 후).

**의존**: Phase 1 완료. P2-E는 Phase 3(AI `/speech`)에 의존. P2-B는 M3 결정.

---

## Phase 3 — 실제 AI 서비스 진입

**목표**: 빈 WireMock을 실제 `services/ai`로 교체하고, 안전한 엔드포인트(생성·발음평가)를 실연동한다. 미구현 엔드포인트(evaluate/transcribe/synthesize)는 구현하거나 토글 true로 명시적으로 남긴다.

> 진단 결론: AI `app.py`에 `/trainings/evaluate`·`/speech/transcribe`·`/speech/synthesize`가 없다. `HttpAiClient`가 이들을 호출하면 404 → `AiClientException` → `GlobalExceptionHandler`가 502로 변환. 단 demo 프로필은 `ai.mock-*=true` 강제로 AI 호출 자체를 안 한다(`application-demo.properties:9-11`).

**작업**
- [ ] **P3-A. [P0] `services/ai` compose 서비스 추가** — `ai-mock`(WireMock, 빈 매핑)을 실제 AI로 교체. `services/ai/Dockerfile` 기반 빌드, healthcheck(`/health`), `env_file: ./services/ai/.env`(AI_INTERNAL_API_KEY, AZURE_SPEECH_KEY/REGION/LANGUAGE). `services/backend/docker-compose.yml:40-62`의 정의를 루트 맞춤으로 가져오되 `context: ../iRead-ai` 경로 오타를 `./services/ai`로 수정.
- [ ] **P3-B. [P0] backend env 주입** — `AI_BASE_URL=http://iread-ai:8080`(컨테이너명 변경 시 동기화), `AI_API_KEY` 추가(현재 `compose.yml:67-77`에 누락). `AI_API_KEY`와 AI `AI_INTERNAL_API_KEY`를 동일값으로.
- [ ] **P3-C. demo 프로필 토글 분리** — `application-demo.properties:9-11`이 `ai.mock-generate/evaluate/speech=true` 강제. 실AI 전환용 프로필을 분리하거나 해당 라인을 제거/수정.
- [ ] **P3-D. [안전] 안전 엔드포인트 실연동** — `AI_MOCK_GENERATE=false`, `AI_MOCK_PRONUNCIATION=false`. `/trainings/candidates`·`/generate`·`/story/*`·`/images/generate`·`/speech/pronunciation/analyze`는 AI에 구현되어 있어 안전.
- [ ] **P3-E. [P0] AI에 미구현 엔드포인트 3종 구현 (결정 M4)** — `services/ai/app.py`에 `/api/v1/trainings/evaluate`·`/api/v1/speech/transcribe`·`/api/v1/speech/synthesize` 추가. backend 호출부(`HttpAiClient.java:115,345,421`)와 `contracts/openapi/ai-api.yaml` 계약에 맞춤(입력·오류·SLO·`X-API-Key`/`Idempotency-Key`). 구현 후 `AI_MOCK_EVALUATE/TRANSCRIBE/TTS=false` 전환 가능 → 현재 `AI_MOCK_EVALUATE=false` 시 학습 완료 롤백(`TrainingService.java:328-335`) 해소. P3-F(TTS)·P3-G(STT)도 이 결정으로 실연동 목표(그 전까지는 mock 폴백 유지).
- [ ] **P3-F. [P1] TTS mock 유효 오디오로 교체** — `MockSpeechProcessor.java:18-28`가 10바이트 ID3 스텁 반환 → 브라우저 재생 실패. 유효한 silent mp3(또는 최소 실제 음성)로 교체. 토글 true 유지 시에도 데모 동작이 가능해야.
- [ ] **P3-G. [P1] 분기 STT mock 가변화** — `MockSpeechProcessor.java:11-16`이 `expectedText` null/blank면 항상 `"친구를 따라간다"` 반환 → 실제 발화 무시. 업로드 메타(길이/해시) 기반 가변 결과 또는 실 STT 구현(M4).
- [ ] **P3-H. [P1] webm→wav 변환 또는 GStreamer** — 프론트는 `audio/webm`만 생성(`useVoiceRecorder.ts:105`), AI 발음 제공자는 파일 그대로 Azure에 넘김(`pronunciation.py:68`). webm 처리엔 GStreamer 필요(AI README). AI 컨테이너에 GStreamer 설치, 또는 백엔드/AI에서 webm→wav(16kHz mono PCM) 변환, 또는 프론트 WAV 녹음.
- [ ] **P3-I. backend-AI 키 정합 재확인** — AI `app.py:200,223-226`가 `/speech/pronunciation/analyze`에서만 `X-API-Key` 검증. `AiClientConfig.java:24-26`가 모든 호출에 헤더 주입. 키 불일치 시 401.

**검증**
- `services/ai` 컨테이너 `GET /health` 200.
- `AI_MOCK_GENERATE=false`에서 훈련 후보 생성 200(`/api/v1/trainings/candidates`).
- `AI_MOCK_PRONUNCIATION=false`에서 녹음 제출 발음평가 200(`/api/v1/speech/pronunciation/analyze`).
- 미구현 엔드포인트가 502를 내지 않음(토글 true 또는 구현).
- webm 녹음 발음평가가 GStreamer 유무와 무관하게 200(P3-H).

**의존**: Phase 0·1. M4 결정이 P3-E를 갈라놓는다.

---

## Phase 4 — 시선(gaze) 통합

**목표**: 실제 Tobii 시선 데이터가 eyetracking → (프론트 집계) → 백엔드 → DB로 정합하게 흐르고, 교사 앱에서 분석 결과가 보인다.

> 진단 결론: 현재 체크아웃(fe60fed)엔 백엔드 직송 코드가 없고 `feature/tobii-gaze-calibration-sync`에만 있다. 사실상 유일한 동작 경로는 프론트 집계→`end`이나 analysis 미호출로 분석 테이블이 비고, eyetracking 직송 경로는 (1) JSESSIONID 쿠키 vs 백엔드 Bearer 인증, (2) analysis→end 호출 순서 역전, (3) end 페이로드에 words 누락, (4) config 기본 비활성 — 4중 결함으로 단 한 건도 성공 못 한다. 집계 SoT는 프론트 `createWordMetrics`이고 백엔드는 재계산하지 않는다.

**작업**
- [ ] **P4-A. eyetracking 통합 베이스 (결정 M2: feature 채택)** — `feature/tobii-gaze-calibration-sync`를 체크아웃(Phase 0 P0-B에서 수행). 경로C(eyetracking→백엔드 직송) 코드(`backend_gaze_client.py`, `gaze_payloads.py`)를 확보했으므로 아래 4중 결함 수정이 본 Phase의 핵심.
- [ ] **P4-B. [P0] eyetracking→백엔드 인증 수정** — `backend_gaze_client.py:86-103`가 `Cookie: JSESSIONID`만 보내나 백엔드는 `Authorization: Bearer`만 본다(`JwtAuthenticationFilter.java:37`) → 401/403. eyetracking이 학생 access 토큰을 Bearer로 전송하도록 변경. 단일 config 세션만 쓰는 문제(다중 학생 미지원)는 P5-E에서.
- [ ] **P4-C. [P0] 호출 순서 표준화** — `backend_gaze_client.py:60-72`가 analysis→end 순서인데, `GazeService.saveAnalysisResult`(`GazeService.java:163-165`)는 `status==COMPLETED`일 때만 허용. **end(COMPLETED) 먼저 → analysis 나중**으로 순서 변경. 단 end에 words/samples 필요(P4-D).
- [ ] **P4-D. [P0] end 페이로드에 words/samples 포함** — `GazeService.java:275-287`(`hasCompletedData`)와 `GazeWordMetricMergeService.java:46-54`(TRAINING/TEST는 words 필수)가 end 데이터를 검사. `gaze_payloads.build_session_data`(`gaze_payloads.py:138-167`)는 `filters/sampleSummary/readingTimeMs/samplingHz`만 생성하고 words가 없음 → COMPLETED 불가. `build_word_attempts` 결과를 end `data.words[]`에 포함.
- [ ] **P4-E. 시선 집계 활성 경로 = 경로B(프론트 집계) 전환 (M5 재결정 2026-08-01)** — 백엔드 `readMetric`이 questionNo/targetIndex 필수(`GazeWordMetricMergeService.java:226-265`)인데 eyetracking은 문항 컨텍스트가 없어 경로C(직송)가 merge에서 실패. 따라서 **프론트 `TrainingLessonView`가 questionNo/targetIndex와 words를 함께 전송**하는 경로B를 활성 경로로(P2-C). eyetracking 연동 코드(P4-B/C/D)는 `backend.enabled=false`로 비활성화해 두되 제거하지 않는다(롤백 대비). 집계 SoT는 프론트 `createWordMetrics`.
- [ ] **P4-F. [P0] 아동 앱 8765 env화 + 컨테이너 연결 (결정 M1b)** — `useTobiiGazeBridge.ts:94-95`의 `ws://127.0.0.1:8765/gaze`, `http://127.0.0.1:8765/api/mode`를 `VITE_GAZE_WS_URL`/`VITE_GAZE_MODE_URL` 환경변수화. 아동 앱은 **컨테이너**로 실행하므로 호스트의 eyetracking(8765)에 닿으려면 `host.docker.internal:8765` 사용. compose `frontend-app` 서비스에 `extra_hosts: ["host.docker.internal:host-gateway"]` 추가(Linux 호스트 대비). eyetracking 자체는 컨테이너화 불가(Windows/Tobii SDK) → 호스트 로컬 helper 유지.
- [ ] **P4-G. eyetracking config 활성화** — feature `config.example.json`의 `backend` 섹션(`enabled:false` 기본)을 `enabled:true` + `baseUrl` + JWT 토큰(P4-B)으로. 체크아웃 `config.json`엔 backend 섹션 자체가 없음.
- [ ] **P4-H. [P2] 장치 상태 SoT 통일** — `GazeService.java:49-57` `getDeviceStatus`가 항상 `(true,"Web Eye Tracker","READY")`. 한편 `LearnerHeader.vue:208`은 WS 상태로, `LearnerLayout.vue:23`은 백엔드 폴링으로 같은 ref를 덮어쓴다. 백엔드가 8765를 실제 probe 하거나 WS 상태를 단일 SoT로.
- [ ] **P4-I. [P2] simulation 프레임 source 통일** — `tobii_sources.py:50-56`가 `source:"simulation"`인데 `useTobiiGazeBridge.ts:553-555`가 `source!=="tobii"`면 무시. 시뮬레이션 모드가 동작하려면 source를 `tobii`로 또는 필터 완화.
- [ ] **P4-J. [P2] TrainingService 더미 어댑터 정리** — `TrainingService.java:457-479`가 gaze 값이 통째로 null이면 `DeterministicGazeWordAnalysisAdapter`로 가짜 메트릭 주입(`GAZE_MOCK_V1`). P4-D로 값이 전달되면 자동 비활성 확인, 잔류 시 값 누락→skipped 처리로 변경(SoT 오염 방지).

**검증**
- 8765 native 모드에서 `useTobiiGazeBridge`가 `source:"tobii"` 프레임 수신(P4-I).
- 학습 세션 gaze start → end(COMPLETED) → analysis-results 순서로 200(P4-C/D).
- `gaze_analysis_results` 행 생성, 교사 앱 `/api/admin/.../gaze-analysis` 200.
- `VITE_MOCK_GAZE_SUBMISSIONS=false`에서 실제 샘플이 `gaze_sessions.data_url`에 저장.
- eyetracking 직송 경로C 활성 시(P4-A feature) 세션이 RUNNING 잔류 없이 종료.

**의존**: Phase 2(P2-C analysis 호출). M2(M4 경로 베이스)·M5(SoT 경로) 결정.

---

## Phase 5 — 교사↔아동 연동 & 운영 배포 준비

**목표**: 교사가 지정한 아동이 앱에 전달되고, 운영 배포 시 CORS/쿠키가 실패하지 않는다.

> 진단 결론: 인증 체인 자체는 정합(audience 3종 `admin-app`/`learning-app`/`learning-bootstrap` 분리, `StudentResourceAccessPolicy` 견고, dev proxy로 동작). 그러나 교사(web)↔아동(app) 세션이 완전 단절(web의 `selectedStudentId`가 백엔드/앱으로 흐르지 않음), 운영 배포 시 SameSite=Strict + localhost CORS + Secure=false가 한꺼번에 실패 가능.

**작업**
- [ ] **P5-A. [P1] 교사↔아동 핸드오프 설계** — web이 선택한 studentId를 담은 단기(예: 60초) 일회성 핸드오프 토큰(`AUD_handoff` 신규 audience + 일회 토큰 테이블 또는 `AuthRefreshSession` 재활용) 발급 → app이 딥링크/QR/코드로 수집 → `student-login` 사전 채움(`JwtTokenService.java:27-29` audience 확장). 현재 핸드오프/deepLink/inviteCode/qr 코드 0건.
- [ ] **P5-B. [P1] CORS 운영화** — `SecurityConfig.java:80-87`의 localhost 하드코드(`5173/4173/5174`, `127.0.0.1:*`)를 `CORS_ALLOWED_ORIGINS` 설정 주입화.
- [ ] **P5-C. [P1] 쿠키 운영화 (결정 M6: 정책 준수)** — `AUTH_COOKIE_SECURE` 기본 false(`application.properties:12`, `AuthCookieService.java:41`) → 운영 프로필 `true` 강제. SameSite/Domain/origin은 [인터페이스 원칙](../docs/architecture/interface-principles.md)(인증·역할·소유권 검사, 비밀값 보호)을 준수하며 운영 토폴로지(동일 사이트 역프록시 권장)에 맞춰 확정. 구체값은 운영 배포 ADR로.
- [ ] **P5-D. [P2] 통합 E2E CI** — `.github/workflows`에 `docker compose up` + `verify_realtime_demo.mjs` 자동화. 현재 문서/계약 정적 검증만.
- [ ] **P5-E. [P2] eyetracking 다중 학생 지원** — 현재 config 단일 세션(`backend.sessionCookie`)만 → 다른 studentId 호출 시 `requireSameStudent` 403. 학생별 토큰 발급 또는 기기-학생 매핑(P4-B 인증과 연동).

**검증**
- web에서 아동 선택 → app이 딥링크로 해당 아동 컨텍스트로 진입(P5-A).
- 운영 도메인(또는 동일 사이트 역프록시)에서 refresh 쿠키 전달 + 자동 갱신 성공(P5-B/C).
- E2E CI가 PR마다 통합 기동 + 실시간 검증(P5-D).

**의존**: Phase 2~4. 운영 토폴로지 확정(동일 사이트 여부)이 P5-C를 갈라놓는다.

---

## 전체 검증 (통합 완료 정의)

아래가 모두 성립할 때 “5개 서브모듈 시스템 통합 완료”로 선언한다.

**데모(mock) 통합**
- [ ] `docker compose up -d`로 7컨테이너 healthy, `verify_realtime_demo.mjs` 통과.
- [ ] 교사/아동 로그인 → 학습·실력도전·스토리 각 1회 완료 2xx.

**데이터 반영**
- [ ] **[사용자 증상]** 실력도전 완료 후 `student_feature_profiles` 갱신 직접 쿼리 확인.
- [ ] 교사 웹 시선 분석(`gaze-analysis`)·보고서가 404 없이 조회.
- [ ] `VITE_MOCK_*`·`AI_MOCK_*` 토글이 의도한 값이며 가짜 데이터가 DB에 섞이지 않음.

**실제 AI**
- [ ] `services/ai` 컨테이너 `/health` 정상, 안전 엔드포인트 실연동, 미구현 엔드포인트 502 없음.

**시선**
- [ ] 8765 native 모드 gaze 프레임 수신 → 세션 start→end→analysis 200 → `gaze_analysis_results` 채워짐 → 교사 앱 조회 200.

**운영 준비**
- [ ] 교사→아동 핸드오프 동작, 운영 CORS/쿠키 설정 적용, 통합 E2E CI 통과.

## 결정 사항 (2026-07-31 확정)

- **M1. `frontend-app` 브랜치** — ✅ `feature/learner-ui-design-refresh` → develop 머지. develop 최신을 이미 머지하여 fast-forward에 가깝고 시선 token 보정 포함. dirty 정리 후 머지.
- **M1b. 아동 앱 배포 방식** — ✅ **컨테이너**. 아동 앱은 compose 컨테이너로 실행, eyetracking(8765)은 호스트 로컬 helper → `host.docker.internal:8765`로 연결(P4-F).
- **M2. eyetracking 통합 베이스** — ✅ `feature/tobii-gaze-calibration-sync` 채택. 백엔드 연동 코드 확보, Phase 4에서 4중 결함(인증·순서·words·활성) 수정.
- **M3. test 결과 성장 집계** — ✅ **포함**. `GrowthService`가 test 결과를 성장 이력에 반영(P2-B).
- **M4. 미구현 AI 엔드포인트** — ✅ **AI에 구현**. `services/ai`에 `/trainings/evaluate`·`/speech/transcribe`·`/speech/synthesize` 추가(P3-E). 토글 false 전환 가능.
- **M5. 시선 집계 활성 경로** — ✅ **경로B(프론트 집계)로 전환**(재결정 2026-08-01). 백엔드 `readMetric`이 questionNo/targetIndex 필수(`GazeWordMetricMergeService.java:226-265`)인데 eyetracking은 문항 컨텍스트가 없어 경로C(직송)가 merge에서 기술적 실패. 프론트 `TrainingLessonView`가 questionNo/targetIndex와 words를 전송(P2-C). eyetracking 연동 코드(P4-B/C/D)는 `enabled=false`로 남겨둠.
- **M6. 운영 CORS/쿠키** — ✅ **정책 준수**. `interface-principles.md`(인증·역할·소유권 검사, 비밀값 보호)에 맞춰 Phase 5에서 SameSite/Secure/origin 확정. 구체 토폴로지는 운영 ADR로.

## 진행 기록

- **2026-08-01: 안전 영역 1차 구현 완료.** 다른 에이전트 동시 작업(`frontend-app`/`backend`) 영역은 대기.
  - **완료(코드)**: P2-A 실력도전 `recalculate`(`backend/AppTestService.java`); P3-E AI 엔드포인트 3종 evaluate/transcribe/synthesize(`services/ai` app.py·generation_models.py·mock_generators.py); P3-A compose `services/ai` 진입 + `AI_API_KEY`(`compose.yml`); P4-B/C eyetracking 인증(Bearer)·호출순서(end→analysis), P4-D words/samples + `config.example.json` accessToken(`services/eyetracking`, feature 브랜치).
  - **완료(계약/문서)**: M5 재결정(경로B 전환 — 백엔드 `readMetric` questionNo/targetIndex 필수라 eyetracking 직송 불가); ai-api.yaml 스키마 4종 보강.
  - **검증**: services/ai·eyetracking `py_compile` ✅, `docker compose config` ✅, `validate_contracts` ✅, `validate_harness` ✅. 백엔드 `gradlew` 빌드는 다른 에이전트 동시 작업으로 보류.
  - **대기(다른 에이전트 정리 후)**: P4-E/F(프론트 경로B 활성·8765 env), P2-C/D/E(gaze analysis-results 호출·mock 토글 false·스토리 발음 UI), P3-C/D(백엔드 토글 false 전환·demo 프로필 분리), P5-A/B/C(교사↔아동 핸드오프·CORS·쿠키), P0-B(frontend-app feature→develop 머지).
  - **주의**: P4-B/C/D eyetracking 코드는 M5=경로B 전환으로 `backend.enabled=false`면 직접 쓰이지 않으나 롤백/참고용 보존.

## 롤백 / 위험

- **Flyway 기준선** — `V1__baseline_schema.sql`·`V2__demo_seed.sql`은 단일 기준선. 스키마 변경 시 `V3+` 추가만 허용(기존 덮어쓰기 금지, 체크섬 민감). demo 프로필 재시작 시 데모 데이터 초기화됨.
- **AI 토글 전환** — `AI_MOCK_EVALUATE=false` 즉시 학습 완료 롤백(AI evaluate 미구현). 전환은 P3-E 해소 후.
- **eyetracking 브랜치 전환** — feature→develop 되돌릴 때 백엔드 연동 코드 손실. M2 확정 후에만.
- **동시 수정 충돌** — 다른 에이전트가 코드 수정 중일 수 있음. 각 Phase 시작 전 작업 트리 최신화 및 조정.

## 관련 문서

- [시스템 통합 작업용 하네스](../docs/architecture/system-integration-harness.md) — 서비스 카드·위험 레지스터
- [교수자 Web–아동 App 실시간 데이터 연동](2026-07-31-teacher-learner-data-linkage.md) — Phase 5 실시간 연동 상세
- [Azure Speech 단어 단위 발음 평가 연동](2026-07-28-azure-speech-pronunciation-assessment.md) — Phase 3 발음 연동
- [맞춤 훈련 데이터 생성 파이프라인](2026-07-28-personalized-training-generation.md) — Phase 2·3 훈련 생성
- [데모 Flyway 기준선 통합](2026-07-30-demo-flyway-squash.md) — 롤백/마이그레이션
- [인터페이스 원칙](../docs/architecture/interface-principles.md), [계약 카탈로그](../contracts/catalog.md)
