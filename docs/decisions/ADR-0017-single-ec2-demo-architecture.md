---
type: Architecture Decision
title: "ADR-0017: AWS Single EC2 데모 아키텍처 채택"
description: "iRead 외부 데모의 실행 경계, 시선 처리 흐름과 외부 AI 연동 구조를 확정합니다."
tags: [architecture, deployment, aws, ec2, nginx, electron, eye-tracking, ai, adr]
timestamp: 2026-08-14T00:00:00+09:00
---
# ADR-0017: AWS Single EC2 데모 아키텍처 채택

- 상태: accepted
- 결정일: 2026-08-14
- 결정자: 사용자
- 보완 대상: [ADR-0002](ADR-0002-technology-baseline.md)의 클라우드·배포 플랫폼 미결 범위

## 배경

iRead 데모를 외부에서 실행하고 교수자 브라우저, 아동용 앱, 시선 추적 장치, Backend, AI server와 데이터 계층 사이의 책임을 일관되게 설명할 배포 기준선이 필요하다.

아동의 시선 추적은 Tobii 장치와 로컬 실행 환경에 의존하므로 학습자 PC에서 처리해야 한다. 서비스 API와 데이터 저장은 외부에서 접근 가능한 공통 서버 경계가 필요하며, 발음 평가와 이야기 생성은 공급자별 외부 AI 서비스를 사용한다.

## 결정

### 사용자와 로컬 실행 경계

- 교수자는 브라우저에서 HTTPS로 서비스에 접속한다.
- 아동은 Windows PC의 Electron 앱에서 훈련·검사·이야기 읽기를 진행한다.
- Tobii Eye Tracker의 장치 제어와 시선 프레임 처리는 아동 PC의 로컬 서비스와 Electron IPC 경계에서 수행한다.
- 아동 앱은 장치 상태를 확인하고 보정 또는 대체 입력을 결정한 뒤 시선 수집을 시작한다.
- 로컬 처리 모듈은 시선 프레임을 정규화하고 DOM 콘텐츠와 매칭해 단어·문장별 지표를 생성한다.

### 데모 서버 경계

- 외부 데모는 AWS의 Single EC2에 배포한다.
- Nginx가 TLS를 종료하고 정적 파일 제공과 Backend API proxy를 담당한다.
- Spring Boot Backend와 FastAPI AI server는 같은 EC2 경계에서 실행한다.
- MySQL, Redis와 파일 저장소도 데모 기준으로 같은 EC2 경계에서 운영한다.
- Backend가 세션 상태, 분석 결과와 원시 파일 저장을 조율하고 커밋 이후 SSE로 교수자 클라이언트에 갱신을 알린다.

### 외부 AI 경계

- 발음 평가는 [ADR-0013](ADR-0013-azure-speech-pronunciation-assessment.md)에 따라 Azure Speech를 사용한다.
- 이야기 텍스트와 이미지 생성은 [ADR-0016](ADR-0016-independent-story-ai-provider-routing.md)에 따라 독립된 외부 공급자로 라우팅한다.
- 외부 AI 자격증명은 AI server 경계에서 관리하고 클라이언트에 노출하지 않는다.

## 데이터 흐름

1. 아동 앱이 학습 콘텐츠와 토큰 메타데이터를 로드한다.
2. 로컬 처리 모듈이 장치 상태를 확인하고 시선 좌표를 보정한다.
3. Electron IPC를 통해 시선 수집을 제어하고 프레임을 정규화한다.
4. DOM 콘텐츠와 시선 좌표를 매칭해 단어·문장별 지표를 만든다.
5. Backend가 세션 메타데이터, 원시 좌표 파일과 분석 결과를 저장한다.
6. Backend가 SSE 이벤트를 발행하고 교수자 클라이언트가 분석 결과를 다시 조회한다.

## 영향

### 긍정적 영향

- 아동 PC의 하드웨어 의존 처리와 서버의 저장·분석 책임이 분리된다.
- 단일 EC2 배포로 데모 환경의 구성과 운영 복잡도를 제한한다.
- 교수자 조회, 원시 파일과 분석 DB 사이의 데이터 흐름을 하나의 기준으로 설명할 수 있다.

### 제약과 트레이드오프

- Single EC2는 단일 장애 지점이며 고가용성 구성이 아니다.
- MySQL, Redis, 파일과 애플리케이션 프로세스가 같은 인스턴스 자원을 공유한다.
- 학습자 PC마다 Electron 앱, Tobii SDK와 로컬 시선 처리 환경이 필요하다.
- 외부 AI 호출은 공급자 장애, 네트워크 지연과 비용에 영향을 받는다.

## 미결 운영 정책

- [TBD] 운영 전환 시 EC2 분리, 오토스케일링과 고가용성 구성
- [TBD] MySQL·Redis·원시 파일의 백업, 복구와 보관 주기
- [TBD] 운영 관측성, 경보와 장애 대응 기준
- [TBD] Redis의 구체적인 데이터와 장애 시 fallback

## 시각 자료

- [시스템 아키텍처](../assets/readme/architecture/system-architecture.png)
- [시선 데이터 흐름 요약](../assets/readme/architecture/gaze-data-flow-overview.png)
- [시선 데이터 상세 흐름도](../assets/readme/architecture/gaze-data-flow-detail.png)
