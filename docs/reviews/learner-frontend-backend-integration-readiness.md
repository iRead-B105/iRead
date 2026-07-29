# 아동용 Vue–Spring 시스템 통합 전 점검 보고서

- 점검일: 2026-07-29
- 점검 범위: `services/frontend-app`의 아동 화면과 `services/backend`의 `/api/auth/app/**`, `/api/app/**`
- 점검 방식: 소스·라우트·DTO·보안 설정·OpenAPI 계약의 정적 대조
- 제외 범위: 실제 API 호출, 데이터베이스 기동, 코드 연결 및 계약 변경

## 결론

최초 점검 당시처럼 데이터 저장소 함수만 HTTP 호출로 바꾸는 방식으로는 정상 통합되지 않는다. 다만 이번 프론트 준비 작업으로 아동 전용 인증·토큰·API client·repository·DTO mapper·route guard를 분리했기 때문에, **백엔드에 이미 존재하고 계약이 확인된 endpoint는 교수자 코드를 바꾸지 않고 연결할 수 있는 상태**다.

전체 아동 서비스를 한 번에 완성하는 것은 아직 불가능하다. 현재 커리큘럼 조회, 훈련 `generatedData/question` 스키마, 성장 단계 집계, 실력 도전의 검사 매핑, 이야기 음성 분기 UI 계약은 백엔드 또는 제품 결정이 필요하다. 이 기능들은 API 모드에서 목업으로 자동 대체하지 않고 이유를 표시하도록 차단했다.

현재 통합 준비도는 **중간(기존 endpoint 단위 연동 가능, 전체 학습 흐름은 계약 확정 필요)** 으로 평가한다.

- `[ASSUMPTION]` 회사 협의 전까지 아동 UI의 기본 데이터 소스는 `mock`으로 유지한다.
- `[BLOCKED]` current curriculum, 훈련 question schema, 성장 단계, 실력 도전, 이야기 음성 분기의 기준 계약은 백엔드·제품 담당자 확인이 필요하다.

## 2026-07-29 프론트 준비 반영

실제 Backend 연결은 켜지 않은 상태로 다음 통합 경계를 아동 전용 서브모듈인 `services/frontend-app`에 반영했다.

- `VITE_LEARNER_DATA_SOURCE`로 아동 UI의 mock/API 선택을 교수자 설정과 분리했다. 기본값은 `mock`이다.
- bootstrap token과 learning access token을 분리하는 `learnerSession` store와 아동 전용 API client를 추가했다.
- `/learner/login`과 `/learner/**` 전용 인증 guard를 추가했다.
- auth, content, training, story, gaze 기능에 mock/API repository를 분리했다.
- Spring 숫자 ID와 응답 DTO를 현재 아동 화면 모델로 변환하는 경계를 추가했다.
- story session 생성, shelf·line 조회, 훈련 전송, multipart 음성, gaze session 전송 코드를 준비했다.
- Backend에 없는 current curriculum 계약과 제품 규칙이 없는 성장 단계 매핑은 API 모드에서 명시적 계약 오류로 표시하고 mock으로 자동 대체하지 않는다.
- 대응 아동 API가 확정되지 않은 실력 도전도 API 모드에서 로컬 문제를 실행하지 않고 계약 필요 상태를 표시한다.
- 로컬 eye tracker bridge와 cursor는 교수자 화면에서 제거하고 아동 layout 범위에서만 초기화한다.
- API 모드 production build, 타입 검사, lint, Vitest 377개와 mock 로그인 브라우저 흐름을 통과했다.

아래의 원래 점검 항목 중 인증 분리, 라우트 guard, repository 구조와 지원 endpoint 전송 준비는 해소했다. current curriculum, training question schema, 성장 단계, story 표시 필드와 음성 분기 UI는 회사에서 Backend 담당자와 계약을 확정해야 한다.

## 최초 차단 항목의 현재 상태

