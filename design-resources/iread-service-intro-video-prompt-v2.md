# iRead 서비스 소개 영상 생성 프롬프트 v2

- 영상 길이: 약 75초
- 화면 비율: `16:9`, `1920×1080`, `24fps`
- 마스코트 이름: `토리(Tori)`
- 제작 방식: 생성 애니메이션 + 실제 서비스 화면 이미지 투 비디오 + 후반 합성
- 핵심 원칙: 실제 UI와 한글은 생성하지 않고 첨부 화면을 원본 그대로 사용한다.

## 1. 첨부 화면 사용표

| ID | 파일 | 영상 사용처 |
| --- | --- | --- |
| UI-01 | `dashboard.png` | 서비스 진입, 오늘의 목표, 성장 정원 |
| UI-02 | `글자연습_단계선택페이지.png` | 개인별 단계와 학습 경로 |
| UI-03 | `훈련_첫소리찾기.png` | 소리를 듣고 첫소리 선택 |
| UI-04 | `훈련_소리합치기.png` | 음절·소리 합치기 |
| UI-05 | `훈련_글자자르기.png` | 글자 구조 나누기 |
| UI-06 | `훈련_문장만들기.png` | 낱말 카드로 문장 만들기 |
| UI-07 | `훈련_그림보고문장맞추기.png` | 그림에 맞는 문장 선택 |
| UI-08 | `이야기나라.png` | 이야기 읽기 경험 |
| UI-09 | `end페이지.png` | 최종 메시지와 엔딩 |

## 2. 제작 전 화면 정리

1. 아동 프로필명 `이서연`과 테스트 계정명 `sfds`는 사용 허가를 확인한다.
2. [TBD] 사용 허가가 없다면 영상 편집 단계에서 `아이리드 친구`처럼 중립적인 이름으로 교체하거나 프로필 영역을 블러 처리한다.
3. `end페이지.png`는 브라우저의 흰 여백과 오른쪽 스크롤바를 제거하고 중앙의 엔딩 카드만 크롭한다.
4. 모든 서비스 화면은 약 `1.596:1`이므로 `16:9`로 늘리지 않는다. `1920×1080` 캔버스에서 높이에 맞춰 배치하고 좌우 여백은 브랜드 하늘색 또는 화면 배경을 확장한 정지 이미지로 채운다.
5. 화면 속 토리를 직접 생성형 영상으로 변형하지 않는다. 움직임이 필요하면 동일한 투명 PNG 토리를 별도 레이어로 올려 `2~3%` 상하 이동, 눈 깜박임, 한 번의 손 흔들기처럼 제한된 2D 모션만 적용한다.

## 3. 생성 애니메이션 공통 스타일 프롬프트

아동과 토리를 새로 연출하는 장면 1, 2, 8에 사용한다.

```text
Create a warm, polished animated introduction film for iRead, a Korean personalized reading-training and learning-support service for lower-elementary children.

Use the provided Tori rabbit reference image as the exact and consistent character reference in every generated shot.

Tori is a bright pink child-friendly rabbit mascot with a simple rounded silhouette, one upright ear and one gently bent ear, large oval black eyes, a white muzzle, a small red nose, pink cheeks, short rounded limbs, and a warm expressive face.

Preserve Tori's exact identity throughout the film: identical body proportions, face shape, facial features, ear shapes and orientation, pink-white-red color palette, eye size and placement, and limb proportions. Do not redesign, accessorize, age, recolor, or reinterpret Tori.

Tori behaves like a friendly reading companion: encouraging, curious, playful, patient, and supportive. Tori never evaluates, pressures, or judges the child.

Visual style: high-saturation 2D flat vector animation, modern Korean children's picture-book aesthetic, rounded solid shapes, large readable color areas, minimal internal lines, one or two soft cel-shading steps, cream-colored learning surfaces, vivid sky blue, fresh green, orange, purple, coral, and pink accents.

Tone: reassuring, playful, respectful, hopeful, and emotionally warm. Never clinical, frightening, competitive, or stigmatizing. Portray the child as curious, capable, and actively participating.

Animation direction: gentle camera movement, one primary action per shot, clear visual hierarchy, subtle parallax, smooth page-turn transitions, natural anticipation and follow-through, no chaotic movement.

Maintain the same child design and the same Tori design across every generated scene.

16:9 landscape, 1920x1080, 24 fps, polished commercial-quality children's animation. Reserve clean negative space for Korean captions added during post-production.

Do not generate final Korean captions, logos, watermarks, subtitles, or service UI.
```

