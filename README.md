<img src="docs/assets/readme/overview/service-overview.png" width="100%" alt="난독증 훈련 보조 서비스 iRead 대표 이미지" />
<div align="center"><br>


# iRead

### 아동의 읽기 특성을 이해하는 개인화 읽기 훈련 시스템

**개발 인원** 6명<br />
**개발 기간** 2026.07.06 ~ 2026.08.10 (6주)<br />
**플랫폼** 교수자 Web · 아동 Windows Electron App<br />
**프로젝트 자료** [발표 자료 보기](docs/assets/readme/portfolio/iread-presentation-b105.pdf) · [소개 영상 보기](docs/assets/readme/portfolio/iread-video-portfolio-b105.mp4)<br />
<img src="docs/assets/readme/overview/cta-mascot.png" width="180" alt="iRead 마스코트 토리" />

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

## iRead 서비스 소개

**iRead는 읽기에 어려움을 겪는 초등학교 저학년 난독증 아동을 위한 시선·발음 데이터 기반 맞춤형 읽기 훈련 서비스입니다.**

기존 읽기 학습은 정답과 점수 같은 결과를 중심으로 평가하기 때문에, 아동이 **어디에서 머뭇거리고 어떤 단어나 문장을 어려워하는지** 읽는 과정까지 파악하기 어렵습니다.

iRead는 아동이 글을 읽는 동안의 **시선과 발음 데이터를 분석해 읽기 특성을 파악**합니다. 이를 바탕으로 아동에게는 자신의 수준과 특성에 맞는 읽기 훈련을 제공하고, 교수자에게는 아동의 어려움과 학습 변화를 확인할 수 있는 데이터를 제공합니다.

아동은 **이야기와 놀이 중심의 콘텐츠**를 통해 부담 없이 읽기 훈련을 이어가고, 교수자는 축적된 **시선·발음·학습 데이터와 리포트**를 통해 아동의 읽기 과정을 이해하고 맞춤형 커리큘럼을 관리할 수 있습니다. 보호자 역시 리포트를 통해 아동의 학습 현황과 성장 과정을 확인할 수 있습니다.

## iRead가 제공하는 가치

### 읽는 과정까지 이해하는 분석

정답과 점수뿐만 아니라 시선과 발음을 함께 분석해 아동이 **어디에서 어려움을 겪는지** 구체적으로 확인합니다.

### 아동에게 맞는 읽기 훈련

아동의 읽기 특성과 학습 진행 상황을 바탕으로 **개인별 맞춤형 훈련**을 제공합니다.

### 변화가 보이는 학습 관리

훈련 결과와 검사 데이터, 학습 변화 추이를 한눈에 보여주어 교수자가 **아동의 성장 과정과 필요한 학습을 판단**할 수 있도록 돕습니다.

### 즐겁게 지속하는 학습 경험

이야기와 놀이, 상호작용 중심의 콘텐츠를 통해 아동이 읽기 훈련을 **부담이 아닌 즐거운 경험으로 지속**할 수 있도록 합니다.

---

<a id="team"></a>

## 👥 팀원 소개 및 역할