| 최초 심각도 | 영역 | 현재 상태 | 남은 조건 |
| --- | --- | --- | --- |
| P0 | 로그인 진입점 | 프론트 해결 | `/learner/login` 2단계 로그인과 learner route guard 구현. 실제 cookie/CORS 검증 필요 |
| P0 | 인증 토큰 분리 | 프론트 해결 | bootstrap/learning token과 refresh coalescing 분리. 실제 만료 통합 테스트 필요 |
| P0 | 현재 커리큘럼 | 미해결·명시적 차단 | 아동 권한 current curriculum endpoint 또는 조회 정책 필요 |
| P0 | 훈련 식별자 | 부분 해결 | 숫자 `trainingId` 운반·전송 구현. question JSON 공식 스키마 필요 |
| P0 | 이야기 식별자·표시 데이터 | 부분 해결 | 숫자 ID/session과 line 매핑 구현. shelf 표시 필드·분기 화면 계약 필요 |
| P0 | 로그아웃 | 프론트 해결 | app logout 호출 및 `/learner/login` 이동 구현. 실제 cookie 제거 검증 필요 |

## 기능별 계약 대조

### 1. 인증과 세션

백엔드가 의도한 흐름은 다음과 같다.

1. `POST /api/auth/app/teacher-login`으로 `teacherSessionToken`과 `linkedStudents`를 받는다.
2. bootstrap token을 Authorization 헤더에 넣고 `POST /api/auth/app/student-login`에 숫자형 `studentId`를 보낸다.
3. 반환된 learning access token으로 `/api/app/**`를 호출한다.
4. 만료 시 HttpOnly refresh cookie를 사용해 `POST /api/auth/app/refresh`를 호출한다.

프론트의 `fetchLinkedStudents`, `saveTeacherBootstrapSession`, `saveSelectedStudentSession`은 이름만 위 흐름을 반영하고 실제로는 목업 토큰을 `localStorage`와 `sessionStorage`에 저장한다. `AppTeacherLoginResponse.LinkedStudent`는 `studentId`, `name`, `profileImage`만 제공하지만 프론트 타입은 `age`, `profileColor`, `profileImageUrl`도 필수로 요구한다.

필요 조치:

- learning 전용 session store와 learning 전용 `ApiClient`를 분리한다.
- `/learner/login` 또는 앱 시작 bootstrap 화면과 인증 guard를 추가한다.
- refresh cookie 사용을 위해 `credentials: include`를 유지하고 app refresh/logout을 별도 처리한다.
- access token 저장 위치와 새로고침 복구 정책을 결정한다. 아동용 토큰을 장기 `localStorage`에 두는 방식은 재검토가 필요하다.
- `profileImage` 대 `profileImageUrl`, 누락된 `age/profileColor`의 매핑 또는 계약 확장을 결정한다.

### 2. 오늘의 훈련과 훈련 실행

백엔드의 개별 훈련 실행 API는 시작, intro, 문제 조회, 선택 답안 저장, 녹음 저장, 완료, reset까지 갖춰져 있다. 다만 프론트는 모든 문제와 정답을 번들에 포함하고 브라우저에서 정답을 직접 판정한다.

주요 불일치:

- 현재 커리큘럼을 학습 앱 권한으로 조회하는 API가 없다.
- 프론트 `TrainingLesson`과 백엔드 `generatedData/question` JSON의 공식 discriminator 및 필드 매핑이 없다.
- 프론트는 문자열 `question.id`와 `answer`를 사용하지만 백엔드는 순번과 숫자형 `wordId`를 요구한다.
- 선택형 응답 API는 클라이언트가 `isCorrect`, `totalScore`를 보내도록 되어 있어 프론트의 로컬 판정과 결합하면 조작 가능성과 중복 판정 책임이 생긴다.
- 녹음 UI는 `blob:` URL과 목업 완료 상태만 저장한다. 백엔드는 multipart `audioFile`, `wordId`, `targetIndex`, `expectedText` 등을 요구한다.
- 프론트 `saveResult()`는 700ms 후 무조건 성공하며, 완료 화면 guard도 메모리 상태에 의존한다. 새로고침하면 완료 화면 진입이 깨진다.
- backend status와 frontend의 `COMPLETED/CURRENT/LOCKED`, `PREPARING/READY/REST/COMPLETED` 간 공식 매핑이 없다.