## 4. 실제 서비스 화면 공통 잠금 프롬프트

장면 3~7과 실제 화면이 합성되는 장면 8, 9에 반복해서 사용한다.

```text
EXACT UI REFERENCE LOCK:
Use the attached iRead service screenshot as the exact immutable base plate.
Do not redraw, recreate, reinterpret, restyle, or regenerate the interface.
Preserve every existing Korean character, word, number, logo, icon, card, button, illustration, color, spacing, and layout exactly as shown in the source image.

The source screenshot must remain geometrically stable and readable in every frame.
No text morphing, no letter replacement, no random characters, no icon drift, no duplicated controls, no warped cards, and no changing progress values.

Animate only the explicitly requested elements through rigid 2D layers, masks, highlights, or camera transforms. Do not apply generative deformation to the UI.

Use a slow controlled push-in between 100% and 104% scale, or a gentle pan of less than 5% of the frame. Never stretch the original screenshot to 16:9. Fit it by height and fill the narrow side margins with a clean iRead sky-blue background.

Keep the Tori mascot already visible in the screenshot exactly unchanged. If Tori needs motion, use a separately composited exact Tori cutout instead of regenerating the mascot.
```

## 5. 75초 장면별 프롬프트

### Scene 1 — 아이마다 다른 읽기의 속도

- 길이: 7초
- 유형: 생성 애니메이션
- 화면 문구: `아이마다 다른 읽기의 속도`

```text
A Korean lower-elementary child sits at a warm wooden desk with an open illustrated picture book. The child pauses thoughtfully while reading and gently traces one reading line with a finger, spending a little more time on one character.

The child's expression shows concentration and curiosity, never sadness, fear, embarrassment, or frustration. Soft morning sunlight, calm room, safe and supportive atmosphere. Use a very slow cinematic push-in and subtle natural page movement. Leave clean negative space for a Korean caption added in post-production.
```

### Scene 2 — 토리의 등장

- 길이: 7초
- 유형: 생성 애니메이션
- 화면 문구: `안녕! 나는 토리야`

```text
Tori, matching the exact provided mascot reference, gently peeks out from behind a colorful bookmark inside the open book. Tori softly hops onto the desk, sits beside the book, smiles warmly, and waves once. Tori points toward the next reading area with a small encouraging gesture.

The child notices Tori, relaxes, and smiles gently. Use only one subtle sparkle accent. End with a clean page-turn transition into the iRead service screen. Keep Tori perfectly consistent with the reference image.
```

### Scene 3 — 나에게 맞는 iRead 읽기 여행

- 길이: 9초
- 유형: 실제 화면 이미지 투 비디오
- 소스: UI-01 `dashboard.png` 4초 → UI-02 `글자연습_단계선택페이지.png` 5초
- 화면 문구: `나에게 맞는 읽기 여행, iRead`

#### Scene 3A — 대시보드

```text
Use dashboard.png as the exact immutable base plate and apply the EXACT UI REFERENCE LOCK.

Begin with the full dashboard visible. Add a very slow 3% push-in toward the left-side "오늘의 목표" panel, then guide attention toward the three flower beds using a soft warm glow that travels once from left to right. Keep every label, progress bar, flower, house, icon, logo, and Korean text unchanged.

Do not animate the existing UI text. Add only subtle leaf sway and one gentle Tori blink through separate composited layers.
```

#### Scene 3B — 글자연습 단계 선택

```text
Use 글자연습_단계선택페이지.png as the exact immutable base plate and apply the EXACT UI REFERENCE LOCK.

Transition from the dashboard with a soft page turn. Keep the full learning path readable. Add a small warm highlight around the active blue stage marked 2, followed by a restrained dotted-path light moving toward the next stage. Do not change the stage numbers, Korean labels, progress value, date, or locked-stage appearance.

The Tori figure on the active stage remains exact and may perform only a subtle 2% bounce as a separately composited rigid layer.
```

### Scene 4 — 소리를 듣고 글자를 익혀요