<table>
  <tr>
    <td align="center" width="33%">
      <strong>윤정</strong>
      <br />
      PM · 백엔드
      <br />
      <a href="https://github.com/dbswjd0191a"><code>dbswjd0191a</code></a>
    </td>
    <td align="center" width="33%">
      <img
        src="docs/assets/readme/profile/kim-jihoon.jpg"
        alt="김지훈"
        width="120"
      />
      <br />
      <strong>김지훈</strong>
      <br />
      교수자 웹 백엔드
      <br />
      <a href="https://github.com/2hnK"><code>2hnK</code></a>
    </td>
    <td align="center" width="33%">
      <strong>정의찬</strong>
      <br />
      아동 앱 백엔드
      <br />
      <a href="https://github.com/uichan01"><code>uichan01</code></a>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <strong>담당 기능</strong><br />
      프로젝트 관리 · 커리큘럼 및 훈련 백엔드<br /><br />
      <strong>주요 구현 내용</strong><br />
      <ul>
        <li>훈련 카탈로그와 문항 정책 정리</li>
        <li>커리큘럼 교안 자동 생성 연동</li>
        <li>진단 문항·발음 평가·성장 정보 API 안정화</li>
      </ul>
    </td>
    <td valign="top">
      <strong>담당 기능</strong><br />
      교수자 웹 API · 학습 및 이야기 관리<br /><br />
      <strong>주요 구현 내용</strong><br />
      <ul>
        <li>학습 현황·이력·보고서 API 구현</li>
        <li>커리큘럼·교안 편집 계약 구현</li>
        <li>SSE 학습 상태와 이야기·이미지 관리 연동</li>
      </ul>
    </td>
    <td valign="top">
      <strong>담당 기능</strong><br />
      아동 앱 API · 훈련 및 이야기 실행<br /><br />
      <strong>주요 구현 내용</strong><br />
      <ul>
        <li>훈련 제출·진행·재진입과 성장 정보 API 연동</li>
        <li>이야기 분기 생성 중복 제어</li>
        <li>교안 생성 완료 실시간 알림 구현</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <strong>김민재</strong>
      <br />
      프론트엔드
      <br />
      <a href="https://github.com/minjaekim1122"><code>minjaekim1122</code></a>
    </td>
    <td align="center" width="33%">
      <strong>이승환</strong>
      <br />
      인프라 · 아이트래커
      <br />
      <a href="https://github.com/wanderingperson"><code>wanderingperson</code></a>
    </td>
    <td align="center" width="33%">
      <strong>송승우</strong>
      <br />
      AI
      <br />
      <a href="https://github.com/themancalledsong"><code>themancalledsong</code></a>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <strong>담당 기능</strong><br />
      교수자 웹 프론트엔드<br /><br />
      <strong>주요 구현 내용</strong><br />
      <ul>
        <li>학습 현황·이력·보고서 화면 구현</li>
        <li>커리큘럼·교안 편집 UI 구현</li>
        <li>이야기 이미지 재생성과 시선 리플레이 연동</li>
      </ul>
    </td>
    <td valign="top">
      <strong>담당 기능</strong><br />
      배포 인프라 · Tobii 아이트래커<br /><br />
      <strong>주요 구현 내용</strong><br />
      <ul>
        <li>AWS·Nginx·Docker Compose 배포 환경 구성</li>
        <li>Tobii 보정·연결 상태·자동 실행 구현</li>
        <li>단어별 시선 수집·분석·리플레이 구현</li>
      </ul>
    </td>
    <td valign="top">
      <strong>담당 기능</strong><br />
      개인화 학습 · 생성형 AI · 발음 평가<br /><br />
      <strong>주요 구현 내용</strong><br />
      <ul>
        <li>읽기 프로필 기반 커리큘럼·교안 생성 및 검증</li>
        <li>개인화 이야기·장면 이미지 생성 API 구현</li>
        <li>Azure Speech 발음 평가 피드백 구현</li>
      </ul>
    </td>
  </tr>
</table>

---

<a id="features"></a>

## ✨ 주요 기능

| 기능 | 설명 |
| --- | --- |
| 개인화 읽기 훈련 | 아동 앱에서 배정된 커리큘럼을 열고 글자 따라 읽기, 첫소리 찾기, 소리 합치기, 문장 만들기 등의 훈련을 진행합니다. |
| 시선 기반 읽기 분석 | Tobii Eye Tracker로 훈련 중 시선을 수집하고 화면의 단어·문장 영역과 연결해 머문 시간, 건너뜀, 되읽기 정보를 기록합니다. |
| 단어별 발음 평가 | 마이크로 수집한 읽기 음성을 Azure Speech로 분석해 단어별 정확도와 오류 유형을 표시합니다. |
| AI 이야기 학습 | 아동의 학습 진행과 선택을 반영해 이야기와 장면 이미지를 생성하고, 이야기 화면에서 읽기와 선택 활동을 진행합니다. |
| 교수자 학습 관리 | 교수자 웹에서 커리큘럼을 생성·편집하고 아동별 학습 현황, 학습 이력, 분석 보고서와 이야기 기록을 조회합니다. |