권장 방식:

- 학습용 current curriculum endpoint를 추가하거나 기존 admin endpoint의 책임을 분리한다.
- `activityType`별 question JSON schema를 계약으로 고정한다.
- 프론트 라우트의 공개 slug와 서버의 `trainingId`를 함께 보관하는 route/session 모델을 만든다.
- 답안 판정의 기준 원본을 서버로 통일하고, 프론트는 서버 응답의 `isCorrect`와 점수를 표시한다.
- 각 mutation에 idempotency 또는 중복 제출 처리 규칙을 정한다.

### 3. 이야기

백엔드는 shelf, template 상세, session 시작, resume, line 조회, 분기 음성 업로드, STT, TTS를 제공한다. 기능 범위는 프론트 요구와 대체로 맞지만 DTO 모양은 직접 호환되지 않는다.

주요 불일치:

- shelf의 필드가 프론트 카드 표시에 부족하다.
- 프론트 `MockStoryPage.lines`는 한 페이지에 문자열 배열을 가지지만 백엔드는 `StoryLineResponse.lineText` 한 줄 단위다.
- 프론트는 `imagePosition`, 등장인물, 분기 질문을 기대하지만 현재 응답에 없다.
- 프론트는 새 이야기 선택 시 실제 session 생성 요청 없이 바로 reader route로 이동한다.
- 이어 읽기 위치와 생성 페이지를 `localStorage`에 저장한다. 백엔드 resume 상태와 두 개의 기준 원본이 생긴다.
- 분기 답변은 현재 브라우저 음성 인식/타이머 기반 생성이며 backend multipart branch API를 사용하지 않는다.
- 이야기 완료 시 캐릭터 해금을 로컬 저장소에 기록한다. 백엔드 캐릭터 목록과 동기화되지 않는다.

권장 방식:

- shelf 전용 view DTO를 확장하거나 프론트 어댑터가 template·resume 데이터를 추가 조회하도록 한다.
- `StoryLineResponse[]`를 페이지 단위 UI로 묶는 규칙을 정의한다.
- 진행 위치, 생성 분기, 완료 상태의 기준 원본을 서버로 통일한다.
- 표지와 장면 이미지 URL이 `/uploads` 또는 API base URL 기준인지 명시한다.

### 4. 성장과 캐릭터

성장 응답은 `trainingTemplateId`, `trainingTemplateName`, `completedCount` 목록이다. 프론트는 고정된 세 정원에 대해 `areaId`, `name`, `learningCount`, 1~5단계 `stage`, `updatedAt`을 기대한다. 직접 대입할 수 없으며 template을 세 성장 영역으로 집계하고 단계로 변환하는 규칙이 필요하다.

캐릭터 응답은 보유한 캐릭터의 숫자 ID, story ID, URL, 이름, 생성 시각을 제공한다. 프론트는 문자열 story slug, 종류, story title, 잠금 상태를 포함한 전체 카탈로그를 기대한다. 현재 API만으로는 잠긴 캐릭터와 이야기 제목을 표시할 수 없다.

### 5. 실력 도전

프론트의 `/learner/challenge`는 로컬 문제와 메모리 상태만 사용한다. 대응하는 아동용 challenge API나 명시적인 test API 매핑이 없다. 이를 진단 검사(`/api/app/test/**`)로 연결할지 별도 게임 기능으로 유지할지 제품 결정이 필요하다.

### 6. 시선 추적

프론트는 `ws://127.0.0.1:8765/gaze`와 `http://127.0.0.1:8765/api/mode`로 로컬 브리지에 직접 연결한다. 백엔드는 장치 상태와 보정 안내, 수집 session, 종료, 분석 결과 저장을 담당한다. 두 계층의 책임은 함께 사용할 수 있지만 현재 프론트는 backend gaze API를 한 번도 호출하지 않는다.

추가 위험:

