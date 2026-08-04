# 📋 quiz-game 프로젝트 수행 TODO 리스트

본 프로젝트 개발 과정에서 진행한 구현 단계별 체크리스트와 각 단계별 권장 Git 커밋 메시지 목록입니다.

---

## 🛠️ 개발 수행 단계 및 커밋 가이드

- [x] **1. 개발 환경 확인**
  - Python 3.10+ 버전을 확인하고 프로젝트 디렉터리를 생성합니다.
  - *Git Commit*: `Init: 프로젝트 기본 구조 생성`

- [x] **2. GitHub 저장소 생성 및 Git 초기화**
  - `git init`, `.gitignore` 설정 및 원격 저장소를 연결합니다.
  - *Git Commit*: `Chore: .gitignore 및 프로젝트 기본 파일 생성`

- [x] **3. 기본 파일 생성 및 뼈대 작성**
  - `main.py`, `quiz.py`, `quiz_game.py`, `state.json` 기본 파일을 작성합니다.
  - *Git Commit*: `Init: 프로젝트 소스 코드 기본 파일 뼈대 생성`

- [x] **4. Quiz 클래스 구현**
  - `quiz.py`에 `Quiz` 클래스 (속성, 유효성 검사, `display`, `check_answer`, `to_dict`, `from_dict`)를 작성합니다.
  - *Git Commit*: `Feat: Quiz 클래스 데이터 구조 및 검증 메서드 구현`

- [x] **5. 기본 퀴즈 데이터 작성 (10개)**
  - Python, Git, JSON 기초 문제 10개를 작성하여 기본 데이터 세트를 만듭니다.
  - *Git Commit*: `Data: Python, Git, JSON 관련 기본 퀴즈 10종 추가`

- [x] **6. QuizGame 클래스 구조 및 메뉴 구현**
  - `quiz_game.py`에 메인 메뉴 출력, `get_integer_input`, `get_non_empty_input` 공백 처리 메서드를 구현합니다.
  - *Git Commit*: `Feat: 메인 메뉴 출력 및 대화형 입력 검증 함수 구현`

- [x] **7. 별도 브랜치 생성 (feature/play-quiz)**
  - `git checkout -b feature/play-quiz` 명령을 실행하여 기능 개발 브랜치를 생성합니다.
  - *Git Commit*: (브랜치 생성 작업)

- [x] **8. 퀴즈 출제 및 채점 기능 구현**
  - 풀 문제 수 선택, 문제 렌덤 섞기 (`random.shuffle`), 정답/오답 판단, 100점 환산 로직을 구현합니다.
  - *Git Commit*: `Feat: 퀴즈 출제, 선택지 랜덤 출제 및 점수 계산 기능 구현`

- [x] **9. main 브랜치 병합**
  - `main` 브랜치로 이동하여 `feature/play-quiz`를 `--no-ff` 옵션으로 병합합니다.
  - *Git Commit*: `Merge: feature/play-quiz 브랜치를 main에 병합`

- [x] **10. 퀴즈 추가 기능 구현**
  - 신규 문제, 선택지 4개, 정답 번호, 카테고리/난이도 입력 및 저장 로직을 구현합니다.
  - *Git Commit*: `Feat: 신규 퀴즈 사용자 추가 기능 및 즉시 저장 처리`

- [x] **11. 퀴즈 목록 출력 기능 구현**
  - 저장된 전체 퀴즈 문제와 정답을 번호순으로 출력하는 기능을 작성합니다.
  - *Git Commit*: `Feat: 전체 퀴즈 목록 및 정답 상세 조회 기능 구현`

- [x] **12. 최고 점수 관리 기능 구현**
  - 최고 점수, 정답 문제 수, 전체 문제 수 갱신 및 플레이 히스토리 기록 기능을 구현합니다.
  - *Git Commit*: `Feat: 최고 점수 기록 갱신 및 히스토리 관리 구현`

- [x] **13. state.json 저장 및 불러오기 구현**
  - `save_state()`, `load_state()`를 통해 UTF-8 한글 미깨짐 JSON 저장 및 로딩을 구현합니다.
  - *Git Commit*: `Feat: state.json 파일 입출력 및 UTF-8 직렬화 구현`

- [x] **14. 손상 데이터 자동 복구 기능 구현**
  - `state.json` 미존재 시 자동 생성, 파일 손상 시 백업(`state.json.broken_*`) 후 복구 로직을 구현합니다.
  - *Git Commit*: `Fix: state.json 손상 시 타임스탬프 백업 및 자동 복구 로직 구현`

- [x] **15. 입력 예외 및 안전 종료 처리**
  - `KeyboardInterrupt` (`Ctrl+C`), `EOFError` 발생 시 데이터 저장 후 안전하게 종료되도록 처리합니다.
  - *Git Commit*: `Fix: KeyboardInterrupt 및 EOFError 수신 시 안전 종료 처리`

- [x] **16. 테스트 케이스 작성 및 검증**
  - `TEST_CASES.md`를 기반으로 수동 기능 및 예외 입력 케이스를 검증합니다.
  - *Git Commit*: `Test: 메뉴, 퀴즈 플레이, 추가, 예외 처리 수동 테스트 완료`

- [x] **17. README.md 및 문서 작성**
  - 프로젝트 개요, 클래스 구조, 실행 방법, Git 가이드를 완성합니다.
  - *Git Commit*: `Docs: README.md 및 상세 기술 문서 작성`

- [x] **18. Git clone & pull 실습**
  - 다른 디렉터리로 clone 후 수정사항 반영 및 `git pull` 통합 검증을 진행합니다.
  - *Git Commit*: `Docs: clone 실습 확인 문구 추가 및 통합 완료`

- [x] **19. 실행 화면 스크린샷 촬영 및 배치**
  - `docs/screenshots/` 폴더에 스크린샷 이미지 등록 위치를 준비합니다.
  - *Git Commit*: `Docs: 실행 화면 스크린샷 템플릿 보관`

- [x] **20. 최종 제출 확인**
  - 모든 요구사항 만족 여부를 최종 검토합니다.
  - *Git Commit*: `Chore: 프로젝트 최종 검수 완료 및 제출 준비`

- [x] **21. 터미널 UI 개편 및 랭크 게이지 추가**
  - 박스 테두리 UI, 카테고리 전용 이모지, 성적 평가 게이지 바(`████░░`)를 완성합니다.
  - *Git Commit*: `Feat: 퀴즈 결과 화면에 시각적 점수 게이지 바 추가`