### 1. 개인화 읽기 훈련

<table>
  <tr>
    <td colspan="2" align="center">
      <img src="docs/assets/readme/features/child-app/login.gif" width="75%" alt="아동 앱 로그인 후 학습 영역을 선택하는 화면" /><br />
      <strong>아동 앱 로그인 및 학습 영역 선택</strong><br />
      <sub>아동 프로필로 로그인한 뒤 학습 섬에서 진행할 영역을 선택합니다.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="docs/assets/readme/features/training/letter-practice.gif" width="100%" alt="글자를 따라 읽는 훈련 화면" /><br />
      <strong>글자 따라 읽기</strong><br />
      <sub>제시된 글자의 획순을 확인하고 마이크로 소리 내어 읽습니다.</sub>
    </td>
    <td width="50%" align="center">
      <img src="docs/assets/readme/features/training/syllable-combination.gif" width="100%" alt="소리 합치기 훈련 화면" /><br />
      <strong>소리 합치기</strong><br />
      <sub>제시된 소리 조각을 순서대로 합쳐 알맞은 낱말을 완성합니다.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="docs/assets/readme/features/training/initial-consonant-finding.gif" width="100%" alt="첫소리 찾기 훈련 화면" /><br />
      <strong>첫소리 찾기</strong><br />
      <sub>낱말의 첫소리를 듣고 보기에서 알맞은 글자를 고릅니다.</sub>
    </td>
    <td width="50%" align="center">
      <img src="docs/assets/readme/features/training/sentence-assembly.gif" width="100%" alt="문장 만들기 훈련 화면" /><br />
      <strong>문장 만들기</strong><br />
      <sub>낱말 카드를 문장 순서에 맞게 배치해 문장을 완성합니다.</sub>
    </td>
  </tr>
</table>

### 2. 시선 기반 읽기 분석

<table>
  <tr>
    <td width="55%" align="center">
      <img src="docs/assets/readme/features/training/picture-sentence-matching.gif" width="100%" alt="그림에 맞는 문장 찾기 훈련 화면" />
    </td>
    <td width="45%">
      <strong>그림에 맞는 문장 찾기</strong><br />
      그림의 내용을 확인하고 세 개의 보기에서 알맞은 문장을 선택합니다.<br /><br />
      훈련 중 Tobii Eye Tracker가 수집한 시선 좌표를 화면의 그림과 문장 영역에 연결해 머문 시간, 건너뜀과 되읽기 정보를 기록합니다.
    </td>
  </tr>
</table>

### 3. 단어별 발음 평가

<table>
  <tr>
    <td width="55%" align="center">
      <img src="docs/assets/readme/features/training/word-reading.gif" width="100%" alt="낱말 읽기와 발음 평가 화면" />
    </td>
    <td width="45%">
      <strong>낱말 읽기와 발음 평가</strong><br />
      화면에 제시된 낱말을 마이크로 읽고 단어별 발음 평가를 진행합니다.<br /><br />
      Azure Speech의 한국어 발음 평가가 읽기 음성을 분석하고 단어별 정확도와 오류 유형을 제공합니다.
    </td>
  </tr>
</table>

### 4. AI 이야기 학습

<table>
  <tr>
    <td width="55%" align="center">
      <img src="docs/assets/readme/features/story/story-branch.gif" width="100%" alt="이야기 내용을 읽고 다음 내용을 선택하는 화면" />
    </td>
    <td width="45%">
      <strong>이야기 선택</strong><br />
      이야기를 읽은 뒤 질문에 답하며 다음 장면의 흐름을 선택합니다.<br /><br />
      아동의 학습 진행을 반영해 생성된 이야기와 장면 이미지를 읽고 화면의 선택지에서 다음 내용을 고릅니다.
    </td>
  </tr>
  <tr>
    <td width="55%" align="center">
      <img src="docs/assets/readme/features/story/story-world.gif" width="100%" alt="새 이야기 생성 진행 화면" />
    </td>
    <td width="45%">
      <strong>새 이야기 생성</strong><br />
      학습을 마친 뒤 새로운 이야기 생성을 요청합니다.<br /><br />
      아동의 학습 진행을 반영한 이야기 본문과 장면 이미지를 생성합니다.
    </td>
  </tr>
