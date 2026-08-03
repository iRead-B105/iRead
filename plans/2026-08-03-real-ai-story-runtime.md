---
type: Execution Plan
---
# 실제 AI 이야기·분기·이미지 런타임 전환

- 상태: in-progress
- 작성일: 2026-08-03
- 수정일: 2026-08-04

## 목표

아동 App의 이야기 시작과 반복 분기 선택이 Backend를 거쳐 GMS 텍스트 모델을 실제로 호출하고, 장면·캐릭터 이미지는 Gemini로 생성한다. 100페이지 동안 기승전결과 아동 선택의 인과관계를 유지하고 마지막 페이지에서 결말을 완성한다. 담당 교사는 생성 결과를 조회하고 아직 읽지 않은 소제목·본문·선택지·이미지를 수정할 수 있다. 테스트용 mock은 유지하되 실 AI 실행 모드에서는 고정 선택지나 1×1 PNG를 정상 결과로 반환하지 않으며, 실제 공급자 호출 여부를 종단 검증으로 증명한다.

## 기준선과 결론

이 계획은 2026-08-03에 fetch한 각 저장소의 `origin/develop`을 기준으로 한다. 로컬 브랜치와 submodule 포인터의 최신화는 계획 실행 첫 단계에서 별도로 수행한다.

| 항목 | 원격 `develop` 기준 상태 | 조치 |
| --- | --- | --- |
| 이야기·분기 호출 | Backend가 `/api/v1/story/generate`, `/api/v1/story/continue`와 전체 이력·`branchIntent`를 전송 | 계약을 유지하고 실 provider 실행 모드를 추가한다. |
| Backend 생성 모드 | 루트 `compose.yml`의 `AI_MOCK_GENERATE=true`가 이야기·이미지·훈련 생성을 함께 mock으로 전환 | 이야기·이미지 토글을 분리하고 실 AI 프로필에서 명시적으로 끈다. |
| AI 텍스트 provider | `STORY_PROVIDER=mock`이 기본이며 `gms`, `openai` 구현이 존재 | GMS를 데모 실연동 기준으로 사용하고 시작 시 설정을 검증한다. |
| 분기 선택지 | mock 경로에서는 고정된 선택지 3개를 반환 | 실 모드에서 GMS 응답의 서로 다른 선택지 3개만 허용한다. |
| 이야기 품질 | 진행률과 선택 이력은 전달하지만 100페이지 서사 계획·품질 수용 기준이 계약에 없음 | 이야기 설계와 누적 요약을 저장하고 기승전결 단계·인과관계·결말 회수를 검증한다. |
| 이어서 읽기 제목 | App이 배열 순서로 `1번`~`6번`과 템플릿 제목을 조합 | AI가 각 분기에 반환한 `branchPrompt.subtitle` 중 가장 최근 값을 표시한다. |
| 교사 접근 | 담당 아동의 이야기·분기·이미지·시선 기록은 조회 가능하지만 수정 API가 없음 | 아직 읽지 않은 생성 결과의 소제목·본문·선택지·이미지만 revision 기반으로 수정한다. |
| Backend 이미지 호출 | `/api/v1/images/generate`를 호출한 뒤 같은 AI origin의 이미지를 내려받아 Backend 저장소에 보관 | 호환 계약을 유지하면서 AI endpoint를 Gemini-backed 구현으로 승격한다. |
| AI 이미지 provider | `/api/v1/images/generate`는 항상 1×1 mock PNG이고 Gemini는 `/api/v1/story/images/generate`에만 연결 | `STORY_IMAGE_PROVIDER=gemini`일 때 호환 endpoint도 실제 이미지를 생성하도록 연결한다. |
| 검증 | fake/mock provider 중심이며 실제 공급자 smoke 결과가 자동 완료 조건에 포함되지 않음 | opt-in 실호출 smoke와 Backend–AI–App 종단 검증을 추가한다. |

## 확정 결정

