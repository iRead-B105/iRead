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

## 📌 서비스 소개

iRead는 읽기에 어려움을 겪는 초등학교 저학년 난독증 아동을 위한 시선·발음 데이터 기반 맞춤형 읽기 훈련 서비스입니다.

아동은 이야기와 놀이로 구성된 콘텐츠를 통해 즐겁게 읽기 훈련을 이어갈 수 있고, 교수자는 훈련 중 수집된 시선·발음·학습 데이터를 통해 아동이 어떤 부분에서 어려움을 겪는지 파악하고 학습 변화를 확인할 수 있습니다.

### 기획 배경

기존의 읽기 학습 결과만으로는 아동이 글을 읽는 동안 어디에서 머뭇거리는지, 어떤 단어나 문장을 어려워하는지 구체적으로 파악하기 어렵습니다.

iRead는 아동이 글을 읽는 동안의 시선과 발음을 분석해 읽기 특성을 파악하고, 그 결과를 바탕으로 아동에게는 맞춤형 훈련을, 교수자에게는 상세한 리포트를 제공합니다.

### 대상 사용자

| 사용자 | 제공 가치 |
| --- | --- |
| 아동 | 이야기와 놀이를 통해 자신의 수준에 맞는 읽기 훈련을 진행합니다. |
| 교수자 | 시선·발음·학습 데이터를 바탕으로 아동의 읽기 과정과 변화를 확인하고, 커리큘럼을 관리합니다. |
| 보호자 | 보고서를 통해 아동의 학습 현황과 성장 과정을 확인할 수 있습니다. |

### 핵심 가치

1. **읽는 과정까지 들여다보는 분석**<br>
정답과 점수뿐 아니라 시선과 발음까지 함께 분석해 아동이 글을 읽어가는 과정을 살펴봅니다.
2. **아동 맞춤형 읽기 훈련**<br>
아동 개개인의 읽기 특성과 학습 진행 상황을 반영한 맞춤형 훈련을 제공합니다.
3. **한눈에 보이는 학습 변화**<br>
훈련 결과와 검사 데이터, 학습 변화 추이를 교수자 화면과 리포트로 한눈에 확인할 수 있습니다.
4. **즐겁게 지속하는 학습 경험**<br>
이야기와 상호작용 중심의 콘텐츠로 아동이 읽기 훈련을 부담 없이 꾸준히 이어갈 수 있도록 돕습니다.

<!-- 서비스 이용 흐름 이미지: docs/assets/readme/overview/service-flow.png -->

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
      <strong>김지훈</strong>
      <br />
      교수자 웹 백엔드
      <br />
      <a href="https://github.com/2hnK"><code>2hnK</code></a>
    </td>
    <td align="center" width="33%">
      <strong>정의찬</strong>
      <br />
      아동 앱 백엔드 · 인프라
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
      아동 앱 API · 훈련 및 이야기 실행 · 배포 인프라<br /><br />
      <strong>주요 구현 내용</strong><br />
      <ul>
        <li>AWS·Nginx·Docker Compose 배포 환경 구성</li>
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
        <img
          src="docs/assets/readme/profile/lee-seunghwan.jpg"
          alt="이승환"
          width="120"
        />
      <br />
      <strong>이승환</strong>
      <br />
      아이트래커
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
      Tobii 아이트래커 연동 · 시선 데이터 처리 및 분석<br /><br />
      <strong>주요 구현 내용</strong><br />
      <ul>
        <li>Tobii 보정·연결 상태·자동 실행 구현</li>
        <li>실시간 시선 좌표 수집 및 단어 단위 데이터 매핑</li>
        <li>단어별 시선 분석·리플레이 구현</li>
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
| 📚 개인화 읽기 훈련 | 아동 앱에서 배정된 커리큘럼을 열고 글자 따라 읽기, 첫소리 찾기, 소리 합치기, 문장 만들기 등의 훈련을 진행합니다. |
| 👁️ 시선 기반 읽기 분석 | Tobii Eye Tracker로 훈련 중 시선을 수집하고 화면의 단어·문장 영역과 연결해 머문 시간, 건너뜀, 되읽기 정보를 기록합니다. |
| 🗣️ 단어별 발음 평가 | 마이크로 수집한 읽기 음성을 Azure Speech로 분석해 단어별 정확도와 오류 유형을 표시합니다. |
| ✨ AI 이야기 학습 | 아동의 학습 진행과 선택을 반영해 이야기와 장면 이미지를 생성하고, 이야기 화면에서 읽기와 선택 활동을 진행합니다. |
| 📊 교수자 학습 관리 | 교수자 웹에서 커리큘럼을 생성·편집하고 아동별 학습 현황, 학습 이력, 분석 보고서와 이야기 기록을 조회합니다. |

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

아동의 학습 데이터가 수집되고 분석되어 다음 학습으로 이어지는 과정을 중심으로 정리합니다.

### 1. 시선 데이터 수집 및 분석

Electron IPC와 로컬 시선 추적 bridge를 통해 Tobii Eye Tracker의 시선 프레임을 아동 앱으로 전달합니다. 수집한 좌표는 화면 요소와 매칭해 단어별 머문 시간, 건너뜀, 되읽기 등의 지표로 변환합니다. 장치 연결이 어려운 개발 환경에서는 마우스 기반 입력으로 전체 흐름을 검증할 수 있도록 구성했습니다.


### 2. 발음 평가

AI server가 Azure Speech의 한국어 발음 평가를 호출하고, 단어별 정확도와 오류 유형을 Backend에 전달합니다. Backend는 기준 문장과 분석 결과의 단어 순서를 검증한 뒤 학습 결과로 저장합니다. 음성 원본은 분석 과정에서만 사용하며, 처리가 끝나면 별도로 보관하지 않습니다.

<!-- 기술 흐름 이미지: docs/assets/readme/details/pronunciation-flow.png -->

### 3. 개인화 훈련 구성

완료된 학습에서 정답 여부, 발음 정확도, 시선 부담과 응답 지연을 읽기 특성별로 집계합니다. 분석된 취약 특성을 기준으로 직접 보완 훈련, 확장 훈련, 복습 훈련을 조합해 다음 학습을 구성합니다. 생성 결과는 문제 형식과 정답, 필수 입력 조건을 검증하며, 검증에 실패한 결과는 저장하지 않습니다.

<!-- 기술 흐름 이미지: docs/assets/readme/details/personalization-flow.png -->

### 4. AI 이야기 생성

아동의 학습 진행과 선택을 바탕으로 다음 이야기와 장면 이미지를 생성합니다. 생성된 페이지는 필수 구성과 내용 품질을 확인하며, 검증에 실패하면 제한된 횟수만큼 다시 생성합니다. 최종 검증을 통과한 경우에만 이야기를 저장해 불완전한 콘텐츠가 노출되지 않도록 합니다.

<!-- 기술 흐름 이미지: docs/assets/readme/details/ai-story-flow.png -->

### 5. 실시간 학습 연동

아동 앱과 교수자 Web은 서로 직접 연결하지 않고, Backend의 인증된 SSE 연결을 통해 상태를 전달합니다. 훈련 시작과 완료, 학습 정보 변경 등의 이벤트가 발생하면 관련 데이터를 다시 조회하도록 하며, heartbeat와 재연결 처리로 화면 상태를 유지합니다.

<!-- 기술 흐름 이미지: docs/assets/readme/details/realtime-sync-flow.png -->

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
