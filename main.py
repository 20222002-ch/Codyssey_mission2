import json
import random
from pathlib import Path

class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(self.question)

        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer

def create_default_quizzes():
    return [
        Quiz(
            question="Python에서 문자열을 나타내는 자료형은?",
            choices=["int", "str", "bool", "list"],
            answer=2,
        ),
        Quiz(
            question="Python에서 조건에 따라 실행할 코드를 나누는 키워드는?",
            choices=["for", "return", "if", "def"],
            answer=3,
        ),
        Quiz(
            question="Python에서 함수를 정의하는 키워드는?",
            choices=["def", "class", "while", "import"],
            answer=1,
        ),
        Quiz(
            question="다음 중 Python의 불리언 값은?",
            choices=['"hello"', "42", "[1, 2]", "True"],
            answer=4,
        ),
        Quiz(
            question="Python에서 리스트의 첫 번째 요소의 인덱스는?",
            choices=["1", "0", "-1", "2"],
            answer=2,
        ),
    ]

def show_menu():
    print("\n========================================")
    print("          나만의 퀴즈 게임")
    print("========================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("========================================")


def read_menu_choice():
    while True:
        user_input = input("선택: ").strip()

        if user_input == "":
            print("번호를 입력해주세요.")
            continue

        try:
            choice = int(user_input)
        except ValueError:
            print("1~5 사이의 숫자를 입력해주세요.")
            continue

        if 1 <= choice <= 5:
            return choice

        print("1~5 사이의 번호를 선택해주세요.")

def read_answer():
    while True:
        user_input = input("정답 번호 (1~4): ").strip()

        if user_input == "":
            print("정답 번호를 입력해주세요.")
            continue

        try:
            answer = int(user_input)
        except ValueError:
            print("1~4 사이의 숫자를 입력해주세요.")
            continue

        if 1 <= answer <= 4:
            return answer

        print("1~4 사이의 번호를 선택해주세요.")

def read_number(prompt, minimum, maximum):
    while True:
        text = input(prompt).strip()
        try:
            number = int(text)
        except ValueError:
            print(f"{minimum}~{maximum} 사이의 숫자를 입력해주세요.")
            continue
        if minimum <= number <= maximum:
            return number
        print(f"{minimum}~{maximum} 사이의 번호를 선택해주세요.")


def play_quizzes(quizzes):
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    total = read_number(f"풀 문제 수 (1~{len(quizzes)}, 0: 취소): ", 0, len(quizzes))
    if total == 0:
        print("퀴즈 시작을 취소했습니다.")
        return

    selected_quizzes = random.sample(quizzes, total)
    correct_count = 0

    print(f"\n퀴즈를 시작합니다! 총 {total}문제입니다.")

    for number, quiz in enumerate(selected_quizzes, start=1):
        print("\n----------------------------------------")
        print(f"[문제 {number}]")
        quiz.display()

        user_answer = read_answer()

        if quiz.check_answer(user_answer):
            print("정답입니다!")
            correct_count += 1
        else:
            print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

    score = round(correct_count / total * 100, 2)

    print("\n========================================")
    print(f"결과: {total}문제 중 {correct_count}문제 정답!")
    print(f"점수: {score:g}점")
    print("========================================")

    return {
        "score": score,
        "correct_count": correct_count,
        "total": total,
    }

def read_non_empty_text(prompt):
    while True:
        text = input(prompt).strip()

        if text:
            return text

        print("내용을 입력해주세요.")

def add_quiz(quizzes):
    print("\n새로운 퀴즈를 추가합니다.")

    question = read_non_empty_text("문제: ")

    choices = []

    for number in range(1, 5):
        choice = read_non_empty_text(f"선택지 {number}: ")
        choices.append(choice)

    answer = read_answer()

    quiz = Quiz(
        question=question,
        choices=choices,
        answer=answer,
    )

    quizzes.append(quiz)

    print("퀴즈가 추가되었습니다!")
    print(f"현재 등록된 퀴즈: {len(quizzes)}개")

def show_quiz_list(quizzes):
    if not quizzes:
        print("\n등록된 퀴즈가 없습니다.")
        return

    print(f"\n등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print("----------------------------------------")

    for number, quiz in enumerate(quizzes, start=1):
        print(f"[{number}] {quiz.question}")

    print("----------------------------------------")

def show_best_score(best_score):
    if best_score is None:
        print("\n아직 퀴즈를 완료한 기록이 없습니다.")
        return

    score = best_score["score"]
    correct_count = best_score["correct_count"]
    total = best_score["total"]

    print(f"\n최고 점수: {score:g}점")
    print(f"기록: {total}문제 중 {correct_count}문제 정답")

class QuizGame:
    def __init__(self):
        self.state_path = Path(__file__).resolve().parent / "state.json"
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.load_state()

    def parse_state(self, data):
        if not isinstance(data, dict):
            raise ValueError("저장 데이터는 객체 형태여야 합니다.")

        quiz_data = data["quizzes"]
        best_score = data["best_score"]

        if not isinstance(quiz_data, list):
            raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

        quizzes = []

        for item in quiz_data:
            if not isinstance(item, dict):
                raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")

            question = item["question"]
            choices = item["choices"]
            answer = item["answer"]

            if not isinstance(question, str) or not question.strip():
                raise ValueError("문제 내용이 올바르지 않습니다.")

            if not isinstance(choices, list) or len(choices) != 4:
                raise ValueError("선택지는 4개여야 합니다.")

            if any(
                not isinstance(choice, str) or not choice.strip()
                for choice in choices
            ):
                raise ValueError("선택지 내용이 올바르지 않습니다.")

            if type(answer) is not int or not 1 <= answer <= 4:
                raise ValueError("정답 번호가 올바르지 않습니다.")

            quizzes.append(Quiz(question, choices, answer))

        if best_score is not None:
            if not isinstance(best_score, dict):
                raise ValueError("최고 기록 형식이 올바르지 않습니다.")

            score = best_score["score"]
            correct_count = best_score["correct_count"]
            total = best_score["total"]

            if type(total) is not int or total < 1:
                raise ValueError("전체 문제 수가 올바르지 않습니다.")

            if (
                type(correct_count) is not int
                or not 0 <= correct_count <= total
            ):
                raise ValueError("정답 수가 올바르지 않습니다.")

            if type(score) not in (int, float) or not 0 <= score <= 100:
                raise ValueError("점수가 올바르지 않습니다.")

            if score != round(correct_count / total * 100, 2):
                raise ValueError("점수와 정답 수가 일치하지 않습니다.")

        return quizzes, best_score

    def load_state(self):
        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes, best_score = self.parse_state(data)

        except FileNotFoundError:
            print("저장 파일이 없어 기본 퀴즈로 시작합니다.")
            return

        except (ValueError, KeyError, TypeError):
            print("저장 파일이 손상되었거나 형식이 올바르지 않습니다.")
            print("기본 퀴즈와 초기 점수로 시작합니다.")
            return

        except (OSError, UnicodeError) as error:
            print(f"저장 파일을 읽을 수 없습니다: {error}")
            print("기본 퀴즈와 초기 점수로 시작합니다.")
            return

        self.quizzes = quizzes
        self.best_score = best_score

        print(f"저장 데이터를 불러왔습니다. 퀴즈 {len(self.quizzes)}개")

    def save_state(self):
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score,
        }

        temp_path = self.state_path.with_suffix(".tmp")

        try:
            with temp_path.open("w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4,
                    allow_nan=False,
                )

            temp_path.replace(self.state_path)

        except OSError as error:
            print(f"데이터를 저장하지 못했습니다: {error}")
            return False

        print("데이터를 저장했습니다.")
        return True

    def play(self):
        result = play_quizzes(self.quizzes)

        if result is None:
            return

        if (
            self.best_score is None
            or result["score"] > self.best_score["score"]
        ):
            self.best_score = result
            print("새로운 최고 점수입니다!")

        self.save_state()

    def add_quiz(self):
        add_quiz(self.quizzes)
        self.save_state()

    def show_quiz_list(self):
        show_quiz_list(self.quizzes)

    def show_best_score(self):
        show_best_score(self.best_score)

    def run(self):
        while True:
            show_menu()
            choice = read_menu_choice()

            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                print("퀴즈 게임을 종료합니다.")
                break

def main():
    game = QuizGame()

    try:
        game.run()
    finally:
        game.save_state()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n사용자 요청으로 퀴즈 게임을 종료합니다.")
    except EOFError:
        print("\n입력이 종료되어 퀴즈 게임을 종료합니다.")