| 대상 | 결정 |
| --- | --- |
| 텍스트 provider | 기존 결정대로 GMS OpenAI 호환 API와 `gpt-5.4-mini`를 사용한다. 직접 OpenAI 연결은 대체 설정으로만 유지한다. |
| 이미지 provider | 기존 Gemini adapter와 `gemini-2.5-flash-image`를 사용한다. |
| 호출 경계 | Frontend App은 AI를 직접 호출하지 않고 Backend만 `X-API-Key`로 AI server를 호출한다. |
| 페이지 분량 | 페이지당 정확히 3문장, 문장당 공백·숫자·문장부호를 제외한 한글 10~22음절로 생성·검증하고 13~19음절을 권장한다. |
| 문체와 대사 | 서술자는 일관된 해요체 높임 단계를 유지하되 종결어미를 자연스럽게 바꾼다. 직접 대사는 페이지당 0~1문장이고 위치를 고정하지 않으며, 연속된 두 페이지에는 가능하면 한 번 이상 둔다. |
| 서사 진행 | 100페이지를 `기(1~25) → 승(26~50) → 전(51~75) → 결(76~100)`로 관리한다. 100페이지 이전에는 핵심 갈등을 닫지 않고 100번째 페이지에서 누적 선택과 복선을 회수한 결말을 낸다. |
| 분기 입력 | 버튼은 AI 선택지 3개 중 하나를 확정한다. 음성은 선택지 밖의 자유 입력을 허용하며 STT 확인과 안전성·길이 검증 후 `branchIntent`로 확정한다. |
| 분기 소제목 | AI가 각 `branchPrompt`에 짧은 `subtitle`을 반환하고 Backend가 함께 저장한다. 이어서 읽기에는 가장 최근 분기 소제목을 사용하며 첫 분기 전에는 템플릿 제목을 사용한다. |
| 교사 수정 | 담당 교사는 아직 읽지 않은 생성 페이지의 소제목·본문·선택지 3개·이미지만 수정한다. 읽은 페이지, 아동의 확정 선택과 진행률은 불변이다. |
| 교사 이미지 수정 | 검증된 이미지 직접 업로드와 Gemini 재생성을 모두 제공한다. 임의 외부 URL 입력은 허용하지 않는다. |
| 이미지 통합 | 현재 Backend DTO와 파일 저장 흐름을 깨지 않도록 `/api/v1/images/generate` 응답의 `requestId`, `imageUrl`, `provider` 계약을 유지한다. AI server가 생성 이미지를 제한된 수명으로 제공하고 Backend가 즉시 내려받아 영속화한다. 구조화된 `/api/v1/story/images/generate`는 고급 장면·캐릭터 일관성용 후속 경로로 유지한다. |
| 실행 모드 | 기본 자동 테스트는 mock을 유지한다. 실제 연동은 별도 Compose override 또는 명시적 환경 집합으로만 켜며 필요한 키가 없으면 시작 단계에서 실패한다. |
| 실패 정책 | 실 텍스트 모드에서 provider 실패를 고정 mock 이야기로 숨기지 않는다. 오류를 반환하고 DB 변경을 롤백한다. 이미지 실패는 이야기 읽기를 막지 않고 `null` 이미지와 App의 정적 fallback을 사용한다. |
| 데이터 | 실호출 smoke에는 합성 아동·이야기 데이터만 사용한다. 실제 아동 데이터의 외부 provider 전송은 별도 개인정보·동의 결정 전까지 금지한다. |
| 비용 통제 | 자동 테스트는 외부 호출을 하지 않는다. 수동/보호된 CI smoke는 provider별 시나리오당 최대 1회 호출하고 명시적 opt-in과 실행 주체를 요구한다. |

## 범위

### 포함

- Orchestration의 실 AI 실행 설정, 비밀값 템플릿과 readiness 확인
- Backend의 이야기·이미지 mock 토글 분리와 AI 오류/트랜잭션 처리
- AI server의 GMS 이야기 생성과 Gemini 이미지 호환 endpoint 연결
- 이야기 시작, 버튼 분기, 음성으로 확정된 `branchIntent`, 다음 장면과 이미지 저장 검증
- 100페이지 서사 설계·누적 요약, 진행률별 기승전결과 결말 완성 검증
- 교사 이야기 조회·수정 API와 교사 Web 편집 UI, 수정본의 후속 AI 맥락 반영
- 가장 최근 AI 분기 소제목을 이어서 읽기 제목으로 제공하는 Backend–App 계약
- OpenAPI 계약, 서비스 테스트, 제한된 실 provider smoke와 종단 검증
- 관측 가능한 provider·request ID 기록과 비밀값·아동 입력 로그 차단

