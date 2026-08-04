"""quiz.py - 개별 퀴즈 문제 객체 정의 모듈"""

from typing import Any, Dict, List, Optional


class Quiz:
    """개별 퀴즈 문제와 선택지, 정답을 관리하는 클래스입니다."""

    def __init__(
        self,
        question: str,
        choices: List[str],
        answer: int,
        category: str = "일반",
        difficulty: str = "보통",
    ) -> None:
        self.question = question
        self.choices = choices
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        self.validate()

    def validate(self) -> None:
        """퀴즈 데이터 유효성 검사"""
        if not isinstance(self.question, str) or not self.question.strip():
            raise ValueError("문제 내용은 비어 있을 수 없습니다.")
        if not isinstance(self.choices, list) or len(self.choices) != 4:
            raise ValueError("선택지는 정확히 4개이어야 합니다.")
        for idx, choice in enumerate(self.choices, 1):
            if not isinstance(choice, str) or not choice.strip():
                raise ValueError(f"{idx}번 선택지가 비어 있습니다.")
        if not isinstance(self.answer, int) or not (1 <= self.answer <= 4):
            raise ValueError("정답 번호는 1~4 사이의 정수여야 합니다.")

    def display(self, number: Optional[int] = None) -> None:
        """문제와 선택지 출력"""
        num_str = f" [문제 {number}]" if number else " [문제]"
        print(f"\n{num_str} ({self.category} / 난이도: {self.difficulty})")
        print(f"질문: {self.question}")
        print("-" * 40)
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")
        print("-" * 40)

    def check_answer(self, user_answer: int) -> bool:
        """정답 확인"""
        return user_answer == self.answer

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
        if not isinstance(data, dict):
            raise ValueError("올바르지 않은 데이터 형식입니다.")
        return cls(
            question=data.get("question", ""),
            choices=data.get("choices", []),
            answer=data.get("answer", 1),
            category=data.get("category", "일반"),
            difficulty=data.get("difficulty", "보통"),
        )

    def __repr__(self) -> str:
        return f"<Quiz: {self.question[:15]}... answer={self.answer}>"
