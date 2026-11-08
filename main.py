import json
import random
from pathlib import Path
from datetime import datetime

HINT_PENALTY = 5


def calculate_score(correct_count, total, hints_used=0, hint_penalty=HINT_PENALTY):
    return max(0, round(correct_count / total * 100 - hints_used * hint_penalty, 2))


class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

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
            hint="텍스트를 표현하는 자료형이며 string의 약자입니다.",
        ),
        Quiz(
            question="Python에서 조건에 따라 실행할 코드를 나누는 키워드는?",
            choices=["for", "return", "if", "def"],
            answer=3,
            hint="조건이 참일 때 실행할 코드를 지정하는 키워드입니다.",
        ),
        Quiz(
            question="Python에서 함수를 정의하는 키워드는?",
            choices=["def", "class", "while", "import"],
            answer=1,
            hint="define에서 유래한 세 글자 키워드입니다.",
        ),
        Quiz(
            question="다음 중 Python의 불리언 값은?",
            choices=['"hello"', "42", "[1, 2]", "True"],
            answer=4,
            hint="참과 거짓은 따옴표 없이 쓰며 첫 글자는 대문자입니다.",
        ),
        Quiz(
            question="Python에서 리스트의 첫 번째 요소의 인덱스는?",
            choices=["1", "0", "-1", "2"],
            answer=2,
            hint="리스트의 인덱스는 첫 위치를 0으로 셉니다.",
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
    print("6. 퀴즈 삭제")
    print("7. 점수 히스토리")
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
            print("1~7 사이의 숫자를 입력해주세요.")
            continue

        if 1 <= choice <= 7:
            return choice

        print("1~7 사이의 번호를 선택해주세요.")

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


def read_quiz_answer(quiz):
    used_hint = False
    while True:
        text = input("정답 번호 (1~4, h: 힌트): ").strip().lower()
        if text == "h":
            if not quiz.hint:
                print("이 문제에는 등록된 힌트가 없습니다. 감점하지 않습니다.")
            else:
                print(f"힌트: {quiz.hint}")
                if not used_hint:
                    print(f"이 문제의 힌트 사용으로 최종 점수에서 {HINT_PENALTY}점 차감됩니다.")
                else:
                    print("이미 확인한 힌트입니다. 추가 감점은 없습니다.")
                used_hint = True
            continue
        try:
            answer = int(text)
        except ValueError:
            print("1~4 사이의 숫자 또는 h를 입력해주세요.")
            continue
        if 1 <= answer <= 4:
            return answer, used_hint
        print("1~4 사이의 번호를 선택해주세요.")


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
    hints_used = 0

    print(f"\n퀴즈를 시작합니다! 총 {total}문제입니다.")

    for number, quiz in enumerate(selected_quizzes, start=1):
        print("\n----------------------------------------")
        print(f"[문제 {number}]")
        quiz.display()

        user_answer, used_hint = read_quiz_answer(quiz)
        hints_used += int(used_hint)

        if quiz.check_answer(user_answer):
            print("정답입니다!")
            correct_count += 1
        else:
            print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

    score = calculate_score(correct_count, total, hints_used)

    print("\n========================================")
    print(f"결과: {total}문제 중 {correct_count}문제 정답!")
    print(f"점수: {score:g}점")
    print(f"힌트 사용: {hints_used}회 (회당 {HINT_PENALTY}점 차감, 최소 0점)")
    print("========================================")

    return {
        "score": score,
        "correct_count": correct_count,
        "total": total,
        "hints_used": hints_used,
        "hint_penalty": HINT_PENALTY,
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
    hint = input("힌트 (선택 사항, Enter: 없음): ").strip()

    quiz = Quiz(
        question=question,
        choices=choices,
        answer=answer,
        hint=hint,
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
    print(f"힌트 사용: {best_score.get('hints_used', 0)}회")

class QuizGame:
    def __init__(self):
        self.state_path = Path(__file__).resolve().parent / "state.json"
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.history = []
        self.load_state()

    def parse_state(self, data):
        if not isinstance(data, dict):
            raise ValueError("저장 데이터는 객체 형태여야 합니다.")

        quiz_data = data["quizzes"]
        best_score = data["best_score"]

        if not isinstance(quiz_data, list):
            raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

        quizzes = []
        default_hints = {q.question: q.hint for q in create_default_quizzes()}

        for item in quiz_data:
            if not isinstance(item, dict):
                raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")

            question = item["question"]
            choices = item["choices"]
            answer = item["answer"]
            hint = item.get("hint", default_hints.get(question, "")) if isinstance(question, str) else ""

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

            if not isinstance(hint, str):
                raise ValueError("힌트 형식이 올바르지 않습니다.")

            quizzes.append(Quiz(question, choices, answer, hint))

        if best_score is not None:
            best_score = self.parse_record(best_score)

        history_data = data.get("history", [])
        if not isinstance(history_data, list):
            raise ValueError("점수 히스토리 형식이 올바르지 않습니다.")
        history = [self.parse_record(record, require_date=True) for record in history_data]

        return quizzes, best_score, history

    def parse_record(self, record, require_date=False):
        if not isinstance(record, dict):
            raise ValueError("점수 기록 형식이 올바르지 않습니다.")
        score = record["score"]
        correct_count = record["correct_count"]
        total = record["total"]
        hints_used = record.get("hints_used", 0)
        # Records written before the five-point rule used ten points per hint.
        hint_penalty = record.get("hint_penalty", 10)

        if type(total) is not int or total < 1:
            raise ValueError("전체 문제 수가 올바르지 않습니다.")
        if type(correct_count) is not int or not 0 <= correct_count <= total:
            raise ValueError("정답 수가 올바르지 않습니다.")
        if type(score) not in (int, float) or not 0 <= score <= 100:
            raise ValueError("점수가 올바르지 않습니다.")
        if type(hints_used) is not int or not 0 <= hints_used <= total:
            raise ValueError("힌트 사용 횟수가 올바르지 않습니다.")
        if type(hint_penalty) is not int or hint_penalty not in (5, 10):
            raise ValueError("힌트 감점 기준이 올바르지 않습니다.")
        if score != calculate_score(correct_count, total, hints_used, hint_penalty):
            raise ValueError("점수와 정답 수가 일치하지 않습니다.")

        parsed = dict(score=score, correct_count=correct_count, total=total,
                      hints_used=hints_used, hint_penalty=hint_penalty)
        if require_date:
            played_at = record["played_at"]
            if not isinstance(played_at, str):
                raise ValueError("게임 기록 날짜가 올바르지 않습니다.")
            if datetime.fromisoformat(played_at).utcoffset() is None:
                raise ValueError("게임 기록 날짜에 시간대가 필요합니다.")
            parsed["played_at"] = played_at
        return parsed

    def load_state(self):
        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes, best_score, history = self.parse_state(data)

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
        self.history = history

        print(f"저장 데이터를 불러왔습니다. 퀴즈 {len(self.quizzes)}개")

    def save_state(self):
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                    "hint": quiz.hint,
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score,
            "history": self.history,
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

        self.history.append({
            **result,
            "played_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        })

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

    def delete_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        self.show_quiz_list()
        number = read_number(f"삭제할 문제 번호 (1~{len(self.quizzes)}, 0: 취소): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했습니다.")
            return
        quiz = self.quizzes[number - 1]
        print(f"삭제할 문제: {quiz.question}")
        while True:
            confirmation = input("이 문제를 삭제할까요? (y/n): ").strip().lower()
            if confirmation in ("y", "n"):
                break
            print("y 또는 n을 입력해주세요.")
        if confirmation == "n":
            print("삭제를 취소했습니다.")
            return
        self.quizzes.pop(number - 1)
        if self.save_state():
            print("퀴즈를 삭제했습니다. 기존 점수 기록은 유지됩니다.")
        else:
            self.quizzes.insert(number - 1, quiz)
            print("저장 실패로 삭제를 취소하고 문제를 복원했습니다.")

    def show_history(self):
        if not self.history:
            print("아직 완료한 게임 기록이 없습니다.")
            return
        print(f"\n점수 히스토리 (총 {len(self.history)}회, 최신순)")
        for number, record in enumerate(reversed(self.history), start=1):
            played_at = datetime.fromisoformat(record["played_at"]).isoformat(sep=" ")
            print(f"[{number}] {played_at} | {record['total']}문제 중 "
                  f"{record['correct_count']}개 정답 | {record['score']:g}점 | "
                  f"힌트 {record['hints_used']}회")

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
            elif choice == 6:
                self.delete_quiz()
            elif choice == 7:
                self.show_history()

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