- 길이: 11초
- 유형: 실제 화면 몽타주
- 소스: UI-03 3.5초 → UI-04 3.5초 → UI-05 4초
- 화면 문구: `소리부터 글자까지`

#### Scene 4A — 첫소리 찾기

```text
Use 훈련_첫소리찾기.png as the exact immutable base plate and apply the EXACT UI REFERENCE LOCK.

Add one soft pulse around the coral sound button. After the pulse, add a thin warm highlight around the yellow first-sound card as a separate overlay. Do not move or regenerate any Korean letter. Keep the title, progress dots, arrows, cards, logo, and Tori unchanged and fully readable.
```

#### Scene 4B — 소리 합치기

```text
Use 훈련_소리합치기.png as the exact immutable base plate and apply the EXACT UI REFERENCE LOCK.

Add a subtle listening pulse around the sound button, followed by a clean left-to-right motion cue across the existing equation area. Briefly highlight the two choice cards one at a time. All Korean letters and numbers must remain fixed. Do not fabricate a result, alter the question mark, or change the progress state.
```

#### Scene 4C — 글자 자르기

```text
Use 훈련_글자자르기.png as the exact immutable base plate and apply the EXACT UI REFERENCE LOCK.

Use a gentle 3% push-in toward the puzzle-shaped syllable pieces. Add one restrained outline sweep around the puzzle edges to explain that a word can be divided into smaller sound units. Keep every puzzle piece, Korean character, button, title, progress indicator, and Tori exactly unchanged. Do not cut, morph, or regenerate the Korean text itself.
```

### Scene 5 — 글자에서 문장으로

- 길이: 10초
- 유형: 실제 화면 몽타주
- 소스: UI-06 5초 → UI-07 5초
- 화면 문구: `글자에서 문장까지`

#### Scene 5A — 문장 만들기

```text
Use 훈련_문장만들기.png as the exact immutable base plate and apply the EXACT UI REFERENCE LOCK.

Keep the screenshot fixed. Using a separately cut rigid card layer, move the existing "사과를" card smoothly into the middle sentence slot without changing a single Korean character or the card design. Add a very small snap-in scale response, then hold the completed placement. Do not regenerate the sentence cards or invent new text.
```

#### Scene 5B — 그림 보고 문장 맞추기

```text
Use 훈련_그림보고문장맞추기.png as the exact immutable base plate and apply the EXACT UI REFERENCE LOCK.

Use a slow 2% push-in that keeps both the rabbit illustration and the three sentence options visible. Add a soft golden outline around the first existing sentence card, "토끼가 들판을 달린다.", followed by one small confirmation sparkle. Do not modify the illustration, the three Korean sentences, the title, the progress indicator, or the mascot.
```

### Scene 6 — 이야기를 읽는 즐거움

- 길이: 9초
- 유형: 실제 화면 이미지 투 비디오
- 소스: UI-08 `이야기나라.png`
- 화면 문구: `이야기 속에서 이어지는 읽기`

```text
Use 이야기나라.png as the exact immutable base plate and apply the EXACT UI REFERENCE LOCK.

Begin with the full story-reading screen. Apply a slow 3% push-in toward the illustrated rabbit and turtle while keeping all three Korean reading lines visible. Add a low-opacity reading guide that travels once from left to right beneath one existing line without covering the text. Add very subtle leaf motion inside the illustration only through a masked overlay.

Keep the story text, navigation buttons, logo, background blocks, and book-holding Tori exactly unchanged. Do not generate a different story scene or replace any Korean sentence.
```

### Scene 7 — 오늘의 한 걸음이 모여

- 길이: 9초
- 유형: 실제 화면 이미지 투 비디오
- 소스: UI-01 `dashboard.png`
- 화면 문구: `오늘의 한 걸음이 모여`

```text
Use dashboard.png as the exact immutable base plate and apply the EXACT UI REFERENCE LOCK.

Start focused on the small sprouts in the right flower bed, then make a slow horizontal camera move across the yellow and pink flower beds. Add only subtle leaf sway, one or two tiny star particles, and a gentle glow across the existing progress bars. Do not add new flowers that cover labels or change the recorded progress values.

End with the full garden visible and Tori giving one small wave through a separately composited exact cutout. Preserve all Korean labels and UI elements.
```

