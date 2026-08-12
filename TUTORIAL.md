# 🐍 Python & Git 퀴즈 게임 — 입문자를 위한 코드 학습 가이드

> 이 문서는 퀴즈 게임 소스코드(`main.py`, `quiz.py`, `quiz_game.py`)를 처음부터 함께 읽으며,  
> **각 코드가 왜 이렇게 생겼는지**를 설명하는 입문자 맞춤 학습 자료입니다.

---

## 📌 목차

1. [프로그램 구조 한눈에 보기](#1-프로그램-구조-한눈에-보기)
2. [main.py — 프로그램의 시작점](#2-mainpy--프로그램의-시작점)
3. [quiz.py — Quiz 클래스 완전 분해](#3-quizpy--quiz-클래스-완전-분해)
4. [quiz_game.py — QuizGame 클래스 완전 분해](#4-quiz_gamepy--quizgame-클래스-완전-분해)
5. [핵심 개념 정리 카드](#5-핵심-개념-정리-카드)
6. [state.json — 데이터 파일 이해하기](#6-statejson--데이터-파일-이해하기)

---

## 1. 프로그램 구조 한눈에 보기

이 퀴즈 게임은 **3개의 Python 파일**로 나뉘어 있습니다.  
각 파일이 하나의 역할만 담당하도록 설계되어 있습니다 (= **역할 분리, Separation of Concerns**).

```
python3 main.py       ← 사용자가 실행하는 명령
       │
       ▼
   main.py            ← "시작점" — QuizGame 객체를 만들고 실행
       │
       ▼
 quiz_game.py         ← "총감독" — 메뉴, 게임 진행, 파일 저장 담당
       │
       ▼
   quiz.py            ← "단역배우" — 퀴즈 한 문제의 데이터와 동작 담당
       │
       ▼
  state.json          ← "창고" — 퀴즈 데이터와 점수를 영구 보관
```

---

## 2. `main.py` — 프로그램의 시작점

### 실제 코드

```python
"""
main.py - 퀴즈 게임 프로그램 시작 진입점 (Entry Point)
"""

from quiz_game import QuizGame   # (1) quiz_game.py에서 QuizGame 클래스를 가져옴


def main() -> None:
    """게임 인스턴스를 생성하고 메인 루프를 구동합니다."""
    game = QuizGame()    # (2) QuizGame 객체(인스턴스) 생성
    game.run()           # (3) 게임 시작


if __name__ == "__main__":   # (4) 이 파일을 직접 실행했을 때만 main() 호출
    main()
```

### 코드 한 줄씩 이해하기

**(1) `from quiz_game import QuizGame`**
> 다른 파일에서 코드를 가져오는 방법입니다.  
> `quiz_game.py` 파일 안에 정의된 `QuizGame` 클래스를 이 파일에서도 쓸 수 있게 됩니다.

**(2) `game = QuizGame()`**
> 클래스(설계도)로부터 **객체(실제 물건)** 를 하나 만드는 코드입니다.  
> `QuizGame()`을 호출하면 내부적으로 `__init__` 메서드가 자동 실행됩니다.

**(3) `game.run()`**
> `game` 객체의 `run` 메서드를 실행합니다.  
> 이 한 줄이 퀴즈 게임 전체를 동작시킵니다.

**(4) `if __name__ == "__main__":`**
> Python 파일은 두 가지 방식으로 실행될 수 있습니다.  
> - **직접 실행**: `python3 main.py` → `__name__`이 `"__main__"`이 됨 → `main()` 호출 O  
> - **다른 파일에서 import**: `from main import ...` → `__name__`이 파일명이 됨 → `main()` 호출 X  
> 이 조건 덕분에 import 할 때 게임이 갑자기 시작되는 사고를 막을 수 있습니다.

---

## 3. `quiz.py` — Quiz 클래스 완전 분해

퀴즈 **한 문제**의 데이터와 동작을 담당하는 클래스입니다.

### 3-1. 클래스 선언과 `__init__` (초기화)

```python
class Quiz:
    def __init__(
        self,
        question: str,       # 문제 내용 (문자열)
        choices: List[str],  # 선택지 4개 (문자열 리스트)
        answer: int,         # 정답 번호 1~4 (정수)
        category: str = "일반",   # 카테고리 (기본값: "일반")
        difficulty: str = "보통", # 난이도 (기본값: "보통")
    ) -> None:
        self.question = question     # 속성에 값 저장
        self.choices = choices
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        self.validate()              # 저장 직후 데이터 검증 실행
```

#### 💡 `__init__`이란?
> 객체가 **처음 만들어지는 순간** 자동으로 실행되는 특별한 메서드입니다.  
> 택배 박스를 열었을 때 내용물을 꺼내서 정리하는 것과 같습니다.

#### 💡 `self`란?
> `self`는 **"이 객체 자신"** 을 가리키는 참조입니다.  
> 여러 개의 Quiz 객체(`q1`, `q2`)가 있어도 각자의 데이터를 따로 유지할 수 있는 이유입니다.

#### 💡 타입 힌트 (`str`, `int`, `List[str]`)란?
> `: str`, `: int`처럼 뒤에 붙는 표시는 **"이 인자는 이 타입이어야 해요"** 라는 안내문입니다.  
> 강제성은 없지만 코드를 읽는 사람과 IDE에 큰 도움을 줍니다.

---

### 3-2. JSON 변환 (`to_dict` / `from_dict`)

```python
def to_dict(self) -> Dict[str, Any]:
    """JSON 변환용 딕셔너리 리턴"""
    return {
        "question": self.question,
        "choices": self.choices,
        "answer": self.answer,
        "category": self.category,
        "difficulty": self.difficulty,
    }

@classmethod
def from_dict(cls, data: Dict[str, Any]) -> "Quiz":
    """JSON 딕셔너리에서 객체 생성"""
    return cls(
        question=data.get("question", ""),
        choices=data.get("choices", []),
        answer=data.get("answer", 1),
        category=data.get("category", "일반"),
        difficulty=data.get("difficulty", "보통"),
    )
```

#### 💡 왜 이 두 메서드가 필요한가요?
> Python의 Quiz 객체는 JSON 파일에 그대로 저장할 수 없습니다.  
> JSON은 딕셔너리(`dict`) 형태만 이해하므로, **객체 ↔ 딕셔너리 변환** 통로가 필요합니다.

#### 💡 `@classmethod`와 `cls`란?
> 일반 메서드는 `self`(이미 만들어진 객체)가 필요합니다.  
> `@classmethod`는 **객체 없이 클래스 자체로 호출**할 수 있는 특별한 메서드입니다. (`Quiz.from_dict(...)` 형태로 사용)

---

## 4. `quiz_game.py` — QuizGame 클래스 완전 분해

### 4-1. 파일 불러오기 (`load_state`)

```python
try:
    # 파일 열기 (r = read 읽기, utf-8 인코딩)
    with open(self.state_file, "r", encoding="utf-8") as f:
        data = json.load(f)   # JSON 텍스트 → Python 딕셔너리
except Exception as err:
    print(f"\n[오류] state.json 손상: {err}")
```

#### 💡 `with open(...) as f:`
> 파일을 열고 작업한 뒤 **자동으로 닫아주는** 안전한 방법입니다.

#### 💡 `try / except`
> 오류가 났을 때 프로그램이 뻗지 않고(Crash), 대체 행동(예: 백업 후 기본값 생성)을 하도록 막아주는 방어막입니다.

### 4-2. 무한 반복과 안전한 숫자 입력 (`get_integer_input`)

```python
def get_integer_input(self, prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            raw = input(prompt).strip()  # 앞뒤 공백 제거
            if not raw: continue
            
            num = int(raw)
            if min_val <= num <= max_val:
                return num               # 통과 시 무한 반복 탈출
                
        except ValueError:
            print("[입력 오류] 숫자로만 입력해야 합니다.")
```

#### 💡 `while True:` + `continue` + `return`
> 올바른 숫자를 입력할 때까지 사용자를 놓아주지 않는 견고한 입력 방식입니다.  
> 조건에 맞으면 `return`으로 함수를 완전히 빠져나갑니다.

---

## 5. 핵심 개념 정리 카드

| 자료형 | 이름 | 이 코드에서 쓰인 곳 |
|:---:|:---:|:---|
| `int` | 정수 | 정답 번호, 점수, 인덱스 |
| `str` | 문자열 | 문제 내용, 선택지, 카테고리 |
| `bool` | 참/거짓 | `check_answer()` 반환값 |
| `list` | 목록 | 선택지 목록, 퀴즈 목록 |
| `dict` | 사전 | JSON 데이터, 히스토리 기록 |

| 개념 | 한 줄 설명 |
|:---|:---|
| 클래스 | 데이터와 동작을 묶은 설계도 |
| 객체 | 클래스로 만든 실체 |
| `__init__` | 객체 초기화 메서드 |
| `self` | 객체 자신을 가리킴 |

---

## 6. `state.json` — 데이터 파일 구조

```json
{
    "quizzes": [
        {
            "question": "Python에서 리스트를 생성하는 기호는?",
            "choices": ["( )", "[ ]", "{ }", "< >"],
            "answer": 2
        }
    ],
    "best_score": 100
}
```
- 프로그램이 종료되어도 변수가 휘발되지 않도록 하드디스크에 보관하는 형태입니다.
- Python의 딕셔너리(dict)와 완벽히 1:1로 대응됩니다.
