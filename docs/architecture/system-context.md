---
type: System Context
title: "시스템 컨텍스트"
description: "iRead의 사용자, 서비스, 외부 경계와 오케스트레이션 관계를 설명합니다."
tags: [architecture, system-context, services]
timestamp: 2026-07-24T00:00:00+09:00
---
# 시스템 컨텍스트

- 상태: accepted
- 최종 검토일: 2026-08-14

외부 데모는 [ADR-0017](../decisions/ADR-0017-single-ec2-demo-architecture.md)에 따라 아동 PC의 로컬 시선 처리 경계와 AWS Single EC2의 서버 경계를 분리한다.

![iRead 시스템 아키텍처](../assets/readme/architecture/system-architecture.png)

## 확정 경계

- 교수자는 브라우저에서 HTTPS로 교수자 Frontend를 사용한다.
- 아동은 Windows PC의 Electron 앱을 사용하며 Tobii 장치 제어, 보정과 시선 프레임 처리는 로컬 서비스와 Electron IPC 경계에서 수행한다.
- AWS Single EC2에서 Nginx, Spring Boot Backend, FastAPI AI server, MySQL, Redis와 파일 저장소를 운영한다.
- Nginx는 TLS 종료, 정적 파일 제공과 Backend API proxy를 담당한다.
- Backend는 인증과 서비스 로직, 시선 세션·분석 결과·원시 파일 저장과 SSE 이벤트 발행을 조율한다.
- AI server는 Azure Speech 발음 평가와 독립된 이야기 텍스트·이미지 공급자 호출을 담당한다.

## 시선 데이터 흐름

![iRead 시선 데이터 흐름 요약](../assets/readme/architecture/gaze-data-flow-overview.png)

상세 처리 단계는 [시선 데이터 상세 흐름도](../assets/readme/architecture/gaze-data-flow-detail.png)에서 확인한다.

## 미결 경계

- Redis에 저장할 구체적인 데이터와 장애 시 fallback
- 운영 전환 시 고가용성, 백업·복구와 관측성
- 원시 시선·음성 파일의 운영 보관 주기와 삭제 보장
