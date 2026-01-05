# 원료생산팀 근무계획표 - 회사 PC 배포 가이드

> **중요**: 이 문서는 Antigravity AI에게 제공하여 **순차적으로 모든 작업을 자동화**하기 위한 완전한 가이드입니다.

---

## 📋 프로젝트 개요

### 완료된 작업 (Mac에서)
- ✅ Firebase 기반 실시간 근무 스케줄 관리 시스템 개발
- ✅ 하드코딩된 설정 데이터를 Firebase로 이관 (공휴일, 팀원, 시스템 설정)
- ✅ 2-File 구조: 사용자용(index.html) + 관리자용(manager.html)
- ✅ GitHub 리포지토리 생성 및 푸시
- ✅ Cloudflare Pages 배포 성공
- ✅ 테스트 완료

### 회사 PC에서 진행할 작업
- 🎯 기존 하드코딩된 회사 버전을 **완전히 새로운 Firebase 버전으로 교체**
- 🎯 Windows 환경 + Z: 드라이브 (네트워크 공유 폴더)에서 작업
- 🎯 실전용 Firebase 설정 (테스트 모드 아님, 보안 규칙 적용)
- 🎯 GitHub 리포지토리 완전 초기화 후 재배포
- 🎯 Cloudflare Pages 배포

---

## 🚨 Antigravity AI에게 전달할 지시사항

### **필수 규칙**
```
[중요] Antigravity는 반드시 한글로 모든 응답과 메시지를 작성해야 합니다.
코드 주석, 커밋 메시지, 문서, 사용자 대화 모두 한글을 사용하세요.
영어는 변수명, 함수명, 코드 자체에만 사용하고, 설명은 무조건 한글입니다.
```

---

## 📍 1단계: 환경 확인 및 준비

### 1.1 작업 디렉토리 확인
```powershell
# Windows PowerShell 또는 CMD에서 실행
# Z: 드라이브가 네트워크 드라이브로 연결되어 있는지 확인
cd Z:\원료생산팀\근무계획표
# 또는
cd Z:\your-folder-path
```

**Antigravity 태스크:**
```
현재 작업 디렉토리를 확인하고, 기존 파일 목록을 보여주세요.
만약 오래된 버전의 HTML 파일들이 있다면 백업 폴더를 만들어 이동시켜주세요.
```

### 1.2 필요한 도구 확인
- Git (설치 여부 확인: `git --version`)
- 브라우저 (Chrome, Edge 등)
- 인터넷 연결

**Antigravity 태스크:**
```
Git이 설치되어 있는지 확인하세요. 
설치되어 있지 않으면 사용자에게 설치를 요청하세요.
```

---

## 🔥 2단계: Firebase 프로젝트 설정 (**실전용**)

### 2.1 Firebase Console 접속
1. https://console.firebase.google.com/ 접속
2. 회사 Google 계정으로 로그인
3. **"프로젝트 추가"** 클릭

### 2.2 프로젝트 생성
- **프로젝트 이름**: `production-roster` (또는 회사 선호 이름)
- **Google Analytics**: 선택사항
- **"프로젝트 만들기"** 클릭

### 2.3 Firestore Database 생성 (**실전 모드**)

> **중요**: 테스트 모드가 아닌 실전 모드로 설정합니다.

1. 왼쪽 메뉴 → **"Firestore Database"** 클릭
2. **"데이터베이스 만들기"** 클릭
3. 모드 선택: **"프로덕션 모드"** 선택 (테스트 모드 아님!)
4. 위치: **`asia-northeast3 (Seoul)`** 선택
5. **"사용 설정"** 클릭

### 2.4 보안 규칙 설정

