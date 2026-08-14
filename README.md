<div align="center">

<!-- iRead 로고: docs/assets/readme/overview/iread-logo.png -->

# iRead

### 아동의 읽기 특성을 이해하는 개인화 읽기 훈련 시스템

<!-- 대표 이미지 또는 핵심 기능 GIF: docs/assets/readme/overview/service-overview.* -->

**개발 기간** 2026.07.06 ~ 2026.08.10 (6주)<br />
**개발 인원** 6명<br />
**플랫폼** 교수자 Web · 아동 Windows Electron App

**[TBD] 서비스 시연 영상** · **[TBD] Notion API 명세** · **[TBD] 화면 설계서**

</div>

---

## 📑 목차

- [📌 서비스 소개](#service-introduction)
- [👥 팀원 소개 및 역할](#team)
- [✨ 주요 기능](#features)
- [🛠️ 기술 스택](#technology-stack)
- [🏗️ 시스템 아키텍처](#system-architecture)
- [🗄️ ERD](#erd)
- [📋 API 명세](#api-specification)
- [🔬 핵심 기술 상세](#technology-details)

---

<a id="service-introduction"></a>

## 📌 서비스 소개

iRead는 난독증 또는 읽기곤란 위험이 있는 초등 저학년 아동을 위한 개인화 읽기 훈련 시스템입니다.

아동이 자신의 읽기 특성과 변화 속도에 맞춰 꾸준히 훈련할 수 있도록 돕고, 보호자와 전문가는 훈련 과정과 변화를 함께 살펴볼 수 있도록 지원합니다.

### 기획 배경

[TBD] 기존 읽기 교육에서 발견한 문제와 iRead를 기획하게 된 배경을 작성합니다.

### 대상 사용자

| 사용자 | 제공 가치 |
| --- | --- |
| 아동 | 자신의 읽기 특성과 학습 속도에 맞는 훈련을 진행합니다. |
| 교수자·전문가 | 아동의 훈련 과정과 학습 변화를 확인합니다. |
| 보호자 | 아동의 학습 현황을 이해하고 적절한 지원을 이어갈 수 있도록 도움받습니다. |

### 핵심 가치

1. 시선과 발음 데이터를 활용해 아동의 읽기 수행을 다각도로 살펴봅니다.
2. 아동의 읽기 특성과 변화 속도에 맞는 훈련 경험을 제공합니다.
3. 아동과 교수자 사이의 학습 현황을 실시간으로 연결합니다.

<!-- 서비스 이용 흐름 이미지: docs/assets/readme/overview/service-flow.png -->

> iRead는 의료적 진단이나 전문가의 판단을 대체하지 않습니다. 아동의 안전과 존엄성, 개인정보 보호를 우선하며 전문가의 읽기 교육과 지원을 보조하는 도구를 지향합니다.

---

<a id="team"></a>

## 👥 팀원 소개 및 역할

<!-- 팀원 수에 맞게 셀을 추가하거나 삭제합니다. 프로필 이미지는 같은 크기와 비율로 준비합니다. -->

<table>
  <tr>
    <td align="center" width="33%">
      <!-- 프로필 이미지: docs/assets/readme/team/kim-min-jae.* -->
      <br />
      <strong>김민재</strong>
      <br />
      [TBD] 역할
      <br />
      [TBD] GitHub
    </td>
    <td align="center" width="33%">
      <!-- 프로필 이미지: docs/assets/readme/team/kim-ji-hun.* -->
      <br />
      <strong>김지훈</strong>
      <br />
      [TBD] 역할
      <br />
      [TBD] GitHub
    </td>
    <td align="center" width="33%">
      <!-- 프로필 이미지: docs/assets/readme/team/song-seung-woo.* -->
      <br />
      <strong>송승우</strong>
      <br />
      [TBD] 역할
      <br />
      [TBD] GitHub
    </td>
  </tr>
  <tr>
    <td align="center">
      [TBD] 담당 기능<br />
      [TBD] 주요 구현 내용
    </td>
    <td align="center">
      [TBD] 담당 기능<br />
      [TBD] 주요 구현 내용
    </td>
    <td align="center">
      [TBD] 담당 기능<br />
      [TBD] 주요 구현 내용
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <!-- 프로필 이미지: docs/assets/readme/team/yoon-jeong.* -->
      <br />
      <strong>윤정</strong>
      <br />
      팀장 · [TBD] 역할
      <br />
      [TBD] GitHub
    </td>
    <td align="center" width="33%">
      <!-- 프로필 이미지: docs/assets/readme/team/lee-seung-hwan.* -->
      <br />
      <strong>이승환</strong>
      <br />
      [TBD] 역할
      <br />
      [TBD] GitHub
    </td>
    <td align="center" width="33%">
      <!-- 프로필 이미지: docs/assets/readme/team/jeong-ui-chan.* -->
      <br />
      <strong>정의찬</strong>
      <br />
      [TBD] 역할
      <br />
      [TBD] GitHub
    </td>
  </tr>
  <tr>
    <td align="center">
      [TBD] 담당 기능<br />
      [TBD] 주요 구현 내용
    </td>
    <td align="center">
      [TBD] 담당 기능<br />
      [TBD] 주요 구현 내용
    </td>
    <td align="center">
      [TBD] 담당 기능<br />
      [TBD] 주요 구현 내용
    </td>
  </tr>
</table>

---

<a id="features"></a>

## ✨ 주요 기능

| 기능 | 설명 |
| --- | --- |
| 📚 개인화 읽기 훈련 | 아동의 읽기 특성과 학습 진행에 맞춰 읽기 훈련을 제공합니다. |
| 👁️ 시선 추적 | 읽기 과정에서 아동의 시선 위치와 움직임을 수집합니다. |
| 🗣️ 발음 평가 | 읽기 음성을 분석하여 단어별 발음 수행 결과를 제공합니다. |
| 📊 학습 현황 확인 | 교수자가 아동의 훈련 진행 상황과 변화를 확인할 수 있도록 지원합니다. |

### 1. 개인화 읽기 훈련

<table>
  <tr>
    <td width="55%" align="center">
      <!-- 기능 GIF: docs/assets/readme/features/personalized-training.gif -->
      기능 화면
    </td>
    <td width="45%">
      <strong>아동별 읽기 훈련</strong><br /><br />
      아동의 읽기 특성과 변화 속도에 맞춰 단계적으로 훈련할 수 있도록 돕습니다.<br /><br />
      <strong>핵심 가치</strong><br />
      · 아동별 수준을 반영한 훈련<br />
      · 단계별 학습 진행<br />
      · 훈련 결과의 지속적인 확인
    </td>
  </tr>
</table>

### 2. 시선 추적

<table>
  <tr>
    <td width="55%" align="center">
      <!-- 기능 GIF: docs/assets/readme/features/eye-tracking.gif -->
      기능 화면
    </td>
    <td width="45%">
      <strong>읽기 과정의 시선 데이터 수집</strong><br /><br />
      Tobii Eye Tracker를 이용해 아동이 글을 읽는 동안의 시선 데이터를 수집합니다.<br /><br />
      <strong>핵심 가치</strong><br />
      · 읽기 중 시선 위치 수집<br />
      · native bridge 기반 장치 연동<br />
      · 장치 미연결 시 마우스 기반 fallback
    </td>
  </tr>
</table>

### 3. 발음 평가

<table>
  <tr>
    <td width="55%" align="center">
      <!-- 기능 GIF: docs/assets/readme/features/pronunciation-assessment.gif -->
      기능 화면
    </td>
    <td width="45%">
      <strong>단어 단위 발음 수행 분석</strong><br /><br />
      Azure Speech의 한국어 발음 평가를 활용해 읽기 음성의 단어별 정확도를 분석합니다.<br /><br />
      <strong>핵심 가치</strong><br />
      · 실제 음성 기반 발음 평가<br />
      · 단어별 정확도와 오류 유형 확인<br />
      · 음성 원본을 분석 이후 보관하지 않는 정책
    </td>
  </tr>
</table>

### 4. 학습 현황 확인

<table>
  <tr>
    <td width="55%" align="center">
      <!-- 기능 GIF: docs/assets/readme/features/learning-dashboard.gif -->
      기능 화면
    </td>
    <td width="45%">
      <strong>아동과 교수자의 실시간 학습 연동</strong><br /><br />
      아동 앱의 훈련 진행 상황을 교수자 앱에 전달하여 학습 현황을 함께 확인할 수 있도록 지원합니다.<br /><br />
      <strong>핵심 가치</strong><br />
      · 아동별 훈련 상태 확인<br />
      · SSE 기반 실시간 상태 전달<br />
      · 교수자와 아동 사이의 학습 흐름 연결
    </td>
  </tr>
</table>

---

<a id="technology-stack"></a>

## 🛠️ 기술 스택

<!-- 최종 작성 시 기술명 대신 shields.io 배지를 사용할 수 있습니다. -->

| 분류 | 기술 | 선택 이유 |
| --- | --- | --- |
| Frontend Web | Vue 3, TypeScript, Vite, pnpm | [TBD] 기술 선택 이유를 작성합니다. |
| Frontend App | Vue 3, TypeScript, Vite, Electron | Tobii 장치와 로컬 시선 처리 모듈을 연동하고 Windows 앱으로 배포합니다. |
| Backend | Spring Boot 4.0.7, Java 21, Gradle | [TBD] 기술 선택 이유를 작성합니다. |
| AI server | FastAPI, Python 3.12, uv, Azure Speech | AI 기능을 별도 서비스 경계에서 제공하고 한국어 단어 단위 발음 평가를 수행합니다. |
| Database | MySQL 8.4 LTS | 관계형 학습 데이터를 일관되게 저장하고 migration 기반 스키마 이력을 관리합니다. |
| Infrastructure | AWS EC2, Nginx, Redis, Docker Compose | Single EC2 데모 경계에서 TLS, 정적 파일, API proxy와 서비스 실행 환경을 구성합니다. |
| Eye Tracking | FastAPI, JavaScript, C++, Tobii Game Integration SDK | 브라우저에서 직접 접근하기 어려운 시선 추적 장치를 로컬 bridge를 통해 연동합니다. |

기술 기준선과 선택 배경은 [ADR-0002](docs/decisions/ADR-0002-technology-baseline.md), [ADR-0006](docs/decisions/ADR-0006-mysql-primary-database.md), [ADR-0013](docs/decisions/ADR-0013-azure-speech-pronunciation-assessment.md)에서 확인할 수 있습니다.

---

<a id="system-architecture"></a>

## 🏗️ 시스템 아키텍처

![iRead 시스템 아키텍처](docs/assets/readme/architecture/system-architecture.png)

iRead 데모는 AWS Single EC2 안에서 Nginx, Spring Boot Backend, FastAPI AI server, MySQL, Redis와 파일 저장소를 함께 운영합니다. 교수자는 브라우저로 접속하고, 아동은 로컬 시선 추적 환경이 포함된 Electron 앱을 사용합니다. 발음 평가와 이야기 텍스트·이미지 생성은 AI server가 외부 AI 서비스와 연동합니다.

| 서비스 | 역할 | 주요 연결 |
| --- | --- | --- |
| Nginx | TLS 종료, 정적 파일 제공과 API proxy | 교수자 브라우저, 아동 앱, Backend |
| Frontend Web | 교수자용 사용자 인터페이스 | HTTPS, Backend API, SSE |
| Frontend App | Electron 기반 아동용 읽기 훈련 애플리케이션 | HTTPS, Electron IPC, Tobii 로컬 서비스 |
| Backend | 인증, 서비스 로직, 세션·분석 결과와 파일 관리 | MySQL, Redis, 파일 저장소, AI server |
| AI server | 발음 평가와 이야기 콘텐츠 생성 연동 | Backend–AI API, 외부 AI 서비스 |
| Eye Tracking | Tobii 시선 데이터 수집, 보정과 단어·문장별 지표 생성 | Frontend App, Electron IPC, Backend |
| MySQL·Redis·File | 영구 데이터, 캐시와 원시 파일 저장 | Backend |

<a id="gaze-data-flow"></a>

### 시선 데이터 흐름

아동 앱에서 시작한 학습 세션은 장치 확인과 좌표 보정을 거쳐 단어·문장별 시선 지표로 변환됩니다. Backend는 원시 파일과 분석 결과를 저장하고, 교수자 앱은 저장된 결과를 조회해 분석 화면과 보고서로 제공합니다.

![iRead 시선 데이터 흐름 요약](docs/assets/readme/architecture/gaze-data-flow-overview.png)

<details>
<summary><strong>시선 데이터 상세 흐름도 보기</strong></summary>

<br />

![iRead 시선 데이터 상세 흐름도](docs/assets/readme/architecture/gaze-data-flow-detail.png)

</details>

상세한 서비스 경계와 배포 기준은 [시스템 컨텍스트](docs/architecture/system-context.md)와 [ADR-0017](docs/decisions/ADR-0017-single-ec2-demo-architecture.md)에서 확인할 수 있습니다.

---

<a id="erd"></a>

## 🗄️ ERD

![iRead ERD](contracts/database/erd.png)

<details>
<summary><strong>주요 도메인 설명</strong></summary>

<br />

- **사용자·교수자:** [TBD] 주요 엔티티와 책임을 설명합니다.
- **아동:** [TBD] 주요 엔티티와 책임을 설명합니다.
- **교육과정:** [TBD] 주요 엔티티와 책임을 설명합니다.
- **훈련·검사:** [TBD] 주요 엔티티와 책임을 설명합니다.
- **학습 결과:** [TBD] 주요 엔티티와 책임을 설명합니다.

</details>

---

<a id="api-specification"></a>

## 📋 API 명세

<div align="center">

### [TBD] Notion API 명세 링크를 추가합니다

</div>

| API 영역 | 기준 명세 | 주요 기능 |
| --- | --- | --- |
| Authentication | [공통 인증 API](contracts/openapi/auth-api.yaml) | 로그인, 토큰 갱신, 비밀번호 재설정 |
| App | [App–Backend API](contracts/openapi/app-api.yaml) | 아동용 앱의 교육과정·훈련·검사 기능 |
| Admin | [Admin–Backend API](contracts/openapi/admin-api.yaml) | 교수자용 아동·교육과정·학습 현황 관리 |
| AI | [Backend–AI API](contracts/openapi/ai-api.yaml) | 발음 평가 등 AI 분석 요청 |
| Eye Tracking | [Eye Tracker 연동 초안](contracts/gaze/eyetracker-api-contract.md) | 시선 데이터 수집 및 전달 |

전체 계약 현황은 [계약 카탈로그](contracts/catalog.md)에서 확인할 수 있습니다.

---

<a id="technology-details"></a>

## 🔬 핵심 기술 상세

각 기술은 해결하려는 문제, 적용한 방법, 검증 결과를 중심으로 정리합니다.

### 1. 시선 추적 데이터 수집 및 보정

#### 문제

브라우저는 Tobii Eye Tracker에 직접 접근할 수 없으므로 아동 앱과 시선 추적 장치 사이를 연결할 별도 실행 경계가 필요합니다.

#### 해결

로컬 FastAPI bridge와 C++ native bridge를 이용해 장치 데이터를 수집하고 WebSocket으로 아동 앱에 전달합니다. 장치가 없거나 연결에 실패하면 마우스 포인터 기반 fallback으로 동작할 수 있도록 구성했습니다.

[시선 데이터 흐름과 상세 처리 단계 보기](#gaze-data-flow)

#### 결과

- [TBD] 시선 데이터 수집 주기와 보정 결과를 작성합니다.
- [TBD] 장치 연결 및 fallback 검증 결과를 작성합니다.

### 2. Azure Speech 기반 발음 평가

#### 문제

일반 STT 전사와 기준 문자열 비교만으로는 표기와 실제 발음이 다른 한국어 단어의 발음 정확도를 평가하기 어렵습니다.

#### 해결

AI server가 Azure Speech `ko-KR` scripted Pronunciation Assessment를 호출합니다. 단어별 정확도와 오류 유형을 Backend 계약으로 전달하며, 음성 원본은 분석 요청 동안만 사용하고 성공·실패 후 보관하지 않습니다.

<!-- 기술 흐름 이미지: docs/assets/readme/details/pronunciation-flow.png -->

#### 결과

- 단어 단위 `AccuracyScore`와 읽기 누락 여부를 학습 수행 근거로 사용할 수 있습니다.
- Azure 자격증명과 분석 호출을 AI server 경계에 한정합니다.
- [TBD] 실제 음성 fixture 검증 결과와 평균 처리 시간을 작성합니다.

### 3. 개인화 읽기 훈련

#### 문제

아동마다 읽기 특성과 변화 속도가 다르므로 동일한 순서와 난이도의 훈련만으로는 개인별 학습 과정을 충분히 지원하기 어렵습니다.

#### 해결

[TBD] 시선, 발음, 읽기 수행 데이터를 훈련 구성에 반영하는 기준과 과정을 작성합니다.

<!-- 기술 흐름 이미지: docs/assets/readme/details/personalization-flow.png -->

#### 결과

- [TBD] 개인화 기준과 적용 결과를 작성합니다.
- [TBD] 훈련 전후 비교 또는 검증 결과를 작성합니다.

### 4. 실시간 학습 현황 연동

#### 문제

아동 앱과 교수자 앱이 서로 분리되어 있어 훈련 진행 상태를 별도의 새로고침 없이 전달할 방법이 필요합니다.

#### 해결

Backend를 중심으로 SSE 연결을 구성해 교수자에서 아동으로 전달되는 상태와 아동에서 교수자로 전달되는 훈련 진행 정보를 실시간으로 연동합니다.

<!-- 기술 흐름 이미지: docs/assets/readme/details/realtime-sync-flow.png -->

#### 결과

- 통합 데모 환경에서 양방향 이벤트 전달을 확인할 수 있습니다.
- [TBD] 최종 측정 환경과 응답 시간 결과를 작성합니다.

---

<details>
<summary><strong>🚀 개발자 가이드</strong></summary>

<br />

저장소 구성, 통합 데모 실행 방법과 검증 절차는 [README_V1.md](README_V1.md)에서 확인할 수 있습니다.

</details>

<details>
<summary><strong>📁 프로젝트 문서</strong></summary>

<br />

- [문서 인덱스](docs/index.md)
- [제품 비전과 범위](docs/product/vision-and-scope.md)
- [시스템 컨텍스트](docs/architecture/system-context.md)
- [계약 카탈로그](contracts/catalog.md)
- [ADR 목록](docs/decisions/index.md)

</details>

<details>
<summary><strong>🌿 브랜치 및 커밋 컨벤션</strong></summary>

<br />

[Git Flow 및 커밋 정책](docs/workflows/git-flow.md)을 확인합니다.

</details>
