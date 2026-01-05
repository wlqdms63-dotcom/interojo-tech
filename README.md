# 원료생산팀 설비운영 근무계획표 (Full Firebase Version)

본 프로젝트는 Firebase Firestore를 단일 데이터 소스(SSOT)로 사용하는 웹 기반 근무계획표 시스템입니다.
기존의 엑셀/파이썬 동기화 방식을 완전히 대체하며, 언제 어디서나 실시간으로 데이터를 관리할 수 있습니다.

## 🔗 주요 접속 주소
- **사용자용 (메인):** `https://interojo-tech.pages.dev`
- **관리자용 (설정):** `https://interojo-tech.pages.dev/manager` (또는 `/manager.html`)

## ✨ 주요 기능
1.  **실시간 동기화:** 사용자가 근무를 입력하면 즉시 모든 접속자에게 반영됩니다.
2.  **타임 락 (Time-Lock):** 지난 날짜의 근무표는 수정할 수 없도록 잠깁니다.
3.  **관리자 페이지:**
    -   **팀원 관리:** A, B, C, 주간조 인원을 자유롭게 추가/삭제/수정 가능.
    -   **공휴일 관리:** 공휴일 정보를 DB에 저장하여 달력에 빨간색으로 자동 표시.
4.  **자동 배포:** GitHub에 코드를 Push하면 Cloudflare Pages가 자동으로 배포합니다.

## 🛠️ 기술 스택
- **Frontend:** HTML5, Tailwind CSS, Vanilla JS (ES6 Modules)
- **Backend:** Firebase Firestore (NoSQL Database), Firebase Auth (Anonymous)
- **Deployment:** GitHub -> Cloudflare Pages

## 📂 프로젝트 구조
```
z:\interojo-sc\
├── index.html          # 메인 페이지 (달력, 근무 입력)
├── manager.html        # 관리자 페이지 (팀원, 공휴일 설정)
├── migrate-config.html # (초기설정용) 로컬 데이터를 DB로 업로드하는 도구
└── .firebase/          # Firebase 관련 설정 (자동생성)
```

## 🚀 배포 방법
수정 사항이 생기면 아래 명령어로 GitHub에 올리기만 하면 됩니다.
```powershell
git add .
git commit -m "수정 내용 설명"
git push
```
(약 1~2분 뒤 사이트에 자동 반영됨)

## ⚠️ 주의사항
- **Firebase Config:** `index.html`과 `manager.html`에는 Firebase 연결 정보(`apiKey` 등)가 포함되어 있습니다. 보안을 위해 이 코드는 GitHub Public 리포지토리에 올릴 때 주의가 필요합니다. (현재는 편의상 포함됨)
- **데이터 백업:** Firestore 데이터는 클라우드에 안전하게 저장되지만, 필요 시 `migrate-config.html`을 변형하여 백업 기능을 만들 수 있습니다.
