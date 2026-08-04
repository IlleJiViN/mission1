"""quiz_game.py - 퀴즈 게임 메인 컨트롤러 및 UI 모듈"""

from datetime import datetime
import json
import pathlib
import random
import sys
from typing import Any, Dict, List

from quiz import Quiz


class QuizGame:
    """게임 상태 관리, 메뉴 출력, 데이터 저장/불러오기 컨트롤러"""

    def __init__(self, state_filename: str = "state.json") -> None:
        self.base_dir: pathlib.Path = pathlib.Path(__file__).parent.resolve()
        self.state_file: pathlib.Path = self.base_dir / state_filename

        self.quizzes: List[Quiz] = []
        self.best_score: int = 0
        self.best_correct: int = 0
        self.best_total: int = 0
        self.history: List[Dict[str, Any]] = []

        self.load_state()

    def create_default_quizzes(self) -> List[Quiz]:
        """기본 퀴즈 10개 세트 생성"""
        return [
            Quiz(
                question="Python에서 리스트(List)를 생성할 때 사용하는 괄호 기호는 무엇인가요?",
                choices=["( ) 소괄호", "[ ] 대괄호", "{ } 중괄호", "< > 화살괄호"],
                answer=2,
                category="Python",
                difficulty="쉬움",
            ),
            Quiz(
                question="PEP 8 가이드에 따라 Python 변수 및 함수 이름에 권장되는 명명 규칙은 무엇인가요?",
                choices=["camelCase", "PascalCase", "snake_case", "kebab-case"],
                answer=3,
                category="Python",
                difficulty="쉬움",
            ),
            Quiz(
                question="Git에서 현재 스테이징 영역에 올라온 변경 사항을 커밋 메시지와 함께 기록하는 명령어는?",
                choices=["git add", "git commit", "git push", "git checkout"],
                answer=2,
                category="Git",
                difficulty="쉬움",
            ),
            Quiz(
                question="다음 중 표준 JSON 형식에서 공식 지원하지 않는 데이터 타입은 무엇인가요?",
                choices=["문자열 (String)", "숫자 (Number)", "Python 튜플 (Tuple)", "불리언 (Boolean)"],
                answer=3,
                category="JSON",
                difficulty="보통",
            ),
            Quiz(
                question="Python에서 딕셔너리(Dictionary) 자료형을 표현할 때 사용하는 기호는 무엇인가요?",
                choices=["( ) 소괄호", "[ ] 대괄호", "{ } 중괄호", "< > 화살괄호"],
                answer=3,
                category="Python",
                difficulty="쉬움",
            ),
            Quiz(
                question="Git에서 새로운 브랜치를 생성함과 동시에 해당 브랜치로 이동하는 명령어는 무엇인가요?",
                choices=["git branch new-b", "git checkout -b new-b", "git merge new-b", "git pull origin main"],
                answer=2,
                category="Git",
                difficulty="보통",
            ),
            Quiz(
                question="Python 표준 라이브러리 중 JSON 직렬화 및 역직렬화를 지원하는 모듈 이름은 무엇인가요?",
                choices=["sys", "os", "json", "pathlib"],
                answer=3,
                category="JSON",
                difficulty="쉬움",
            ),
            Quiz(
                question="Python에서 조건 분기를 작성할 때 첫 번째 조건 이후 추가 조건을 검사하는 키워드는?",
                choices=["else if", "elif", "then", "switch"],
                answer=2,
                category="Python",
                difficulty="쉬움",
            ),
            Quiz(
                question="원격 Git 저장소를 내 컴퓨터 로컬 환경에 새로 복제(다운로드)할 때 사용하는 명령어는?",
                choices=["git init", "git clone", "git status", "git log"],
                answer=2,
                category="Git",
                difficulty="쉬움",
            ),
            Quiz(
                question="Python에서 사용자 정의 함수(Function)를 선언할 때 사용하는 키워드는 무엇인가요?",
                choices=["func", "function", "def", "define"],
                answer=3,
                category="Python",
                difficulty="쉬움",
            ),
        ]

    def load_state(self) -> None:
        """state.json 불러오기 및 예외 복구"""
        if not self.state_file.exists():
            print("\n[안내] state.json 파일이 존재하지 않아 기본 퀴즈 데이터로 생성합니다.")
            self.quizzes = self.create_default_quizzes()
            self.save_state()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("JSON 최상위 데이터가 올바르지 않습니다.")

            self.best_score = int(data.get("best_score", 0))
            self.best_correct = int(data.get("best_correct", 0))
            self.best_total = int(data.get("best_total", 0))
            self.history = data.get("history", []) if isinstance(data.get("history"), list) else []

            raw_quizzes = data.get("quizzes", [])
            loaded: List[Quiz] = []
            for item in raw_quizzes:
                try:
                    loaded.append(Quiz.from_dict(item))
                except Exception as item_err:
                    print(f"[경고] 퀴즈 항목 읽기 건너뀀: {item_err}")

            if not loaded:
                raise ValueError("유효한 퀴즈가 없습니다.")

            self.quizzes = loaded
            print(f"[안내] 성공적으로 {len(self.quizzes)}개의 퀴즈를 불러왔습니다.")

        except Exception as err:
            print(f"\n[오류] state.json 파일이 손상되었거나 형식이 올바르지 않습니다: {err}")
            self.backup_broken_file()
            print("[안내] 기본 퀴즈 데이터로 신규 state.json을 초기화합니다.")
            self.quizzes = self.create_default_quizzes()
            self.best_score = 0
            self.best_correct = 0
            self.best_total = 0
            self.history = []
            self.save_state()

    def backup_broken_file(self) -> None:
        """손상 파일 타임스탬프 백업"""
        if self.state_file.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.state_file.parent / f"state.json.broken_{timestamp}"
            try:
                self.state_file.rename(backup_path)
                print(f"[백업] 손상된 파일이 다음 위치로 보존되었습니다: {backup_path.name}")
            except Exception as e:
                print(f"[경고] 백업 생성 실패: {e}")

    def save_state(self) -> None:
        """state.json 파일 저장"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
            "history": self.history,
        }
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"\n[오류] state.json 저장 실패: {e}")

    def get_non_empty_input(self, prompt: str) -> str:
        """공백 검증 입력"""
        while True:
            try:
                val = input(prompt).strip()
                if val:
                    return val
                print("[입력 오류] 빈 값은 입력할 수 없습니다. 다시 입력해 주세요.")
            except (KeyboardInterrupt, EOFError):
                self.safe_exit()

    def get_integer_input(self, prompt: str, min_val: int, max_val: int) -> int:
        """정수 범위 검증 입력"""
        while True:
            try:
                raw = input(prompt).strip()
                if not raw:
                    print("[입력 오류] 빈 값은 입력할 수 없습니다. 숫자를 입력해 주세요.")
                    continue
                num = int(raw)
                if min_val <= num <= max_val:
                    return num
                print(f"[범위 오류] {min_val}부터 {max_val} 사이의 숫자를 입력해 주세요.")
            except ValueError:
                print("[입력 오류] 숫자로만 입력해야 합니다. 다시 시도해 주세요.")
            except (KeyboardInterrupt, EOFError):
                self.safe_exit()

    def show_menu(self) -> None:
        """메인 메뉴 출력"""
        print("\n" + "=" * 40)
        print("        나만의 Python 퀴즈 게임        ")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print("=" * 40)

    def play_quiz(self) -> None:
        """퀴즈 풀기 실행"""
        if not self.quizzes:
            print("\n[안내] 저장된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요!")
            return

        total_available = len(self.quizzes)
        print(f"\n--- [ 퀴즈 풀기 ] ---")
        print(f"현재 등록된 총 문제 수: {total_available}개")

        count = self.get_integer_input(
            f"풀 문제 수를 입력해 주세요 (1~{total_available}): ",
            min_val=1,
            max_val=total_available,
        )

        quiz_pool = list(self.quizzes)
        random.shuffle(quiz_pool)
        selected = quiz_pool[:count]

        correct_count = 0
        print(f"\n총 {count}문제를 시작합니다! 파이팅!")

        for idx, quiz in enumerate(selected, 1):
            quiz.display(number=idx)
            user_choice = self.get_integer_input("정답 번호 입력 (1~4): ", 1, 4)

            if quiz.check_answer(user_choice):
                print(">> [정답입니다! 👏]")
                correct_count += 1
            else:
                ans_str = quiz.choices[quiz.answer - 1]
                print(f">> [오답입니다. ❌]")
                print(f"   실제 정답: {quiz.answer}번 ({ans_str})")

        score = round((correct_count / count) * 100)
        print("\n" + "=" * 40)
        print("           퀴즈 결과 발표           ")
        print("=" * 40)
        print(f"맞힌 문제 수 : {correct_count} / {count}문제")
        print(f"최종 환산 점수: {score}점")

        if score > self.best_score:
            print("🎉 축하합니다! 최고 점수를 갱신하였습니다! 🎉")
            self.best_score = score
            self.best_correct = correct_count
            self.best_total = count
        elif score == self.best_score and count > self.best_total:
            print("🎉 동일 최고 점수에서 더 많은 문제 풀기 기록을 갱신하였습니다! 🎉")
            self.best_correct = correct_count
            self.best_total = count

        self.history.append({
            "played_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "score": score,
            "correct": correct_count,
            "total": count,
        })

        self.save_state()
        print("결과가 state.json에 안전하게 저장되었습니다.")

    def add_quiz(self) -> None:
        """퀴즈 추가"""
        print("\n--- [ 새 퀴즈 추가 ] ---")
        question = self.get_non_empty_input("1. 문제 내용을 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = self.get_non_empty_input(f"   선택지 {i}번: ")
            choices.append(choice)

        answer = self.get_integer_input("6. 정답 번호를 입력하세요 (1~4): ", 1, 4)
        category = self.get_non_empty_input("7. 카테고리 (예: Python, Git, JSON): ")
        difficulty = self.get_non_empty_input("8. 난이도 (예: 쉬움, 보통, 어려움): ")

        try:
            new_quiz = Quiz(
                question=question,
                choices=choices,
                answer=answer,
                category=category,
                difficulty=difficulty,
            )
            self.quizzes.append(new_quiz)
            self.save_state()

            print("\n✅ 새 퀴즈가 정상적으로 등록 및 저장되었습니다!")
            new_quiz.display(number=len(self.quizzes))

        except ValueError as err:
            print(f"❌ 퀴즈 추가 실패: {err}")

    def show_quizzes(self) -> None:
        """퀴즈 목록 조회"""
        print("\n--- [ 전체 퀴즈 목록 ] ---")
        if not self.quizzes:
            print("현재 저장된 퀴즈가 없습니다.")
            return

        print(f"총 {len(self.quizzes)}개의 퀴즈가 등록되어 있습니다.\n")
        for idx, quiz in enumerate(self.quizzes, 1):
            quiz.display(number=idx)
            correct_text = quiz.choices[quiz.answer - 1]
            print(f"  👉 정답: {correct_text}")

    def show_best_score(self) -> None:
        """최고 점수 및 기록 확인"""
        print("\n--- [ 최고 점수 확인 ] ---")
        if self.best_total == 0:
            print("아직 저장된 점수 기록이 없습니다.")
        else:
            print(f"최고 점수: {self.best_score}점")
            print(f"정답 개수: {self.best_correct}문제")
            print(f"전체 문제 수: {self.best_total}문제")

        if self.history:
            print("\n[ 최근 플레이 히스토리 (최근 5회) ]")
            recent = self.history[-5:]
            for idx, h in enumerate(reversed(recent), 1):
                print(f"  {idx}. 일시: {h.get('played_at', 'N/A')} | 점수: {h.get('score')}점 ({h.get('correct')}/{h.get('total')}문제)")

    def delete_quiz(self) -> None:
        """퀴즈 삭제"""
        print("\n--- [ 퀴즈 삭제 ] ---")
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        print(f"현재 등록된 총 {len(self.quizzes)}개 퀴즈:")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"  {idx}. {quiz.question}")

        idx = self.get_integer_input(
            f"삭제할 퀴즈 번호를 입력하세요 (1~{len(self.quizzes)}): ",
            min_val=1,
            max_val=len(self.quizzes),
        )

        deleted = self.quizzes.pop(idx - 1)
        self.save_state()
        print(f"\n✅ '{deleted.question}' 퀴즈가 삭제되었습니다.")

    def safe_exit(self) -> None:
        """데이터 저장 후 안전 종료"""
        print("\n")
        self.save_state()
        print("데이터를 저장했습니다.")
        print("프로그램을 안전하게 종료합니다.")
        sys.exit(0)

    def run(self) -> None:
        """메인 제어 루프"""
        while True:
            try:
                self.show_menu()
                choice = self.get_integer_input("선택: ", 1, 6)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quizzes()
                elif choice == 4:
                    self.show_best_score()
                elif choice == 5:
                    self.delete_quiz()
                elif choice == 6:
                    self.safe_exit()

            except (KeyboardInterrupt, EOFError):
                self.safe_exit()
            except Exception as e:
                print(f"\n[예외 발생] 오류가 발생했습니다: {e}")
                print("메인 메뉴로 돌아갑니다.")

# feature branch update
