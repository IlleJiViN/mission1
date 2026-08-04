# 📘 초보자를 위한 Git & GitHub 실습 가이드 (GIT_GUIDE.md)

이 가이드는 `quiz-game` 프로젝트를 진행하면서 버전 관리 시스템인 **Git**과 원격 저장소 **GitHub**를 사용하는 전체 흐름을 초보자가 따라할 수 있도록 설명합니다.

---

## 🛠️ 1. 초기 Git 설정 및 저장소 생성

프로젝트 디렉터리를 Git 저장소로 초기화하고 GitHub 원격 저장소에 첫 커밋을 올리는 순서입니다.

```bash
# 1. 프로젝트 폴더로 이동
cd quiz-game

# 2. Git 저장소 초기화
git init

# 3. 모든 파일을 스테이징 영역에 추가
git add .

# 4. 첫 번째 커밋 생성
git commit -m "Init: 퀴즈 게임 프로젝트 기본 구조 생성"

# 5. 기본 브랜치 이름을 main으로 변경
git branch -M main

# 6. GitHub 원격 저장소 연결 (저장소_URL을 본인 저장소주소로 변경)
git remote add origin https://github.com/username/quiz-game.git

# 7. 원격 저장소로 첫 푸시
git push -u origin main
```

---

## 📝 2. 기능별 커밋 이력 예시 (최소 10개 커밋)

프로젝트 개발 시 의미 있는 단위로 나누어 작성한 커밋 메시지 목록입니다.

```text
1. Init: 프로젝트 기본 구조 생성
2. Feat: 메인 메뉴와 대화형 입력 검증 구현
3. Feat: Quiz 클래스 데이터 구조 및 유효성 검사 구현
4. Data: Python, Git, JSON 기본 퀴즈 데이터 10종 추가
5. Refactor: QuizGame 클래스 구조 설계 및 파일 로딩 프레임워크 작성
6. Feat: 퀴즈 출제, 선택지 무작위 섞기 및 100점 환산 로직 구현
7. Feat: 사용자 정의 퀴즈 추가 및 즉시 파일 저장 구현
8. Feat: 전체 퀴즈 목록 상세 조회 기능 구현
9. Feat: 최고 점수 갱신 및 히스토리 관리 구현
10. Feat: state.json 저장 및 로딩 로직 작성
11. Fix: state.json 파손 시 백업 생성 및 자동 복구 기능 구현
12. Fix: Ctrl+C 및 EOFError 수신 시 안전 종료 처리
13. Test: 주요 입력 예외 상황 및 복구 수동 검증 완료
14. Docs: README 및 가이드 문서 작성
```

---

## 🌿 3. 기능 브랜치 생성 및 병합 (Branch & Merge)

퀴즈 출제 기능(`play_quiz`)은 별도의 독립된 브랜치(`feature/play-quiz`)에서 안전하게 개발한 뒤 `main` 브랜치로 병합합니다.

### 3-1. 브랜치 생성 및 이동
```bash
# feature/play-quiz 브랜치를 생성하고 해당 브랜치로 이동
git checkout -b feature/play-quiz
```

### 3-2. 기능 개발 후 커밋 및 푸시
```bash
# 변경된 소스코드 작업 후 스테이징
git add quiz_game.py

# 커밋 작성
git commit -m "Feat: 퀴즈 출제와 채점 기능 구현"

# 원격 저장소에 기능 브랜치 푸시
git push -u origin feature/play-quiz
```

### 3-3. main 브랜치로 이동 및 병합 (Merge)
```bash
# 메인 브랜치로 이동
git checkout main

# feature/play-quiz 브랜치를 --no-ff 옵션으로 병합 (병합 커밋 명시적 생성)
git merge --no-ff feature/play-quiz -m "Merge: feature/play-quiz 브랜치를 main에 병합"

# 병합된 main 브랜치를 GitHub에 푸시
git push origin main
```

> 💡 **`--no-ff` (No Fast-Forward) 옵션을 사용하는 이유**:
> Fast-Forward 병합 시 커밋 히스토리가 일직선으로 합쳐져 독립된 기능 개발 단위였음을 추적하기 어렵습니다. `--no-ff` 옵션을 사용하면 병합 그래프에 가지(Branch)와 병합 커밋(Merge Commit)이 명확히 남아 히스토리를 파악하기 유용합니다.

---

## 🔄 4. `git clone` 및 `git pull` 실습 Workflow

개발 완료 후 다른 컴퓨터나 다른 폴더에 저장소를 복제하고 동기화하는 과정입니다.

### 4-1. 다른 폴더에 저장소 복제 (Clone)
```bash
# 상위 디렉터리로 이동
cd ..

# 저장소 복제 (quiz-game-clone 폴더로 복제)
git clone https://github.com/username/quiz-game.git quiz-game-clone

# 복제된 폴더로 이동
cd quiz-game-clone
```

### 4-2. 복제한 저장소에서 수정 후 Push
```bash
# README.md 파일 수정 (예: 실습 확인 문구 추가)
echo "\n- clone 실습 확인 완료" >> README.md

# 커밋 및 원격 저장소 푸시
git add README.md
git commit -m "Docs: clone 실습 확인 문구 추가"
git push origin main
```

### 4-3. 기존 작업 폴더로 돌아와 최신 상태 동기화 (Pull)
```bash
# 원래 작업 폴더로 이동
cd ../quiz-game

# 원격 저장소의 최신 커밋을 내 로컬 저장소로 가죠오기
git pull origin main
```

---

## 📜 5. Git 로그 그래프 확인 명령어

병합 히스토리와 브랜치 줄기를 시각적으로 확인하는 command입니다.

```bash
git log --oneline --graph --all --decorate
```

### 실행 출력 예시

```text
*   a1b2c3d (HEAD -> main, origin/main) Merge: feature/play-quiz 브랜치를 main에 병합
|\  
| * e5f6g7h (origin/feature/play-quiz, feature/play-quiz) Feat: 퀴즈 출제와 채점 기능 구현
|/  
* 9i8h7g6 Data: Python, Git, JSON 기본 퀴즈 데이터 10종 추가
* 5f4e3d2 Feat: Quiz 클래스 데이터 구조 및 유효성 검사 구현
* 1a2b3c4 Init: 퀴즈 게임 프로젝트 기본 구조 생성
```

> 📷 위 커밋 로그 화면을 캡처하여 `docs/screenshots/git_log.png` 경로에 저장합니다.