### 제외

- 훈련 후보 생성, 발음평가, STT·TTS provider 전환 자체의 재구현
- `/api/v1/story/images/generate`의 visual scene·캐릭터 레퍼런스를 Backend 도메인에 전면 도입하는 작업
- 운영용 객체 스토리지, 다중 AI 인스턴스 공유 캐시와 장기 이미지 CDN
- 실제 아동 데이터로 수행하는 품질 평가, 반복 유료 벤치마크와 모델 파인튜닝

## 작업

### 1. 기준선과 작업 브랜치

- [ ] 루트와 5개 submodule의 작업 트리가 깨끗한지 확인하고 각 로컬 `develop`을 `origin/develop`으로 `--ff-only` 최신화한다.
- [ ] 최신 서비스 커밋으로 루트 submodule 포인터를 맞춘 뒤 변경 전 기준 SHA를 기록한다.
- [ ] 코드 변경이므로 AI server, Backend와 Orchestration에 각각 최신 `develop` 기반 `feature/real-ai-story-runtime` 작업 브랜치를 만든다.
- [ ] `compose.yml`, AI 설정, Backend `AiClientProperties`, OpenAPI와 기존 테스트의 실제 최신 상태를 다시 대조한다.

### 2. 실행 설정과 모드 분리

- [ ] Backend에 이야기와 이미지 전용 설정(`AI_MOCK_STORY`, `AI_MOCK_IMAGE`)을 추가하고 기존 `AI_MOCK_GENERATE`는 훈련 생성 호환 설정으로 한정한다. 이전 환경변수만 있는 실행의 호환 규칙을 문서화하고 테스트한다.
- [ ] 실 AI용 Compose override에서 `AI_MOCK_STORY=false`, `AI_MOCK_IMAGE=false`, `STORY_PROVIDER=gms`, `STORY_IMAGE_PROVIDER=gemini`를 한 번에 설정한다.
- [ ] `GMS_KEY`, Backend `AI_API_KEY`와 AI `AI_INTERNAL_API_KEY`를 환경으로만 주입하고 예제에는 placeholder만 둔다. 저장소·이미지·로그에 실제 키를 남기지 않는다.
- [ ] 실 AI 모드에서 GMS 키, 모델, base URL 또는 이미지 provider 설정이 빠지면 health/readiness 단계에서 실패하도록 한다.
- [ ] AI `/health`가 `storyProvider=gms`, `storyImageProvider=gemini`를 보고하고 Backend가 해당 상태를 시작 전 또는 smoke 사전 조건으로 확인하게 한다.

### 3. GMS 이야기·분기 실연동 고정