</table>

### 5. 교수자 학습 관리

<table>
  <tr>
    <td width="55%" align="center">
      <img src="docs/assets/readme/features/teacher/report.gif" width="100%" alt="교수자용 학습 분석 리포트 화면" />
    </td>
    <td width="45%">
      <strong>학습 분석 보고서</strong><br />
      아동별 학습 참여, 발음 정확도, 읽기 속도와 기간별 변화 추이를 확인합니다.<br /><br />
      보고서 화면에는 학습 참여 일수, 총 학습 시간과 총 학습 횟수가 함께 표시됩니다.
    </td>
  </tr>
</table>

#### 교수자 관리 화면

<table>
  <tr>
    <td width="50%" align="center">
      <img src="docs/assets/readme/features/teacher/curriculum-ai-generation.gif" width="100%" alt="AI 기반 개인화 커리큘럼 생성 화면" /><br />
      <strong>AI 커리큘럼 생성</strong><br />
      <sub>아동과 학습 기간을 선택해 개인화 커리큘럼 생성을 요청합니다.</sub>
    </td>
    <td width="50%" align="center">
      <img src="docs/assets/readme/features/teacher/curriculum-material-editing.gif" width="100%" alt="개인화 커리큘럼 교안 편집 화면" /><br />
      <strong>커리큘럼 교안 편집</strong><br />
      <sub>훈련별 문항, 정답, 보기와 안내 내용을 확인하고 수정합니다.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="docs/assets/readme/features/teacher/learning-status.gif" width="100%" alt="아동 학습 현황 화면" /><br />
      <strong>학습 현황</strong><br />
      <sub>아동의 학습 진행률과 지표별 변화 추이를 조회합니다.</sub>
    </td>
    <td width="50%" align="center">
      <img src="docs/assets/readme/features/teacher/learning-history.gif" width="100%" alt="아동 학습 이력 화면" /><br />
      <strong>학습 이력</strong><br />
      <sub>회차별 훈련 결과와 문항별 상세 기록을 확인합니다.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="docs/assets/readme/features/teacher/story-image-regeneration.gif" width="100%" alt="이야기 이미지 재생성 화면" /><br />
      <strong>이야기 이미지 재생성</strong><br />
      <sub>이야기 장면과 생성 정보를 확인하고 필요한 이미지를 다시 생성합니다.</sub>
    </td>
    <td width="50%" align="center">
      <img src="docs/assets/readme/features/teacher/story-reading-replay.gif" width="100%" alt="이야기 읽기 리플레이 화면" /><br />
      <strong>이야기 읽기 리플레이</strong><br />
      <sub>이야기 페이지와 함께 단어별 시선 이동과 읽기 기록을 재생합니다.</sub>
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
      <img src="https://img.shields.io/badge/Pinia-FFD859?style=flat-square&logo=pinia&logoColor=black" alt="Pinia" />
      <img src="https://img.shields.io/badge/Tailwind%20CSS%204-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind CSS 4" />
      <img src="https://img.shields.io/badge/ECharts%206-AA344D?style=flat-square&logo=apacheecharts&logoColor=white" alt="ECharts 6" />
    </td>
  </tr>
  <tr>
    <td><strong>Frontend App</strong></td>
    <td>
      <img src="https://img.shields.io/badge/Vue.js%203-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white" alt="Vue.js 3" />
      <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
      <img src="https://img.shields.io/badge/Pinia-FFD859?style=flat-square&logo=pinia&logoColor=black" alt="Pinia" />
      <img src="https://img.shields.io/badge/Rive-1D1D1D?style=flat-square&logo=rive&logoColor=white" alt="Rive" />
      <img src="https://img.shields.io/badge/Electron-47848F?style=flat-square&logo=electron&logoColor=white" alt="Electron" />
    </td>
  </tr>
  <tr>
    <td><strong>Backend</strong></td>
    <td>
      <img src="https://img.shields.io/badge/Java%2021-ED8B00?style=flat-square&logo=openjdk&logoColor=white" alt="Java 21" />
      <img src="https://img.shields.io/badge/Spring%20Boot%204.0.7-6DB33F?style=flat-square&logo=springboot&logoColor=white" alt="Spring Boot 4.0.7" />
      <img src="https://img.shields.io/badge/Spring%20Data%20JPA-6DB33F?style=flat-square&logo=spring&logoColor=white" alt="Spring Data JPA" />
      <img src="https://img.shields.io/badge/Spring%20Security-6DB33F?style=flat-square&logo=springsecurity&logoColor=white" alt="Spring Security" />
      <img src="https://img.shields.io/badge/Flyway-CC0200?style=flat-square&logo=flyway&logoColor=white" alt="Flyway" />
    </td>
  </tr>
  <tr>
    <td><strong>AI Server</strong></td>
    <td>
      <img src="https://img.shields.io/badge/Python%203.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.12" />
      <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
      <img src="https://img.shields.io/badge/OpenAI%20API-412991?style=flat-square&logo=openai&logoColor=white" alt="OpenAI API" />
      <img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white" alt="Google Gemini" />
      <img src="https://img.shields.io/badge/Azure%20Speech-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" alt="Azure Speech" />
    </td>
  </tr>
  <tr>
    <td><strong>Data</strong></td>
    <td>
      <img src="https://img.shields.io/badge/MySQL%208.4%20LTS-4479A1?style=flat-square&logo=mysql&logoColor=white" alt="MySQL 8.4 LTS" />
      <img src="https://img.shields.io/badge/Redis%207.4-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis 7.4" />
    </td>
  </tr>
  <tr>
    <td><strong>Infrastructure</strong></td>
    <td>
      <img src="https://img.shields.io/badge/Amazon%20EC2-FF9900?style=flat-square&logo=amazonec2&logoColor=white" alt="Amazon EC2" />
      <img src="https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white" alt="Nginx" />
      <img src="https://img.shields.io/badge/Docker%20Compose-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker Compose" />
      <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions" />
      <img src="https://img.shields.io/badge/GHCR-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub Container Registry" />
    </td>
  </tr>
  <tr>
    <td><strong>Eye Tracking</strong></td>
    <td>
      <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
      <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
      <img src="https://img.shields.io/badge/WebSocket-010101?style=flat-square&logoColor=white" alt="WebSocket" />
      <img src="https://img.shields.io/badge/C%2B%2B-00599C?style=flat-square&logo=cplusplus&logoColor=white" alt="C++" />
      <img src="https://img.shields.io/badge/Tobii%20Game%20Integration%20SDK-5B2C83?style=flat-square" alt="Tobii Game Integration SDK" />
    </td>
  </tr>
