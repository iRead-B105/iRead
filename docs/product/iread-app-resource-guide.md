# 아이리드 앱 리소스 가이드

- 적용 대상: `services/frontend-app`
- 기준일: 2026-07-30
- 상위 기준: [아이리드 앱 디자인 가이드](iread-app-design-guide.md)
- 실행 계획: [Frontend 리소스 정비 계획](../planning/frontend-resource-plan.md)
- 현재 목록: [Frontend 에셋 인벤토리](frontend-asset-inventory.md)

## 1. 목표

아이리드의 배경, 캐릭터, 카드, 아이콘과 장식이 서로 다른 시기에 만들어져도 하나의 동화책 세계처럼 보이게 한다. 시각 오브젝트는 정식 파일로 제작하고 CSS는 배치와 상태만 담당한다.

## 2. 대표 화풍

- 고채도 2D 플랫 벡터
- 둥글고 단단한 실루엣
- 아동이 작은 화면에서도 구분할 수 있는 큰 색면
- 오브젝트당 주색 1개와 명암색 1~2개
- 외곽선 없음 또는 최소한의 내부선
- 짧고 부드러운 바닥 그림자 또는 한 단계 셀 셰이딩
- 메인 섬과 같은 선명한 하늘·초록·주황·보라 팔레트
- 학습 패널 안쪽은 크림색으로 분리해 글자와 선택지가 먼저 보이게 함

다음은 사용하지 않는다.

- 사진풍, 반실사 3D, 수채 번짐과 종이 질감
- 형광펜처럼 눈부신 단색
- 저채도만 사용해 경계가 흐린 카드
- 화면마다 달라지는 캐릭터 머리 비율, 눈 위치와 손발 크기
- 손가락 수, 겹친 눈, 비정상 관절과 의미 없는 손·장식
- 리소스 바깥의 가짜 투명 체크무늬

## 3. 리소스 분류

| 분류 | 포함 대상 | 기본 위치 |
| --- | --- | --- |
| 공통 UI | 뒤로가기, 닫기, 듣기, 다시 듣기, 재생 중, 마이크, 잠금, 체크, 화살표, 손잡이 | `src/assets/icons` |
| 선택 카드 | 글자·낱말·문장 카드의 노랑·민트·보라 variant | `src/assets/training/choice-cards` |
| 학습 UI | 진행도 별, 달력, 간판, 발판, 완료·종료 캐릭터 | `src/assets/training` |
| 캐릭터 | 기리 토끼와 상태·포즈, 이야기 친구 정원 배치본 | `src/assets/characters`, `src/assets/story/characters` |
| 세계 배경 | 메인 섬, 훈련, 이야기, 성장, 실력 도전 | `src/assets/backgrounds`, `src/assets/map` |
| 이야기 콘텐츠 | 표지, 본문 장면, 질문 장면 | `src/assets/story`; 운영 콘텐츠는 API URL |
| 학습 그림 | 낱말·문장 연결용 사물과 장면 | 기능별 폴더 |
| 원본·후보 | 생성 원본, 후보안, 고해상도 마스터, 사용 중단본 | `design-resources` |

## 4. 원본과 앱 최종본

1. 생성 원본과 후보는 `design-resources`에 저장한다.
2. 손·눈·글자·알파·화풍을 검수한다.
3. 실제 표시 크기에 맞는 런타임 사본을 만든다.
4. 승인된 최종본만 `services/frontend-app/src/assets`에 복사한다.
5. Vue 또는 CSS에서 정식 파일을 import한다.
6. 교체된 원본은 앱 폴더에 남기지 않고 `design-resources/archive`로 옮긴다.

앱 폴더에 들어간 파일은 곧 배포 후보라는 의미다. 참고 이미지, 크로마키 원본, 생성 실패본과 단순 색상 후보를 앱 폴더에 두지 않는다.

## 5. 카드 리소스

### 5.1 종류

| 종류 | 비율 | 색상 |
| --- | ---: | --- |
| 글자 카드 | `1:1` | yellow, mint, purple |
| 낱말 카드 | 약 `3:2` | yellow, mint, purple |
| 문장 카드 | 약 `2:1` | 낱말 카드와 같은 계열의 별도 가로형 variant |

- 세 카드는 한 화면에서 노랑, 민트, 보라 순서를 유지한다.
- 색상 variant는 CSS 필터가 아니라 실제 파일로 만든다.
- 색상별 캔버스, 알파, 외곽선, 점선, 안쪽 여백과 기준점은 같아야 한다.
- 카드 리소스는 프레임과 쓰기 면만 소유한다. 선택·정답·오답·힌트 링은 공통 상태 레이어가 담당한다.
- 카드 안에 또 다른 카드 테두리나 패널을 넣지 않는다.
- 학습 글자는 이미지에 굽지 않고 카드 위 HTML 텍스트로 올린다.

### 5.2 현재 공통 카드

- `choice-card-letter-yellow.png`
- `choice-card-letter-mint.png`
- `choice-card-letter-purple.png`
- `choice-card-word-yellow.png`
- `choice-card-word-mint.png`
- `choice-card-word-purple.png`
- `choice-card-sentence-yellow.png`
- `choice-card-sentence-mint.png`
- `choice-card-sentence-purple.png`

## 6. 아이콘과 상태 리소스