### Scene 8 — 함께 이해하는 성장 기록

- 길이: 8초
- 유형: 생성 애니메이션 + 실제 화면 합성
- 합성 소스: UI-01 `dashboard.png`
- 화면 문구: `함께 이해하는 성장 기록`

```text
Show a Korean parent and a literacy education professional sitting together in a calm, bright, non-clinical environment. They look at a tablet and discuss the child's learning journey calmly and collaboratively.

The tablet display must be replaced in post-production with the exact provided dashboard.png screenshot. During generation, keep the tablet screen as a flat, blank, perspective-stable green or neutral tracking surface with no generated interface, no text, and no reflections covering the display.

Use a gentle over-the-shoulder camera angle that clearly shows the tablet area. The adults' expressions communicate shared understanding and thoughtful next-step planning, not diagnosis or evaluation. Tori may appear as a small exact sticker or desk figure only if composited from the provided reference after generation.
```

후반 합성 지시:

```text
Corner-pin dashboard.png onto the tablet tracking surface. Preserve the original aspect ratio and every UI detail. Do not regenerate the dashboard. Add a subtle screen reflection at less than 8% opacity only after the UI replacement is complete.
```

### Scene 9 — 엔딩

- 길이: 5초
- 유형: 실제 화면 이미지 투 비디오
- 소스: UI-09 `end페이지.png` 중앙 카드 크롭본
- 기존 카드 문구를 최종 메시지로 사용하고 별도의 큰 문구는 중복 삽입하지 않는다.

```text
Use the cropped central ending card from end페이지.png as the exact immutable base plate and apply the EXACT UI REFERENCE LOCK.

Remove the browser white margins and scrollbar before animation. Preserve the existing Korean headline, subtitle, books, flowers, clouds, stars, and both Tori illustrations exactly as shown.

Apply a very slow 2% push-in. Add only a soft star shimmer and subtle page movement to the open books through separate masked overlays. Do not change, regenerate, or retype the existing Korean text. End on a clean still frame long enough for the message to be read.

Add the legal notice only in post-production as a small accessible caption below the existing card text. Do not ask the generation model to render it.
```

## 6. 장면 전환

- Scene 1 → 2: 책갈피 뒤에서 토리가 등장한다.
- Scene 2 → 3: 책장이 넘어가며 `dashboard.png`로 전환한다.
- UI 화면 사이: `6~10프레임`의 짧은 페이지 넘김 또는 같은 방향의 카드 슬라이드만 사용한다.
- Scene 5 → 6: 문장 카드가 책의 한 페이지가 되어 이야기 나라 화면으로 이어진다.
- Scene 6 → 7: 이야기 화면의 나뭇잎 하나가 성장 정원의 잎으로 매치 컷된다.
- Scene 7 → 8: 성장 정원 화면이 태블릿 화면 안으로 축소된다.
- Scene 8 → 9: 태블릿의 크림색 화면이 엔딩 카드의 크림색 배경으로 디졸브된다.

전환 중에도 실제 UI 텍스트에 모핑 효과를 적용하지 않는다.

## 7. 공통 네거티브 프롬프트

```text
No photorealism.
No realistic human photography.
No glossy 3D mascot or plastic toy render.
No watercolor or sketch texture.
No dark hospital environment.
No medical diagnosis imagery, brain scans, probability scores, or clinical dashboard.
No distressed, crying, embarrassed, or helpless child.
No disability stigma.
No threatening teacher.
No competitive ranking, leaderboard, punishment, harsh X marks, or red failure screen.
No generated service interface.
No recreated screenshot.
No altered UI layout.
No text morphing.
No corrupted Korean characters.
No random text.
No changed progress numbers.
No duplicated buttons or icons.
No warped cards.
No generated logo.
No watermark or subtitles.
No character redesign.
No inconsistent Tori design, ears, face, proportions, or colors.
No extra limbs, malformed eyes, duplicated characters, or broken anatomy.
No rapid flashing, shaky camera, aggressive zoom, or chaotic motion.
```

## 8. 캐릭터 일관성 강화 문구

```text
CRITICAL CHARACTER CONSISTENCY:
Tori must match the provided reference image exactly.
Do not reinterpret, redesign, age, recolor, accessorize, or change Tori.
Keep the exact same ear shapes, face, eyes, muzzle, nose, cheeks, body proportions, limb length, and color palette in every frame.
Treat Tori as one fixed animation-model character used consistently across all scenes.
```