</table>

---

<a id="system-architecture"></a>

## 🏗️ 시스템 아키텍처

![iRead 시스템 아키텍처](docs/assets/readme/architecture/system-architecture.png)

<a id="gaze-data-flow"></a>


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

### 1. 시선 데이터 수집 및 분석

Tobii Eye Tracker는 브라우저에서 직접 제어할 수 없으므로, 아동용 Windows 앱과 함께 실행되는 로컬 브리지가 장치의 시선 좌표를 수집합니다. 수집된 좌표는 Electron IPC를 통해 앱으로 전달되고, 화면의 단어·문장 위치와 대조해 단어별 머문 시간, 고정 횟수, 건너뜀과 되읽기 지표로 변환됩니다. 계산 결과는 Backend에 저장되어 교수자 리포트와 이후 훈련 구성에 사용됩니다.

### 2. 발음 평가

아동이 읽은 음성은 아동 앱에서 Backend를 거쳐 AI server로 전달됩니다. AI server는 Azure Speech의 한국어 단어 단위 발음 평가를 이용해 단어별 정확도, 오류 유형과 발음 구간을 분석합니다. Backend는 분석된 단어가 기준 문장과 같은 순서로 정렬되는지 확인하고, 일치하는 결과만 학습 기록에 저장합니다.