- [ ] Backend가 `AI_MOCK_STORY=false`일 때만 `/story/generate`, `/story/continue`를 호출하고 `MockStoryGenerator`로 우회하지 않는 단위 테스트를 추가한다.
- [ ] 최초 생성 시 이야기 목표, 핵심 갈등, 등장인물, 결말 방향과 진행률별 주요 사건을 포함한 `narrativeState`를 만들고 Backend가 이야기별로 저장한다.
- [ ] 이어쓰기마다 누적 요약, 최근 원문, 교사 수정본, 현재 기승전결 단계와 확정된 `branchIntent`를 GMS 요청에 포함하고 갱신된 요약을 응답으로 받는다.
- [x] 현재 프롬프트의 페이지 묶음을 정확히 3문장으로 바꾸고 각 문장을 한글 10~22음절(권장 13~19음절)로 제한했다. 서버 validator는 공백·숫자·문장부호를 제외하고 한글 완성형 음절만 센다.
- [x] 길이 위반 문장을 자르거나 범용 문구로 채우는 후처리를 제거하고 재생성 또는 의미 보존 교정으로 처리한다. 해요체 종결과 대사 위치도 장면 흐름 안에서 변주하도록 완화했다.
- [ ] 생성 응답에서 페이지당 문장 수, 음절 수, `nextProgress`, `completed`, 분기 질문·소제목과 서로 다른 선택지 3개를 검증한다. 스키마 불일치나 고정 fallback 응답은 provider 성공으로 저장하지 않는다.
- [ ] AI의 legacy story adapter가 제목·서사 상태·최근 이력·현재 진행률·확정된 `branchIntent`를 GMS 요청에 포함하는지 contract test로 고정한다.
- [ ] 선택한 `branchIntent`가 다음 장면의 사건 또는 결과에 반영되는지 합성 fixture 기반 의미 검증을 추가한다. 정확한 문구 일치가 아니라 응답 내 선택 의도·핵심어 반영을 검사한다.
- [ ] 자유 음성 `branchIntent`는 STT 확인 후 길이, 개인정보성 표현, 폭력·성적·혐오·자해·위험 행동을 검사한다. 거절 시 같은 분기의 AI 선택지 3개를 유지하고 재입력 또는 버튼 선택을 안내한다.
- [ ] 선택지 3개가 짧고 구체적인 단일 행동인지, 의미가 서로 겹치지 않는지, 정답을 암시하지 않는지, 현재 장면에서 실행 가능한지 검증한다.
- [ ] 진행률 `1~25`는 인물·목표·세계 소개, `26~50`은 시도와 갈등 확대, `51~75`는 전환·위기와 선택의 결과, `76~99`는 해결과 복선 회수, `100`은 명확한 결말만 허용한다.
- [ ] 100페이지 장기 품질 회귀 fixture에서 인물·장소·핵심 목표의 모순, 선택 무시, 사건 반복, 조기 결말과 미회수 핵심 갈등을 탐지한다.
- [ ] timeout, 429, 5xx와 잘못된 JSON에서 동일 멱등키 1회 재시도 규칙과 Backend DB 무변경을 검증한다.

### 4. 분기 소제목과 이야기 상태 계약

- [ ] 루트 `ai-api.yaml`의 `StoryBranchPrompt`에 필수 `subtitle`을 추가하고 `StoryGenerateRequest/Response`에 versioned `narrativeState`를 정의한다.
- [ ] Backend가 소제목을 기존 `story_lines.branch_prompt` JSON에 선택지와 함께 저장하고, AI 서사 상태·누적 요약은 `stories`의 별도 JSON 컬럼에 저장하는 migration을 작성한다.
- [ ] App 이야기 책장 응답에 `latestBranchSubtitle`을 추가한다. Backend는 가장 최근 생성된 분기 소제목을 반환하고 없으면 템플릿 제목으로 대체한다.
- [ ] Frontend App의 이어서 읽기 카드에서 배열 순서 기반 `1번`~`6번` 제목을 제거하고 `latestBranchSubtitle`을 표시한다.
- [ ] 소제목 길이·금칙어·중복을 검증하고 같은 이야기의 연속 분기가 동일 소제목을 반환하면 재생성 또는 명시적 오류로 처리한다.

### 5. 교사 조회와 수정

- [ ] Admin 이야기 상세 응답에 revision, 분기 소제목, 선택지 3개와 편집 가능 여부를 추가한다. 기존 담당 교사 소유권 검사를 모든 수정 경로에도 적용한다.
- [ ] 아직 읽지 않은 생성 페이지를 수정하는 Admin PUT 계약을 `admin-api.yaml`의 기준 원본에 먼저 추가한다. 입력은 `revision`, 소제목, 정확히 3문장의 본문, 선택지 3개와 이미지 변경 지시만 허용한다.
- [ ] 이미 읽은 페이지, 선택이 확정된 분기와 완료 이야기는 `409`, 음절·선택지·안전 규칙 위반은 `422`, 다른 교사의 아동은 기존 보안 정책에 맞게 거부한다.
- [ ] 수정은 revision 기반 낙관적 잠금으로 저장하고 교사 ID, 수정 시각, 대상 필드와 변경 전후 revision을 감사 이력에 남긴다. 원문 전체를 일반 애플리케이션 로그에 남기지 않는다.
- [ ] 교사 이미지 수정은 검증된 직접 업로드와 Gemini 재생성을 모두 제공하고 임의 외부 URL은 받지 않는다. 업로드 파일의 MIME·크기·magic bytes를 검증하며, 재생성은 현재 수정본의 소제목·본문과 이야기 맥락을 prompt로 사용한다.
- [ ] 업로드와 재생성 결과는 동일한 이미지 revision 계약으로 저장한다. 새 이미지 저장이 성공한 뒤 참조를 교체하고 실패하면 기존 이미지를 유지한다.
- [ ] 교사가 수정한 본문·소제목·선택지는 아동의 다음 조회에 즉시 반영하고 이후 AI 요청의 확정 맥락으로 사용한다. 이미 읽은 이력과 확정 선택은 재생성하거나 덮어쓰지 않는다.
- [ ] 교사 Web에 읽지 않은 페이지만 편집 가능한 UI, 저장 충돌·검증 오류 안내, 이미지 교체/재생성 상태와 저장 후 재조회 흐름을 구현한다.

