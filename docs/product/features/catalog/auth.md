---
type: Feature Catalog
title: "기능 카탈로그: auth"
description: "auth 도메인의 기능 식별자, 설명과 API 관계를 정리합니다."
tags: [feature, catalog, auth]
timestamp: 2026-07-27T12:19:48+09:00
---
# 기능 카탈로그: auth

| 기능 ID | 기능 | 설명 | 책임 | API operationId |
| --- | --- | --- | --- | --- |
| AU-ADM-REF-01 | 관리자 앱 인증 토큰 갱신 | 관리자 앱의 유효한 refresh token을 검증하고 세션을 회전한 뒤 새 access token을 발급한다. | server | `post_auth_admin_refresh` |
| AU-APP-OUT-01 | 학습 앱 로그아웃 처리 | 현재 학습 앱 access token과 refresh session을 폐기하고 학습용 인증 쿠키를 만료시킨다. | server | `post_auth_app_logout` |
| AU-APP-REF-01 | 학습 앱 인증 토큰 갱신 | 학습 앱의 유효한 refresh token을 검증하고 세션을 회전한 뒤 새 access token을 발급한다. | server | `post_auth_app_refresh` |
| LG-01 | 교수자 아이디 입력 | 교수자가 로그인에 사용할 아이디를 입력한다. | server | `post_auth_admin_login` |
| LG-02 | 교수자 비밀번호 입력 | 교수자가 로그인에 사용할 비밀번호를 입력한다. | server | `post_auth_admin_login` |
| LG-03 | 교수자 아이디 입력값 검증 | 아이디의 필수 입력 여부와 허용 문자 및 길이를 검증한다. | server | `post_auth_admin_login` |
| LG-04 | 교수자 비밀번호 입력값 검증 | 비밀번호의 필수 입력 여부와 허용 형식 및 길이를 검증한다. | server | `post_auth_admin_login` |
| LG-05 | 교수자 로그인 인증 | 입력한 아이디와 비밀번호로 교수자 인증을 요청한다. | server | `post_auth_admin_login` |
| LG-06 | 교수자 로그인 성공 처리 | 인증에 성공하면 교수자 세션을 생성하고 대시보드 화면으로 이동한다. | server | `post_auth_admin_login` |
| LG-07 | 교수자 로그인 실패 처리 | 교수자 인증에 실패하면 구체적인 원인을 구분하지 않고 오류를 표시한 뒤 로그인을 중단한다. | server | `post_auth_admin_login` |
| LG-13 | 비밀번호 표시 상태 전환 | 교수자가 입력한 비밀번호의 표시와 숨김 상태를 전환한다. | server | `post_auth_admin_login` |
| LG-ID-01 | 교수자 아이디 찾기 | 교수자가 이름과 회원가입 시 등록한 이메일을 입력해 본인 확인을 요청하고, 일치하는 계정의 마스킹된 아이디를 확인한다. | server | `post_auth_admin_find_id` |
| LG-ID-02 | 아이디 찾기 본인 확인 정보 입력 | 교수자가 아이디 찾기를 위해 이름과 회원가입 시 등록한 이메일을 필수 입력한다. | server | `post_auth_admin_find_id` |
| LG-ID-03 | 아이디 찾기 결과 표시 | 본인 확인 정보가 일치하면 마스킹된 아이디와 로그인·비밀번호 재설정 이동 수단을 표시한다. | server | `post_auth_admin_find_id` |
| LG-PW-01 | 교수자 비밀번호 재설정 | 교수자가 아이디와 회원가입 시 등록한 이메일로 본인 확인 후 새 비밀번호와 비밀번호 확인을 입력해 비밀번호를 재설정한다. | server | `post_auth_admin_password_reset` |
| LG-PW-02 | 비밀번호 재설정 본인 확인 | 교수자가 아이디와 회원가입 시 등록한 이메일을 입력하면 새 비밀번호 설정 단계로 이동한다. | server | `post_auth_admin_password_reset` |
| LG-PW-03 | 새 비밀번호 입력값 검증 | 새 비밀번호가 8자 이상인지, 비밀번호 확인 값과 일치하는지 검증하고 오류 메시지를 표시한다. | server | `post_auth_admin_password_reset` |
| LG-PW-04 | 비밀번호 재설정 완료 처리 | 새 비밀번호 검증에 성공하면 변경 완료 상태와 로그인 화면 이동 수단을 표시한다. | server | `post_auth_admin_password_reset` |
| LG-STU-01 | 연결 아동 목록 표시 | 교수자 로그인 후 현재 교수자에게 연결된 아동의 프로필 사진과 이름을 선택 목록으로 표시한다. | server | `post_auth_app_teacher_login` |
| LG-STU-02 | 아동 프로필 선택 | 학습을 시작할 아동의 프로필 사진과 이름이 표시된 항목을 선택할 수 있도록 한다. | client | - |
| LG-STU-03 | 아동 선택값 검증 | 선택한 아동의 고유 식별자가 필수이며 허용된 형식인지 검증한다. | server | `post_auth_app_student_login` |
| LG-STU-04 | 연결 아동 식별 | 선택한 아동의 고유 식별자가 현재 교수자에게 연결된 아동인지 확인하여 대상을 식별한다. | server | `post_auth_app_student_login` |
| LG-STU-05 | 아동 로그인 실패 처리 | 선택한 아동이 현재 교수자에게 연결되어 있지 않거나 더 이상 조회할 수 없으면 오류를 표시하고 목록에서 다시 선택할 수 있도록 한다. | server | `post_auth_app_student_login` |
| LG-STU-06 | 아동 세션 생성 | 식별된 아동의 고유 식별 정보를 교수자 세션과 연결하여 아동 세션을 생성한다. | server | `post_auth_app_student_login` |
| LG-STU-07 | 아동 로그인 성공 처리 | 아동 세션 생성 후 해당 아동의 학습 앱 메인 화면으로 이동한다. | server | `post_auth_app_student_login` |
| LG-SU-01 | 교수자 회원가입 정보 입력 | 교수자가 아이디, 이메일, 비밀번호, 비밀번호 확인, 이름과 소속기관을 입력한다. | server | `post_auth_admin_sign_up` |
| LG-SU-02 | 교수자 회원가입 입력값 검증 | 모든 필수값의 입력 여부, 이메일 형식, 비밀번호 8자 이상 여부와 비밀번호 확인 일치 여부를 검증한다. | server | `post_auth_admin_sign_up` |
| LG-SU-03 | 교수자 회원가입 제출 | 교수자가 회원가입 버튼을 선택하면 입력값을 검증하고, 유효한 경우 회원가입 완료 흐름을 진행한다. | server | `post_auth_admin_sign_up` |
| LG-SU-04 | 교수자 회원가입 성공 처리 | 회원가입 입력값 검증을 통과하면 회원가입을 완료하고 로그인 화면으로 이동한다. | server | `post_auth_admin_sign_up` |
| LG-SU-05 | 교수자 회원가입 실패 처리 | 필수값 누락, 이메일 형식 오류, 비밀번호 길이 미달 또는 비밀번호 확인 불일치 시 제출을 중단하고 입력값을 수정할 수 있도록 안내한다. | server | `post_auth_admin_sign_up` |
| LG-TEA-01 | 교수자 아이디 입력 | 교수자가 로그인을 위한 아이디를 입력할 수 있도록 한다. | server | `post_auth_app_teacher_login` |
| LG-TEA-02 | 교수자 비밀번호 입력 | 교수자가 로그인을 위한 비밀번호를 입력할 수 있도록 한다. | server | `post_auth_app_teacher_login` |
| LG-TEA-03 | 교수자 로그인 입력값 검증 | 교수자 아이디와 비밀번호의 필수 입력 여부 및 허용 형식을 검증한다. | server | `post_auth_app_teacher_login` |
| LG-TEA-04 | 교수자 인증 | 입력한 아이디와 비밀번호로 교수자 인증을 요청한다. | server | `post_auth_app_teacher_login` |
| LG-TEA-05 | 교수자 세션 생성 | 인증된 교수자의 식별 정보와 권한을 포함한 교수자 세션을 생성하고 학습 앱에 전달한다. | server | `post_auth_app_teacher_login` |
| LG-TEA-06 | 교수자 로그인 성공 처리 | 교수자 세션 생성 후 연결 아동의 프로필 사진과 이름을 보여주는 아동 선택 화면을 표시한다. | server | `post_auth_app_teacher_login` |
| LG-TEA-07 | 교수자 로그인 실패 처리 | 교수자 인증 실패 사유를 표시하고 로그인 입력을 다시 수행할 수 있도록 한다. | server | `post_auth_app_teacher_login` |
| SB-COM-01 | 교수자 로그아웃 처리 | 현재 로그인한 교수자의 세션을 종료한다. | server | `post_auth_admin_logout` |

# Sources

[Notion 기능 명세](https://app.notion.com/p/de0027df905383e98fb00120c64321fc)