### 3. 개인화 훈련 구성

Backend는 완료된 학습에서 정답 여부, 발음 정확도, 평균 읽기 시간과 시선 지표를 모아 아동의 읽기 특성별 프로필을 구성합니다. AI server는 어려움이 크게 나타난 특성과 데이터의 신뢰도를 바탕으로 핵심 훈련 3개, 보완 훈련 1개, 확장 훈련 1개를 조합해 다음 커리큘럼을 추천합니다. 생성된 문항은 문제 형식, 정답과 필수 입력값을 확인한 뒤 조건을 충족한 경우에만 커리큘럼에 반영됩니다.

### 4. AI 이야기 생성

AI server는 아동의 학습 진행 상황, 읽기 특성과 이전 선택을 반영해 다음 이야기와 장면 이미지를 생성합니다. 이야기 텍스트와 이미지는 OpenAI, Gemini, GMS 중 서로 다른 공급자를 선택할 수 있으며, 공급자가 달라도 Backend에는 같은 형식으로 전달됩니다. 생성된 내용은 페이지 구성, 이야기 분기, 어휘와 데이터 형식을 확인하고, 오류가 있으면 정해진 횟수만큼 다시 생성한 뒤 최종 조건을 충족한 결과만 저장합니다.

### 5. 실시간 학습 연동

아동 앱과 교수자 Web은 서로 직접 연결하지 않고 Backend를 통해 학습 상태를 공유합니다. Backend는 서버 전송 이벤트(SSE)로 훈련 시작·완료와 학습 정보 변경 사실을 알리고, 각 화면은 관련 API를 다시 조회해 최신 내용을 표시합니다. 연결이 끊어졌을 때는 하트비트와 자동 재연결을 이용해 실시간 동기화를 복구합니다.

---

<details>
<summary><strong>🚀 개발자 가이드 (빌드·실행)</strong></summary>

<br />

### 사전 준비

| 도구 | 용도 |
| --- | --- |
| Git | 루트 저장소와 submodule 내려받기 |
| Docker Desktop | 통합 데모 환경 실행 |
| Node.js·pnpm | 교수자 Web과 아동 App 개발·검증 |
| Java 21 | Spring Boot Backend 실행·검증 |
| Python 3.12·uv | AI server 실행·검증 |
| Windows·Tobii SDK | 실제 Eye Tracker를 사용하는 경우에만 필요 |

### 저장소 받기

```bash
git clone --recurse-submodules https://github.com/iRead-B105/iRead.git
cd iRead
```

이미 루트 저장소만 clone했다면 submodule을 초기화합니다.

```bash
git submodule update --init --recursive
```

### 통합 데모 실행

Docker Compose로 전체 서비스를 실행합니다.

```bash
cp .env.example .env
docker compose up -d
```

Windows에서 각 서비스를 로컬 프로세스로 실행하려면 `.env.example`을 `.env`로 복사한 뒤 다음 스크립트를 사용할 수 있습니다.

```powershell
.\start-all-local.bat
```

| 서비스 | 주소 |
| --- | --- |
| 교수자 Web | `http://localhost:5173` |
| 아동 App | `http://localhost:5174` |
| Backend API | `http://localhost:8080` |
| AI server | `http://localhost:8081` |
| Mailpit | `http://localhost:8025` |

### 서비스별 검증

아래 명령은 저장소 루트에서 각 서비스 디렉터리로 이동해 실행합니다.

```bash
# Frontend Web
cd services/frontend-web
pnpm install
pnpm build
pnpm test
cd ../..

# Frontend App
cd services/frontend-app
pnpm install
pnpm build
pnpm test
cd ../..
```