### 6. Gemini 이미지 호환 endpoint 연결

- [ ] AI `/api/v1/images/generate`가 `STORY_IMAGE_PROVIDER=disabled`이면 기존 결정적 mock을, `gemini`이면 실제 Gemini adapter를 호출하도록 provider를 주입한다.
- [x] `[STORY_SCENE]`, `[STORY_CHARACTER]`를 구분하고 사용자 입력을 명령으로 재해석하지 않는 이미지 정책 프롬프트를 실제 호환 endpoint에 적용했다. 한 순간·한 핵심 행동과 관련 배경 단서를 우선하고 불필요한 인물·사물은 금지한다.
- [ ] 생성된 PNG/JPEG/WebP를 크기·MIME·magic bytes·최대 용량으로 검증하고, 예측 불가능한 image ID의 제한 수명 저장소에서 같은 AI origin URL로 제공한다.
- [ ] 이미지 URL은 1회 Backend 저장에 필요한 시간 동안만 유지하고 TTL, 최대 항목 수와 메모리 상한을 둔다. 프로세스 재시작 시 소실 가능함을 데모 제약으로 문서화한다.
- [ ] Backend는 기존 same-origin 검증 후 이미지를 내려받아 현재 업로드 저장소에 영속화한다. 1×1 mock, 빈 본문, 비허용 MIME, 과대 응답은 실제 이미지 성공으로 처리하지 않는다.
- [ ] 장면 이미지 실패는 `null`로 저장해 App fallback을 사용하고, 완료 보상용 캐릭터 이미지 실패 정책은 이야기 완료를 되돌리지 않도록 장면 정책과 일치시킨다.
- [ ] 향후 구조화된 `/story/images/generate` 전환 조건을 별도 후속 항목으로 남긴다: 페이지별 visual scene 계약, 캐릭터 ID/레퍼런스 소유권과 영속 이미지 저장소가 확정될 때 전환한다.

### 7. 계약과 관측성

- [ ] `contracts/openapi/ai-api.yaml`에서 분리된 실행 설정이 아닌 HTTP 계약 변경분만 먼저 반영한다. 이미지 조회 endpoint, 허용 MIME, 크기 제한, 오류와 멱등·재시도 정책을 명시한다.
- [ ] AI와 Backend 로그에는 request ID, endpoint, provider, 모델, latency, 결과 코드와 retry 여부만 남긴다. prompt, 이야기 이력, 음성 전사, 키와 provider 원문 응답은 기록하지 않는다.
- [ ] mock 응답과 실 provider 응답을 운영자가 구분할 수 있도록 health와 구조화 로그에 provider를 노출하되 아동 App API에는 내부 자격증명이나 원문 오류를 노출하지 않는다.
- [ ] provider별 timeout과 응답 크기 제한을 환경 설정으로 고정하고 Backend HTTP timeout이 AI timeout보다 짧아지지 않도록 검증한다.

### 8. 검증과 단계적 활성화