- 같은 행동은 모든 화면에서 같은 파일을 사용한다.
- Vue 템플릿에 inline SVG path를 작성하지 않는다.
- 유니코드 `★`, `●`, `→`, `✓`, `⠿`를 아이콘으로 사용하지 않는다.
- SVG를 사용할 때도 `src/assets/icons`의 독립 파일로 저장하고 `<img>`로 렌더링한다.
- 기본·호버는 같은 리소스의 크기·위치 변화로 표현할 수 있다.
- 형태가 달라지는 기본·재생 중·다시 듣기·성공 상태는 별도 파일을 사용한다.
- 아이콘 주변의 버튼 표면, 포커스 링과 disabled 투명도는 CSS가 담당한다.
- 시선 따라쓰기 궤적과 커리큘럼 연결선처럼 데이터에 따라 좌표가 바뀌는 기능 그래픽만 inline SVG를 허용한다. 정적 아이콘을 이 예외로 처리하지 않는다.

현재 확정된 듣기 리소스:

- `sound-listen.svg`
- `sound-playing.svg`
- `sound-replay.svg`

## 7. 캐릭터 리소스

- 같은 캐릭터의 머리 비율, 눈 위치, 귀·손발 크기와 대표 색을 고정한다.
- 기본, 읽기, 생각, 도움, 성공, 위로와 완료 포즈를 캐릭터 시트로 관리한다.
- 기리 토끼는 훈련 안내의 기본 캐릭터다.
- 이야기 원본 캐릭터와 성장 정원 배치본은 역할을 나눈다.
- 성장 정원 배치본은 서로 다른 이야기에서 생성됐더라도 동일한 캔버스 비율, 바닥 기준선, 외곽선과 조명을 사용한다.
- 정원에는 최대 4명이 보이므로 작은 크기에서도 얼굴과 실루엣이 구분되어야 한다.
- 미획득 생성형 캐릭터의 실루엣은 미리 만들지 않는다.

## 8. 글자 처리

- 학습 글자, 낱말, 문장, 동적으로 바뀌는 제목은 HTML 텍스트로 렌더링한다.
- 글자는 리소스 프레임 안에 배치할 수 있지만 픽셀에 굽지 않는다.
- 브랜드 로고, 변하지 않는 세계 간판처럼 이미지 자체가 하나의 표식인 경우만 글자를 포함할 수 있다.
- 이미지에 글자가 포함되면 오탈자, 자모 모양과 저해상도 번짐을 별도로 검수한다.

## 9. 제작 프롬프트 기본형

```text
Korean children's learning app asset,
high-saturation 2D flat vector illustration,
rounded solid silhouette, large readable color shapes,
minimal internal lines, one or two cel-shading steps,
consistent with the iRead main-island palette,
clear subject at small UI size,
no text, no watermark, no checkerboard background,
no malformed hands, extra fingers, merged eyes or distorted anatomy
```

투명 리소스는 `transparent background`만 믿고 승인하지 않는다. 실제 파일이 RGBA인지, 네 모서리 알파가 0인지, 가장자리에 흰색·크로마키 잔상이 없는지 확인한다.

## 10. Vue 적용 원칙

- 공통 컴포넌트가 리소스 경로와 상태 variant를 소유한다.
- 화면 CSS가 같은 역할의 아이콘을 새로 그리지 않는다.
- 대형 배경과 이야기 장면은 해당 라우트 또는 현재 상태에서 불러온다.
- 상태가 많은 리소스는 typed registry로 관리한다.
- `import.meta.glob(..., { eager: true })`는 작은 공통 세트 외에는 사용하지 않는다.
- 이미지 슬롯에 비율을 먼저 지정해 로딩 중 레이아웃이 움직이지 않게 한다.
- 목록 아래쪽과 아직 열지 않은 모달 이미지는 지연 로딩한다.

## 11. 미리보기와 화면 사용처 확인

[Frontend 에셋 인벤토리](frontend-asset-inventory.md)에서 현재 앱 리소스를 영역별 이미지 모음과 함께 확인한다. 각 파일 행은 다음 정보를 제공한다.

- 미리보기 모음의 식별 번호
- 앱에 포함된 실제 파일 경로
- 파일 용량과 픽셀 크기
- 아동에게 보이는 화면과 배치 위치
- 현재 리소스를 직접 참조하는 Vue, TypeScript 또는 CSS 파일
- mock·registry·repository를 거쳐 도달하는 최종 Vue 화면
- 유지, 최적화, 다듬기 등 현재 분류와 다음 검토

인벤토리 생성기는 일반 import와 CSS URL뿐 아니라 `import.meta.glob` 패턴 및 import 의존 경로를 추적한다. 여러 데이터 필드를 한꺼번에 노출하는 learner repository는 모듈 전체가 아니라 이야기 표지, 본문 장면, 이야기 친구별 실제 소비 화면을 기록한다.

`[TBD] 현재 src 코드 참조 없음`은 즉시 삭제한다는 뜻이 아니다. 현재 소스 번들에서 정적 import, CSS URL, `import.meta.glob` 연결을 찾지 못했다는 의미이며, API 응답이나 향후 콘텐츠 계약까지 확인한 뒤 실제 미사용 여부를 결정한다.

에셋을 추가·삭제하거나 경로를 바꾼 뒤 다음 명령으로 미리보기 모음과 사용처 표를 다시 만든다.

```powershell
python tools/audit_frontend_assets.py
```

## 12. 리소스 승인 체크

- [ ] 대표 화풍과 팔레트가 맞다.
- [ ] 작은 표시 크기에서도 역할이 구분된다.
- [ ] 손·눈·표정·글자 오류가 없다.
- [ ] 투명 배경이 실제 알파다.
- [ ] 캔버스와 기준점이 같은 상태 파일끼리 일치한다.
- [ ] 이미지에 불필요한 글자가 없다.
- [ ] 기존 공통 리소스와 중복되지 않는다.
- [ ] 앱 최종본의 픽셀 크기와 용량이 표시 용도에 맞다.
- [ ] 기본·호버·포커스·재생·선택 상태에서 잘리지 않는다.
- [ ] `1280×720`과 `1920×1080`에서 확인했다.