- 로컬 브리지가 없는 환경에서 앱 전체가 재연결을 계속 시도한다.
- gaze bridge와 전역 cursor가 `/learner`뿐 아니라 교수자 화면에서도 `App.vue`에 의해 초기화된다.
- HTTPS로 배포할 경우 브라우저가 `ws://`와 `http://127.0.0.1` 혼합 콘텐츠를 차단할 수 있다.
- 프레임 좌표, viewport 크기, timestamp, sampling rate와 backend `data/sentenceMetrics` 형식이 정의되지 않았다.
- session 시작·종료 실패 시 학습/이야기 완료 transaction과의 순서가 없다.

로컬 장치 연결과 서버 기록을 별도 adapter로 나누고, 아동 route에서만 bridge를 시작하며, backend gaze session lifecycle을 훈련·이야기 session에 결합해야 한다.

## 공통 런타임 위험

| 심각도 | 위험 | 설명 |
| --- | --- | --- |
| P0 | 응답 envelope 미처리 | backend는 일반 응답을 `{ success, data }`로 감싼다. 공용 `ApiClient`는 이를 처리하지만 learner repository가 이를 사용하지 않는다. raw `fetch`로 단순 교체하면 필드 접근이 모두 실패한다. |
| P1 | 오류·로딩 상태 부족 | story, growth, curriculum 화면은 API 실패를 사용자에게 설명하거나 재시도하는 공통 상태가 부족하다. 일부는 빈 화면 또는 `PREPARING`으로 오인한다. |
| P1 | 숫자 ID와 slug 혼용 | backend `Long`과 프론트 문자열 alias를 URL 하나에 혼용하면 잘못된 resource 접근과 400 응답이 발생한다. |
| P1 | 캐시 기준 원본 충돌 | 진행률, 성장 단계, 캐릭터 해금, story page가 localStorage에 남아 다른 아동 계정으로 전환해도 섞일 수 있다. 일부 key가 student-scoped가 아니다. |
| P1 | CORS 배포 설정 | backend CORS origin은 localhost의 5173/4173만 허용한다. 실제 배포 origin에서는 credential 요청이 차단된다. |
| P1 | 상태 복구 | 훈련 session이 모듈 singleton 메모리에만 있어 새로고침, 탭 종료, 네트워크 재시도 시 서버 상태와 어긋난다. |
| P2 | 대형 정적 자산 | 아동 화면 이미지와 폰트가 크며 초기/기능별 전송량이 높다. 저사양 아동용 장치에서 로딩 지연과 메모리 압박 가능성이 있다. |
| P2 | 날짜·시간대 | backend `LocalDateTime`과 프론트 ISO offset 문자열 가정이 다르다. 정렬과 오늘 학습 판정 기준 시간대를 Asia/Seoul로 명시해야 한다. |

## 권장 통합 구조

```text
Learner views
  -> learner repositories (auth / curriculum / training / story / growth / gaze)
    -> DTO mapper + runtime validator
      -> learning ApiClient
        -> Spring /api/auth/app/**, /api/app/**

Teacher views
  -> existing teacher repositories
    -> existing admin ApiClient/session

Local eye tracker
  -> learner-only gaze bridge
    -> gaze session repository
      -> Spring /api/app/gaze/**
```

교수자 `frontend-web`과 아동 `frontend-app`은 별도 서브모듈로 유지한다. 아동 앱 안에서도 화면 컴포넌트가 DTO를 직접 사용하지 않고 repository가 현재 UI 모델로 변환하도록 하면 목업과 API 전환이 가능하다.

## 권장 작업 순서