## 9. UI 일관성 강화 문구

```text
CRITICAL SCREEN FIDELITY:
This is an image-to-video shot, not a UI redesign task.
The attached screenshot is the final approved interface and must remain pixel-faithful.
Freeze all Korean text, numbers, logos, icons, controls, cards, and layout.
Animate only camera position and explicitly isolated overlay layers.
If exact screen fidelity cannot be guaranteed, return a static shot rather than inventing or deforming interface details.
```

## 10. 75초 내레이션

| 시간 | 내레이션 |
| --- | --- |
| 0~7초 | “누군가에게는 자연스러운 읽기가, 어떤 아이에게는 조금 더 많은 시간과 용기가 필요합니다.” |
| 7~14초 | “그럴 때, 토리가 아이의 읽기 여정에 함께합니다.” |
| 14~23초 | “iRead는 읽기에 어려움을 겪을 수 있는 초등 저학년 아이를 위한 개인화 읽기 훈련 서비스입니다.” |
| 23~34초 | “아이는 소리를 듣고, 글자를 바라보고, 직접 선택하며 기초부터 한 단계씩 연습합니다.” |
| 34~44초 | “글자를 나누고 문장을 만들며, 자신에게 맞는 속도로 읽기의 폭을 넓혀갑니다.” |
| 44~53초 | “이야기 속에서는 문장을 따라 읽고, 다음 장면을 만나며 읽는 즐거움을 이어갑니다.” |
| 53~62초 | “학습이 쌓일수록 성장 정원은 꽃을 피우고, 오늘의 작은 노력을 눈에 보이게 보여줍니다.” |
| 62~70초 | “보호자와 전문가는 이 기록을 함께 살펴보며 다음 지원 방향을 고민할 수 있습니다.” |
| 70~75초 | “아이마다 다른 읽기의 속도. 토리와 함께, iRead.” |

## 11. 엔딩 고지

다음 문구를 생성 이미지가 아닌 편집 프로그램의 텍스트 레이어로 삽입한다.

```text
iRead는 교육용 읽기 훈련 및 학습 지원 시스템으로,
의료적 진단이나 치료를 제공하지 않습니다.
```

## 12. 음악과 효과음

- 글로켄슈필, 우쿨렐레, 가벼운 피아노 중심의 따뜻한 동화책 분위기
- 0~7초: 악기 수를 줄이고 책장과 손가락 움직임에 집중
- 7초: 토리 등장과 함께 글로켄슈필과 가벼운 리듬 추가
- 실제 훈련 화면: 클릭음보다 부드러운 `tap`, `page`, `soft chime` 계열 사용
- 이야기 나라: 작은 벨, 페이지 넘김, 낮은 음량의 마법 효과음
- 성장 정원: 화성과 악기 수를 가장 풍성하게 구성
- 70~75초: 리듬을 줄이고 피아노와 글로켄슈필의 짧은 프레이즈로 마무리
- 토리 동작: 가벼운 `hop`, `page flip`, `sparkle`만 사용하고 과도한 게임 보상음은 피한다.

## 13. 최종 편집 체크

- [ ] 모든 캐릭터명이 `토리`로 통일되었다.
- [ ] 생성 장면의 토리가 첨부 화면 속 토리와 같은 얼굴·귀·색·비율을 유지한다.
- [ ] 서비스 화면의 한글, 숫자, 로고와 버튼이 원본과 일치한다.
- [ ] 화면을 `16:9`로 강제 변형하지 않았다.
- [ ] 아동 이름과 테스트 계정명 사용 허가 또는 마스킹을 확인했다.
- [ ] `end페이지.png`의 브라우저 여백과 스크롤바를 제거했다.
- [ ] UI 화면에서 토리가 일그러지거나 새 캐릭터로 재생성되지 않았다.
- [ ] 보호자·전문가 장면의 태블릿에 실제 `dashboard.png`를 합성했다.
- [ ] 의료적 진단, 치료 효과 또는 개선 보장으로 오해될 표현이 없다.
- [ ] 엔딩 고지가 편집 텍스트로 선명하게 표시된다.