- [ ] AI unit/contract/integration 전체 테스트에서 mock, GMS fake, Gemini fake, provider 오류와 이미지 TTL 저장소를 검증한다.
- [ ] Backend `HttpAiClientTest`, `StoryServiceTest`와 관련 통합 테스트에서 실 모드 호출, 멱등성, 저장 트랜잭션과 이미지 다운로드를 검증한다.
- [ ] Frontend App의 기존 API 테스트와 story reader 테스트로 실제 URL, 이미지 없음 fallback, 분기 선택 후 새 장면 로드를 검증한다.
- [ ] 교사 Web의 이야기 조회·편집, revision 충돌, 읽은 페이지 편집 차단과 수정본 재조회 테스트를 실행한다.
- [ ] 로컬 종단 테스트에서 시작 이야기의 선택지 3개가 고정 mock 문구가 아니고, 버튼·자유 음성 선택이 다음 장면에 반영되며, 최신 소제목이 이어서 읽기에 표시되고, 저장 이미지가 1×1이 아니고 새로고침 후에도 표시되는지 확인한다.
- [ ] 100페이지 반복 생성 시나리오에서 진행률이 생성 페이지 수와 일치하고 99%까지 진행 중, 100%에서만 결말·`COMPLETED`가 되는지 검증한다.
- [ ] 중간의 읽지 않은 페이지를 교사가 수정한 뒤 아동 표시와 다음 AI 이어쓰기가 수정본을 기준으로 하는지 종단 검증한다.
- [ ] 합성 데이터와 명시적 opt-in으로 GMS 이야기 1회, 이어쓰기 1회, Gemini 이미지 1회 smoke를 실행한다. request ID, provider, 상태, latency, 이미지 규격과 비용 확인용 호출 수만 증적으로 남긴다.
- [ ] mock 기본 프로필과 실 AI 프로필을 각각 새 환경에서 기동해 서로 설정이 섞이지 않는지 확인한 뒤 Orchestration submodule 포인터 PR을 병합한다.

## 검증 명령과 수용 기준

- Orchestration: `python tools/validate_contracts.py`, `python tools/validate_harness.py`, `docker compose config`
- AI server: `uv run pytest`, `uv run ruff check .`
- Backend: 관련 Gradle 테스트 후 전체 `test`
- Frontend App: 관련 Vitest, 타입 검사와 production build
- 공통: `git diff --check`, 비밀값 패턴 검사, 컨테이너 health 확인

다음 조건을 모두 만족해야 완료한다.

- 실 AI 프로필의 health가 `storyProvider=gms`, `storyImageProvider=gemini`를 보고한다.
- 이야기 시작과 이어쓰기 요청이 `MockStoryGenerator`를 통과하지 않았다는 테스트와 request ID 상관관계가 있다.
- 버튼으로 고른 분기 문구가 다음 이야기 내용에 반영되고 서로 다른 AI 선택지 3개가 저장된다.
- AI 선택지 밖의 자유 음성 입력도 확인·안전성 검사를 거쳐 다음 이야기 사건에 반영된다.
- 모든 페이지가 정확히 3문장이고 각 문장은 한글 10~22음절이며, 대부분 13~19음절의 자연스러운 문장이다.
- 100페이지의 기승전결 단계가 순서대로 진행되고 100페이지에서 누적 선택을 회수한 결말과 `COMPLETED`가 함께 저장된다.
- 이어서 읽기 제목은 숫자가 아니라 AI가 반환한 가장 최근 분기 소제목이다.
- 담당 교사는 읽지 않은 생성 결과의 소제목·본문·선택지·이미지만 수정할 수 있고 수정본이 아동 조회와 이후 AI 생성에 반영된다.
- Backend에 저장된 장면 이미지의 공급자가 Gemini이며 허용 MIME이고 가로·세로가 모두 1픽셀보다 크다.
- 실 provider 장애 시 이야기 데이터가 부분 저장되지 않고, 이미지 장애만으로 읽기 진행이나 완료가 취소되지 않는다.
- 자동 테스트는 외부 비용을 발생시키지 않고 실호출 smoke는 정해진 최대 호출 수를 넘지 않는다.
- 저장소, 빌드 산출물과 로그에 키·prompt·아동 이야기 이력이 남지 않는다.

## 배포와 롤백

1. mock 프로필에서 전체 회귀검증을 통과시킨다.
2. 개발자 로컬의 합성 데이터로 실 AI 프로필 smoke를 수행한다.
3. 공유 데모 환경에서 이야기·이미지만 제한적으로 활성화하고 오류율, latency와 호출 수를 확인한다.
4. 문제가 있으면 `AI_MOCK_STORY=true`, `AI_MOCK_IMAGE=true`로 되돌린 뒤 AI/Backend를 재기동한다. 새 JSON·revision 컬럼은 하위 호환 nullable/additive migration으로 유지하고 신규 읽기·수정 경로만 비활성화한다. 이미 저장된 생성 결과와 교사 수정 이력은 삭제하지 않는다.