Firestore 생성 후 즉시 보안 규칙 탭으로 이동:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Config 데이터: 읽기는 누구나, 쓰기는 인증된 사용자만
    match /artifacts/production-roster-2026/config/{document=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    
    // Roster 데이터: 인증된 사용자만 읽기/쓰기
    match /artifacts/production-roster-2026/data/{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

**"게시"** 버튼 클릭하여 적용

### 2.5 Authentication 활성화

1. 왼쪽 메뉴 → **"Authentication"** 클릭
2. **"시작하기"** 클릭
3. **"Sign-in method"** 탭
4. **"익명"** 선택 → **"사용 설정"** → **"저장"**

### 2.6 Firebase API 키 발급

1. 프로젝트 설정 (⚙️) → **"프로젝트 설정"** 클릭
2. 아래로 스크롤 → **"내 앱"** 섹션
3. 웹 아이콘 (`</>`) 클릭
4. **앱 닉네임**: `roster-web` 입력
5. **"앱 등록"** 클릭
6. **Firebase SDK 구성** 정보 복사:

```javascript
const firebaseConfig = {
  apiKey: "...",
  authDomain: "...",
  projectId: "...",
  storageBucket: "...",
  messagingSenderId: "...",
  appId: "..."
};
```

**➡️ 이 정보를 메모장에 복사해두세요!**

---

## 📁 3단계: 파일 준비

### 3.1 원본 파일 가져오기

**옵션 A: 이전 성공한 Mac 버전 다운로드**
```
GitHub: https://github.com/kim-dohoon/introjo-roster
"Code" → "Download ZIP" 클릭
Z: 드라이브에 압축 해제
```

**옵션 B: Antigravity가 처음부터 생성**

**Antigravity 태스크:**
```
다음 파일들을 생성해주세요:

1. index.html - 사용자용 앱
   - Firebase 실시간 동기화
   - 근무 스케줄 조회 (캘린더/팀별/상세)
   - 특근/연차 입력
   - 데이터 백업 다운로드
   - 하드코딩 없이 모든 설정을 Firebase에서 로드

2. manager.html - 관리자용 앱
   - 팀 구성원 CRUD
   - 공휴일 관리 (연도별)
   - 시스템 설정 (기준일, 근무시간)
   - 데이터 백업/복원

3. migrate-config.html - 초기 데이터 마이그레이션
   - 하드코딩된 초기 데이터를 Firebase에 업로드
   - 공휴일 (2025-2030)
   - 팀 구성원 (A조, B조, C조, 주간조)
   - 근무 유형 정의
   - 출근 유형 옵션
   - 시스템 설정

4. .gitignore
5. README.md
6. config-structure.md

**중요**: 
- Firestore 경로는 4 segments로: artifacts/appId/config/docName
- 5 segments는 오류 발생 (artifacts/appId/public/config/docName ❌)
- appId = 'production-roster-2026'
```

### 3.2 Firebase API 키 적용

**Antigravity 태스크:**
```
사용자가 제공한 Firebase config 정보를 다음 3개 파일에 적용해주세요:
- index.html
- manager.html  
- migrate-config.html

모두 동일한 Firebase config를 사용합니다.
```

---

## 💾 4단계: Git 리포지토리 완전 초기화

### 4.1 기존 GitHub 리포지토리 내용 삭제

**방법 1: GitHub 웹에서 삭제 (권장)**
1. https://github.com/kim-dohoon/introjo-roster 접속
2. Settings → 맨 아래 "Delete this repository"
3. 리포지토리 이름 입력하여 확인
4. 새로 생성: https://github.com/new
   - Repository name: `introjo-roster` (또는 `company-roster`)
   - Visibility: Private 권장
   - **Initialize this repository 체크 해제**

**방법 2: 로컬에서 완전 초기화**

**Antigravity 태스크:**
```
다음 명령을 순서대로 실행해주세요:

1. 기존 .git 폴더 삭제
2. Git 새로 초기화: git init
3. .gitignore 생성
4. 모든 파일 스테이징: git add .
5. 초기 커밋:
   git commit -m "Initial commit: 원료생산팀 근무계획표 (실전 배포용)
   
   - Firebase 기반 실시간 동기화
   - 2-File 구조 (사용자/관리자)
   - 하드코딩 제거, 모든 설정 Firebase 관리
   - 보안 규칙 적용 (프로덕션 모드)"
```

### 4.2 GitHub 원격 저장소 연결

**Antigravity 태스크:**
```
사용자에게 GitHub 리포지토리 URL을 요청하세요.
받은 URL로 다음 명령 실행:

git remote add origin <사용자가 제공한 URL>
git branch -M main
git push -u origin main

만약 오류가 발생하면:
git push -u origin main --force
```

---

## ☁️ 5단계: Cloudflare Pages 배포

### 5.1 Cloudflare Pages 설정

**사용자 직접 작업:**

1. https://dash.cloudflare.com/ 로그인
2. 왼쪽 메뉴 → **"Pages"** 클릭
3. **"Create a project"** 클릭
4. **"Connect to Git"** 선택
5. GitHub 계정 연결 (처음이면 승인)
6. 리포지토리 선택: `introjo-roster` (또는 새로 만든 이름)
7. **"Begin setup"** 클릭

### 5.2 빌드 설정

| 항목 | 값 |
|------|-----|
| **Project name** | `company-roster` (원하는 이름) |
| **Production branch** | `main` (또는 `master`) |
| **Build command** | **(비워두기)** |
| **Build output directory** | `/` |

8. **"Save and Deploy"** 클릭

### 5.3 배포 완료 대기

- 1-2분 소요
- 완료되면 URL 생성: `https://company-roster.pages.dev`

---

## 🚀 6단계: 초기 데이터 마이그레이션

### 6.1 마이그레이션 스크립트 실행

배포 완료 후:

```
https://company-roster.pages.dev/migrate-config.html
```

1. 위 URL 브라우저에서 접속
2. **"🚀 마이그레이션 시작"** 버튼 클릭
3. 로그 확인:
   - ✅ Firebase 인증 완료
   - ✅ 공휴일 데이터 업로드 완료
   - ✅ 팀 구성원 데이터 업로드 완료
   - ✅ 근무 유형 데이터 업로드 완료
   - ✅ 출근 유형 옵션 업로드 완료
   - ✅ 시스템 설정 업로드 완료
   - 🎉 **모든 설정 데이터 마이그레이션 완료!**

### 6.2 Firebase에서 데이터 확인

Firebase Console → Firestore Database에서 확인:
```
artifacts/
  └── production-roster-2026/
      └── config/
          ├── holidays
          ├── teamMembers
          ├── shiftTypes
          ├── attendanceOptions
          └── systemSettings
```

---

## ✅ 7단계: 동작 검증

### 7.1 사용자 앱 테스트

```
https://company-roster.pages.dev/
```

**확인 사항:**
- [ ] [LIVE] 배지 표시됨
- [ ] 공휴일이 빨간색으로 표시됨
- [ ] 팀원 이름이 자동으로 채워짐
- [ ] 월간 캘린더 정상 작동
- [ ] 근무조별 입력 기능 작동
- [ ] 전체 상세 보기 작동
- [ ] 데이터 다운로드 버튼 작동

### 7.2 관리자 앱 테스트

```
https://company-roster.pages.dev/manager.html
```

**확인 사항:**
- [ ] 팀 관리 → 구성원 추가/수정/삭제 가능
- [ ] 공휴일 관리 → 연도별 공휴일 추가/수정 가능
- [ ] 시스템 설정 → 기준일, 근무시간 변경 가능
- [ ] 백업 다운로드 작동
- [ ] 복원 기능 작동

### 7.3 실시간 동기화 테스트

1. PC에서 manager.html 열기
2. 모바일에서 index.html 열기
3. PC에서 팀원 이름 변경
4. 모바일에서 즉시 반영되는지 확인

### 7.4 보안 규칙 검증

브라우저 콘솔(F12)에서:
- 인증 전: config 읽기 ✅, roster 읽기 ❌
- 인증 후: 모두 가능 ✅

---

## 📱 8단계: 로컬 네트워크 공유 (선택)

### 8.1 Z: 드라이브에 바로가기 생성

**Antigravity 태스크:**
```
Z: 드라이브의 공유 폴더에 다음 파일들을 복사해주세요:
- index.html (사용자용)
- manager.html (관리자용 - 관리자 PC에만)

사용자가 접근하기 쉽게 README.txt 파일도 생성해주세요:
- 사용 방법 안내
- 웹 URL: https://company-roster.pages.dev
- 로컬 파일 경로 안내
```

### 8.2 사용자 안내

직원들에게 다음 정보 제공:
```
📌 근무계획표 접속 방법

웹 (권장):
https://company-roster.pages.dev

로컬 파일:
Z:\원료생산팀\근무계획표\index.html

관리자만:
Z:\원료생산팀\근무계획표\manager.html
```

---

## 🔧 9단계: 추가 설정 (선택)

### 9.1 커스텀 도메인 (Cloudflare Pages)

회사 도메인이 있다면:
```
roster.company.com
```

Cloudflare Pages → Custom domains → "Set up a custom domain"

### 9.2 관리자 접근 제한

**옵션 1: Cloudflare Access**
- Zero Trust → Access → Applications
- manager.html에 이메일 인증 추가

**옵션 2: 파일 분리**
- manager.html을 GitHub에서 제외
- 로컬 Z: 드라이브에만 보관

---

## 🆘 문제 해결

### Firebase 연결 안 됨
1. Firebase API 키 확인
2. Authentication 익명 인증 활성화 확인
3. 브라우저 콘솔(F12) 에러 확인

### 마이그레이션 오류
1. Firestore 보안 규칙 확인 (익명 인증 허용 여부)
2. 경로 확인 (4 segments: artifacts/appId/config/docName)

### 데이터 저장 안 됨
1. 보안 규칙 확인
2. 익명 인증이 되었는지 확인 ([LIVE] 배지)

### Cloudflare 배포 실패
1. GitHub 리포지토리 public/private 확인
2. Build command 비워두었는지 확인
3. Build output directory = `/` 확인

---

## 📋 Antigravity 전체 태스크 체크리스트

**Antigravity에게 제공할 때 사용할 체크리스트:**

```markdown
# 원료생산팀 근무계획표 - Windows PC 배포 자동화

## [중요] 한글 사용 규칙
- 모든 사용자 대화, 설명, 주석, 커밋 메시지는 **반드시 한글**로 작성
- 영어는 변수명, 함수명, 코드 키워드에만 사용
- 사용자에게 질문할 때도 한글 사용

## 작업 순서

### 1단계: 환경 확인
- [ ] 현재 작업 디렉토리 확인 (Z: 드라이브)
- [ ] 기존 파일 백업 (backup 폴더 생성)
- [ ] Git 설치 확인

### 2단계: Firebase 설정 확인
- [ ] 사용자에게 Firebase config 정보 요청
- [ ] Firebase config 정보 검증

### 3단계: 파일 생성
- [ ] index.html 생성 (하드코딩 없이 Firebase 로드)
- [ ] manager.html 생성 (CRUD 기능)
- [ ] migrate-config.html 생성 (초기 데이터)
- [ ] .gitignore 생성
- [ ] README.md 생성
- [ ] config-structure.md 생성
- [ ] 모든 파일에 Firebase config 적용

### 4단계: Git 초기화
- [ ] 기존 .git 폴더 삭제 (있다면)
- [ ] git init
- [ ] git add .
- [ ] git commit -m "Initial commit: 원료생산팀 근무계획표 (실전 배포용)"

### 5단계: GitHub 푸시
- [ ] 사용자에게 GitHub 리포지토리 URL 요청
- [ ] git remote add origin <URL>
- [ ] git branch -M main
- [ ] git push -u origin main --force

### 6단계: Cloudflare Pages 가이드
- [ ] 사용자에게 Cloudflare Pages 배포 가이드 제공
- [ ] 배포 완료 대기

### 7단계: 검증 지원
- [ ] 마이그레이션 URL 안내
- [ ] 테스트 체크리스트 제공
- [ ] 문제 발생 시 디버깅 지원

### 8단계: 문서화
- [ ] 사용자 가이드 생성
- [ ] Z: 드라이브에 복사본 저장
- [ ] 직원 안내문 생성
```

---

## 🎯 최종 결과물

배포 완료 후 다음이 작동해야 합니다:

✅ **웹 앱**: https://company-roster.pages.dev/
- 어디서든 접속 가능
- 실시간 동기화
- 모바일/PC 모두 작동

✅ **로컬 파일**: Z:\원료생산팀\근무계획표\index.html
- 사내 네트워크에서 파일로 직접 접속
- 동일한 Firebase 데이터 사용

✅ **관리자 앱**: manager.html
- 설정 관리
- 팀원, 공휴일 수정
- 데이터 백업

✅ **보안**:
- Firestore 프로덕션 모드
- 보안 규칙 적용
- 익명 인증

---

## 💡 핵심 체크포인트

1. **Firestore 경로**: 반드시 4 segments (artifacts/appId/config/docName)
2. **보안 규칙**: 프로덕션 모드 + 인증 기반 접근 제어
3. **Firebase config**: 3개 HTML 파일 모두 동일한 config 사용
4. **Git 초기화**: 기존 내용 완전 삭제 후 새로 시작
5. **한글 사용**: Antigravity는 모든 응답을 한글로

---

## 📞 지원

이 문서를 Antigravity에게 제공하면:
1. 순차적으로 모든 작업 진행
2. 각 단계마다 확인 요청
3. 한글로 명확하게 소통
4. 문제 발생 시 즉시 디버깅

**성공을 기원합니다!** 🚀