1. **인증 경계 확정**: `/learner/login` 흐름, learning token store, app refresh/logout, learner route guard를 구현한다.
2. **현재 커리큘럼 계약 확정**: 학습 앱용 endpoint와 훈련 목록·상태·식별자 매핑을 추가한다.
3. **계약 타입 고정**: OpenAPI로 auth, curriculum, training question union, story shelf/line, growth DTO의 프론트 타입을 생성하거나 검증한다.
4. **읽기 API부터 연결**: 학생 프로필 → current curriculum → story shelf → growth → character 순으로 repository를 교체한다.
5. **훈련 mutation 연결**: start → question → response/recording → complete → resume/reset 순서를 상태 머신으로 구현한다.
6. **이야기 mutation 연결**: session → resume/lines → speech/branch/TTS → completion을 서버 기준으로 전환한다.
7. **시선 lifecycle 연결**: learner route에서만 로컬 bridge를 시작하고 backend session과 원시/요약 데이터 계약을 맞춘다.
8. **복구·중복·계정 전환 검증**: 새로고침, 토큰 만료, 네트워크 단절, 중복 클릭, 아동 전환, 장치 단절 시나리오를 통합 테스트한다.

## 통합 시작 전 완료 조건

- [x] 아동 전용 access token 발급·refresh·logout 호출 경계가 교수자와 독립되어 있다.
- [x] `/learner/**`가 인증되지 않은 접근을 차단한다.
- [ ] 아동 권한으로 현재 커리큘럼과 실제 `trainingId`를 조회할 수 있다.
- [ ] 모든 훈련 activity의 backend question JSON schema와 UI mapper가 있다.
- [ ] story shelf에 UI 필수 필드가 있거나 추가 조회 전략이 확정됐다.
- [ ] 성장 단계 및 캐릭터 잠금/해금 계산의 기준 원본이 정해졌다.
- [ ] challenge가 test인지 독립 기능인지 결정됐다.
- [ ] local eye tracker와 backend gaze session의 데이터·오류·종료 규칙이 정해졌다.
- [ ] production CORS origin, cookie 속성, API base URL이 배포 환경에 맞게 설정됐다.
- [x] 주요 API repository DTO/요청 contract 단위 테스트가 준비됐다.
- [ ] 실제 Spring·DB·cookie·CORS·eye tracker를 함께 띄운 E2E가 준비됐다.

## 검증 결과와 한계

- 프론트 최종 검증: API 모드 production build, Vue type-check, lint, Vitest 60개 파일·377개 테스트가 통과했다.
- 브라우저 검증: mock 모드에서 교수자 bootstrap → 아동 선택 → `/learner` 홈 진입을 확인했고 console error가 없었다. 교수자 `/login`에는 아동용 전역 gaze cursor가 없었다.
- 백엔드 계약 근거: controller, DTO, security 설정과 `contracts/openapi/*.yaml`을 대조했다.
- 백엔드 테스트: 현재 로컬 기본 Java가 8이고 Gradle 9.5.1은 JVM 17 이상, 프로젝트 toolchain은 Java 21을 요구해 실행하지 못했다. 이는 코드 실패가 아니라 점검 환경 차단이다.
- 실제 HTTP, cookie, CORS, DB 데이터, 로컬 eye tracker를 함께 띄운 검증은 요청에 따라 수행하지 않았다.

## 기준 소스

- 프론트 데이터 경계: `services/frontend-app/src/services/learnerDataRepository.ts`
- 프론트 아동 라우트: `services/frontend-app/src/router/learnerRoutes.ts`
- 프론트 훈련 상태: `services/frontend-app/src/composables/useTrainingSession.ts`
- 프론트 로컬 시선 브리지: `services/frontend-app/src/composables/useTobiiGazeBridge.ts`
- 백엔드 보안 경계: `services/backend/src/main/java/com/iread/backend/security/SecurityConfig.java`
- 백엔드 인증: `services/backend/src/main/java/com/iread/backend/auth/controller/AuthController.java`
- 백엔드 훈련: `services/backend/src/main/java/com/iread/backend/training/app/controller/AppTrainingController.java`
- 백엔드 이야기: `services/backend/src/main/java/com/iread/backend/story/app/controller/StoryController.java`
- 백엔드 성장·캐릭터·시선: 각 `student/app`, `mypage/app`, `gaze/app` controller
- API 계약: `contracts/openapi/app-api.yaml`, `contracts/openapi/auth-api.yaml`
