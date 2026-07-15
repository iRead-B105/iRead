# 프로젝트 컨텍스트

- 상태: draft
- 최종 검토일: 2026-07-15
- 서비스명: `iRead`

## 저장소 목적

서비스 기획부터 구현 준비까지의 공통 컨텍스트를 관리하고, 독립적인 Backend·Frontend·AI server 저장소를 조율한다.

## 확정 사항

- 서비스명과 오케스트레이션 저장소명은 `iRead`다.
- 현재 디렉터리는 오케스트레이션 저장소로 사용한다.
- Backend, Frontend, AI server는 각각 별도 저장소로 만들고 Git submodule로 연결할 예정이다.
- 현재 단계는 하네스와 기획 문서 구조만 구성한다.
- 기술 기준선은 [ADR-0002](../decisions/ADR-0002-technology-baseline.md)에 기록되어 있다.
- GitHub `iRead-B105/iRead` 저장소에 `main`, `develop` 브랜치가 구성되어 있으며 기본 브랜치는 `develop`이다.
- 향후 Git 운영은 [Git Flow 및 커밋 정책](../workflows/git-flow.md)을 따른다.
- 요구사항이나 필수 정보가 모호하면 변경 작업 전에 사용자에게 질문한다.

## 현재 단계에서 하지 않는 일

- 서비스 실행 코드 생성
- Docker Compose 파일 생성
- 패키지 및 의존성 설치
- submodule 경로 또는 URL 확정
- 데이터베이스 선정

## 미결 사항

- [TBD] Backend, Frontend, AI server의 저장소명
- [TBD] 해결할 사용자 문제와 핵심 가치
- [TBD] 핵심 사용자 및 이해관계자
- [TBD] MVP 범위와 성공 지표
- [TBD] 각 서비스의 책임과 submodule 경로
- [TBD] Redis의 책임(캐시, 세션, 큐, pub/sub 등)
- [TBD] 주 데이터베이스와 데이터 소유권
- [TBD] 인증·인가 및 개인정보 처리 요구사항
- [TBD] 배포 환경과 운영 제약
- [BLOCKED] 현재 GitHub 플랜에서는 비공개 저장소의 브랜치 보호 규칙을 사용할 수 없음

## 갱신 원칙

사용자가 미결 사항을 확정하면 이 문서, 관련 제품/아키텍처 문서와 ADR을 함께 갱신한다.