```powershell
# Backend
cd services\backend
.\gradlew.bat test
cd ..\..

# AI server
cd services\ai
uv sync --extra dev
uv run pytest
cd ..\..
```

Tobii Eye Tracker를 사용할 때는 Windows에서 시선 추적 bridge를 먼저 실행합니다.

```powershell
cd services\eyetracking
.\run_server.bat
cd ..\..
```

</details>

<details>
<summary><strong>📁 디렉터리 구조</strong></summary>

<br />

```text
iRead/
├─ services/
│  ├─ backend/          # Spring Boot API와 데이터 처리
│  ├─ frontend-web/     # 교수자용 Vue Web
│  ├─ frontend-app/     # 아동용 Vue·Electron App
│  ├─ ai/               # FastAPI 기반 AI 기능
│  └─ eyetracking/      # Tobii 시선 수집·보정 bridge
├─ contracts/
│  ├─ openapi/          # App·Admin·Auth·AI API 계약
│  └─ database/         # MySQL 스키마와 ERD
├─ docs/                # 제품·아키텍처·결정·계획 문서
│  └─ assets/readme/
│     ├─ api/           # Swagger 명세 이미지
│     ├─ architecture/  # 시스템·데이터 흐름도
│     └─ features/
│        ├─ child-app/  # 아동 앱 공통 화면 GIF
│        ├─ training/   # 아동 읽기 훈련 GIF
│        ├─ story/      # AI 이야기 학습 GIF
│        └─ teacher/    # 교수자 관리 화면 GIF
├─ design-resources/    # UI와 콘텐츠 제작 원본
├─ tools/               # 계약·문서·통합 데모 검증 도구
├─ compose.yml          # 로컬 통합 실행 구성
├─ .env.example         # 환경 변수 예시
└─ README.md
```

`services/*`는 각각 독립된 Git 저장소이며 루트 저장소에는 submodule로 연결됩니다.

</details>

<details>
<summary><strong>🌿 브랜치 전략 & 커밋 컨벤션</strong></summary>

### 브랜치 전략

| 브랜치 | 용도 |
| --- | --- |
| `main` | 배포 가능한 릴리스 이력 |
| `develop` | 다음 릴리스의 통합 기준 |
| `feature/*` | 기능 개발과 검토가 필요한 변경 |
| `release/*` | 정식 릴리스 안정화 |
| `hotfix/*` | 운영 버전 긴급 수정 |


### 커밋 컨벤션

```text
<type>(<scope>): <한국어 제목>
```

<table>
  <tr>
    <td width="50%" valign="top">
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>용도</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><code>feat</code></td><td>사용자 기능 추가</td></tr>
          <tr><td><code>fix</code></td><td>오류 수정</td></tr>
          <tr><td><code>docs</code></td><td>문서 변경</td></tr>
          <tr><td><code>refactor</code></td><td>동작 변경 없는 구조 개선</td></tr>
          <tr><td><code>test</code></td><td>테스트 추가·수정</td></tr>
          <tr><td><code>perf</code></td><td>성능 개선</td></tr>
          <tr><td><code>style</code></td><td>동작과 무관한 서식 변경</td></tr>
          <tr><td><code>build</code></td><td>빌드와 의존성 변경</td></tr>
          <tr><td><code>ci</code></td><td>CI/CD 설정 변경</td></tr>
          <tr><td><code>chore</code></td><td>기타 유지보수</td></tr>
          <tr><td><code>revert</code></td><td>이전 커밋 되돌리기</td></tr>
        </tbody>
      </table>
    </td>
    <td width="50%" valign="top">
      <table>
        <thead>
          <tr>
            <th>Scope</th>
            <th>용도</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><code>feat(training)</code></td><td>개인화 훈련 조회 기능 추가</td></tr>
          <tr><td><code>fix(gaze)</code></td><td>시선 세션 종료 오류 수정</td></tr>
          <tr><td><code>docs(readme)</code></td><td>프로젝트 소개 갱신</td></tr>
        </tbody>
      </table>
    </td>
  </tr>
</table>

</details>
