"""
main.py - 퀴즈 게임 프로그램 시작 진입점 (Entry Point)

프로그램을 실행하면 QuizGame 객체를 만들고 메인 루프 run()을 시작합니다.
"""

from quiz_game import QuizGame


def main() -> None:
    """게임 인스턴스를 생성하고 메인 루프를 구동합니다."""
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
