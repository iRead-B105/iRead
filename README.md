<div align="center">

<!-- iRead 로고: docs/assets/readme/overview/iread-logo.png -->

# iRead

### 아동의 읽기 특성을 이해하는 개인화 읽기 훈련 시스템

<!-- 대표 이미지 또는 핵심 기능 GIF: docs/assets/readme/overview/service-overview.* -->

**개발 기간** 2026.07.06 ~ 2026.08.10 (6주)<br />
**개발 인원** 6명<br />
**플랫폼** 교수자 Web · 아동 Windows Electron App

**[TBD] 서비스 시연 영상** · **[Swagger API 명세](#api-specification)** · **[TBD] 화면 설계서**

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

<table>
  <tr>
    <th width="18%">분류</th>
    <th>기술</th>
  </tr>
  <tr>
    <td><strong>Frontend Web</strong></td>
    <td>
      <img src="https://img.shields.io/badge/Vue.js%203-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white" alt="Vue.js 3" />
      <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
      <img src="https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white" alt="Vite" />
      <img src="https://img.shields.io/badge/pnpm-F69220?style=flat-square&logo=pnpm&logoColor=white" alt="pnpm" />
    </td>
  </tr>
  <tr>
    <td><strong>Frontend App</strong></td>
    <td>
      <img src="https://img.shields.io/badge/Vue.js%203-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white" alt="Vue.js 3" />
      <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
      <img src="https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white" alt="Vite" />
      <img src="https://img.shields.io/badge/Electron-47848F?style=flat-square&logo=electron&logoColor=white" alt="Electron" />
    </td>
  </tr>
  <tr>
    <td><strong>Backend</strong></td>
    <td>
      <img src="https://img.shields.io/badge/Java%2021-ED8B00?style=flat-square&logo=openjdk&logoColor=white" alt="Java 21" />
      <img src="https://img.shields.io/badge/Spring%20Boot%204.0.7-6DB33F?style=flat-square&logo=springboot&logoColor=white" alt="Spring Boot 4.0.7" />
      <img src="https://img.shields.io/badge/Gradle-02303A?style=flat-square&logo=gradle&logoColor=white" alt="Gradle" />
    </td>
  </tr>
  <tr>
    <td><strong>AI Server</strong></td>
    <td>
      <img src="https://img.shields.io/badge/Python%203.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.12" />
      <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
      <img src="https://img.shields.io/badge/uv-DE5FE9?style=flat-square&logo=astral&logoColor=white" alt="uv" />
      <img src="https://img.shields.io/badge/Azure%20Speech-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" alt="Azure Speech" />
    </td>
  </tr>
  <tr>
    <td><strong>Database</strong></td>
    <td>
      <img src="https://img.shields.io/badge/MySQL%208.4%20LTS-4479A1?style=flat-square&logo=mysql&logoColor=white" alt="MySQL 8.4 LTS" />
    </td>
  </tr>
  <tr>
    <td><strong>Infrastructure</strong></td>
    <td>
      <img src="https://img.shields.io/badge/Amazon%20EC2-FF9900?style=flat-square&logo=amazonec2&logoColor=white" alt="Amazon EC2" />
      <img src="https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white" alt="Nginx" />
      <img src="https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis" />
      <img src="https://img.shields.io/badge/Docker%20Compose-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker Compose" />
    </td>
  </tr>
  <tr>
    <td><strong>Eye Tracking</strong></td>
    <td>
      <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
      <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript" />
      <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=flat-square&logo=cplusplus&logoColor=white" alt="C++" />
      <img src="https://img.shields.io/badge/Tobii%20Game%20Integration%20SDK-5B2C83?style=flat-square" alt="Tobii Game Integration SDK" />
    </td>
  </tr>
</table>

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

<details>
<summary><strong>시선 데이터 흐름도 보기</strong></summary>

<br />

#### 요약 흐름도

![iRead 시선 데이터 흐름 요약](docs/assets/readme/architecture/gaze-data-flow-overview.png)

#### 상세 흐름도

![iRead 시선 데이터 상세 흐름도](docs/assets/readme/architecture/gaze-data-flow-detail.png)

</details>

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

<details>
<summary><strong>Swagger API 명세 보기</strong></summary>

<br />

![iRead Swagger API 명세](docs/assets/readme/api/swagger-api.png)

</details>

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
