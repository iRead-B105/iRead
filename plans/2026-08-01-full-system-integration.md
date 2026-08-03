---
type: Execution Plan
---
# Full learning-system integration

- Status: completed
- Updated: 2026-08-02

## Scope

Connect Frontend App, Backend, AI, Eye Tracker, and Teacher Frontend into one
learning flow. The verified paths cover authentication, curriculum and question
loading, submission and completion, speech upload, gaze collection, growth
aggregation, story reading, teacher queries, and realtime invalidation.

## Completed work

- [x] Use root `compose.yml` as the containerized runtime and keep the Windows
  Eye Tracker bridge as the only host-side service.
- [x] Run Backend with the `demo` profile and route it to the real AI service
  container instead of the old AI-mock container.
- [x] Disable frontend device submission mocks and persist gaze analysis once,
  from Frontend App to Backend.
- [x] Make demo AI mock flags configurable and fix the training-data uniqueness
  migration needed for stable Backend startup.
- [x] Fix story multipart `lineId` binding and preserve UTF-8 Korean text across
  Backend-to-AI multipart calls.
- [x] Remove the false-positive local speech path that copied `expectedText`
  into STT output and awarded pronunciation points from upload byte length.
- [x] Add a real Azure Speech provider path for Korean STT and configurable TTS.
- [x] Verify training completion, growth aggregation, teacher training logs, gaze
  analysis queries, story STT/TTS contracts, and teacher SSE delivery.

## Verification

- `docker compose config --quiet`
- All seven Compose services running; MySQL, Redis, Mailpit, and AI healthy.
- Learner and teacher frontend production builds passed.
- Learner frontend suite passed: 32 files, 186 tests.
- Backend full test suite passed against an isolated H2 test runtime.
- AI suite passed: 14 tests. Azure STT was also exercised with real silent
  audio and correctly returned an empty transcript with zero confidence.
- Every mutable `/api/v1/**` AI endpoint now enforces the shared Backend
  `X-API-Key`; a direct no-key TTS request returned 401 while the same request
  through the authenticated Backend path returned valid audio.
- Contract validation passed: 89 API operations, 334 features, 26 MySQL
  tables, and 35 foreign keys. Harness validation also passed.
- Realtime verification passed: teacher-to-learner 33 ms and
  learner-to-teacher 41 ms, including temporary-data cleanup.
- Live API flow passed: learner login, question response, training completion,
  growth count update, teacher log query, SSE event, story speech, training TTS,
  gaze session/end/analysis, and teacher gaze query.
- Real Korean Azure TTS passed through both Backend paths: training prompt
  returned 12,960 MP3 bytes (3,137 ms), and story line synthesis plus its
  authenticated audio download returned 26,208 MP3 bytes (6,450 ms).
- Eye Tracker native bridge is configured and running; websocket delivery was
  verified. Valid gaze points still require a calibrated user in front of the
  physical device.

## Completion notes

- [x] Verify Korean TTS with Unicode-preserving requests. Earlier zero-byte
  diagnostics were caused by the PowerShell diagnostic pipe converting Korean
  text to question marks; normal UTF-8 API requests return valid audio.
- [x] Make the full Backend test suite green after merged demo/test changes.
- [x] Re-run contract, realtime, Docker, frontend, and live API verification.
- [TBD] The Codex in-app browser runtime could not initialize, so this run did
  not add a new automated screenshot. This is non-blocking for service
  integration because authenticated live API flows, frontend component suites,
  production builds, and the user's earlier manual screen checks cover the
  running clients.