## 미결 사항

- [BLOCKED] 실제 아동의 이야기 이력이나 음성 전사를 GMS/Azure 등 외부 provider에 전송하려면 수집 항목, 법정대리인 동의, 보관 기간과 삭제 정책을 별도 승인해야 한다. 승인 전 실호출은 합성 데이터로 제한한다.
- [TBD] 운영 배포 전에 생성 이미지의 영속 저장소와 CDN, 보존·삭제 정책을 정한다. 현재 계획의 AI 메모리 저장소는 Backend가 즉시 내려받는 데모 전달용이다.
- [TBD] 품질 기준선을 위해 분기 반영률, 인과관계·복선 회수, 연령 적합성, 금칙어와 이미지 안전성 평가셋의 합격 임계치를 구현 전 확정한다.

## 진행 기록

- 2026-08-03: 루트와 AI·Backend·학습자 App·교사 Web을 최신 `develop` 기반 기능 브랜치로 정리하고, 이야기·이미지 실 provider 토글을 분리했다.
- 2026-08-03: GMS 최초 이야기와 자유 분기 이어쓰기, Gemini 이미지 생성을 합성 데이터로 실제 호출했다. 이어쓰기는 4개 읽기 페이지와 다음 분기 페이지를 반환했으며 모든 읽기 페이지가 3문장·문장당 한글 12~20음절을 충족했고 확정 분기가 첫 문장에 반영됐다.
- 2026-08-03: AI 분기 소제목, 학습자 음성 자유 입력 확인, 최신 소제목 표시, 교사의 읽기 전 페이지 본문·분기·이미지 수정과 revision·감사 이력을 구현했다.
- 2026-08-03: AI 25개 관련 테스트, 학습자 App 272개 테스트, 교사 Web 이야기 관련 41개 테스트와 타입·lint·production build, Backend 이야기 관련 42개 테스트, 계약·하네스·Compose 검증이 통과했다.
- 2026-08-04: 이야기 문장 범위를 10~22음절(권장 13~19)로 넓히고, 고정 해요체·고정 대사 위치·기계적 절단/채움 후처리를 제거했다. 분기 입력은 AI가 자연스러운 사건으로 통합하며, 실제 이미지 호환 경로에 단일 초점·불필요한 요소 금지 정책을 연결했다.
- 2026-08-04: 합성 자유 분기로 실제 GMS 이어쓰기를 재검증했다. 11.64초에 4페이지와 새 분기를 반환했고 모든 페이지가 정확히 3문장, 문장당 12~20음절이었으며 `노란 나뭇잎` 선택이 첫 장면의 행동과 후속 결과에 반영됐다. 실제 Gemini 호환 이미지도 1536×672 PNG로 생성됐고 단일 거북이·노란 잎·바람 언덕 구도를 확인했다.
- 2026-08-04: AI 전체 259개 테스트, Backend 교사 이야기 서비스 테스트, 교사 Web 타입 검사와 이야기 저장소 테스트, 계약·하네스 검증 및 Ruff가 통과했다. 로컬 실 provider 설정이 일부 테스트에 유입되던 문제는 각 테스트의 mock/disabled provider 명시로 격리했다.
- 2026-08-04: 분기 소제목을 첫 선택지에서 파생하지 않고 AI 장 응답의 독립 `subtitle` 필드로 생성·전달하도록 고쳤다. 실 GMS 응답에서 `노란 돛이 흔들릴 때`와 서로 다른 선택지 3개를 확인했고, 직전 질문 반복과 본문 속 독자 질문은 거절·재생성하도록 보강했다.
- [TBD] 실 provider로 100페이지 전체를 반복 생성하는 유료 장기 품질 평가는 아직 실행하지 않았다. 자동 mock 회귀에서는 100페이지에서만 완료되는 진행 규칙을 검증한다.
- [TBD] 전체 회귀에는 변경 범위 밖의 기존 실패가 남아 있다. Backend 훈련 완료 후 재계산 검증 1건과 교사 Web 시선분석 기대값 3건을 별도 정리해야 한다.
- [BLOCKED] 실제 아동 데이터로 외부 provider 종단 검증하는 작업은 개인정보·동의 결정 전까지 수행하지 않는다.
