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

def play_quizzes(quizzes):
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    correct_count = 0
    total = len(quizzes)

    print(f"\n퀴즈를 시작합니다! 총 {total}문제입니다.")

    for number, quiz in enumerate(quizzes, start=1):
        print("\n----------------------------------------")
        print(f"[문제 {number}]")
        quiz.display()

        user_answer = read_answer()

        if quiz.check_answer(user_answer):
            print("정답입니다!")
            correct_count += 1
        else:
            print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

    score = correct_count / total * 100

    print("\n========================================")
    print(f"결과: {total}문제 중 {correct_count}문제 정답!")
    print(f"점수: {score:.0f}점")
    print("========================================")

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

def main():
    quizzes = create_default_quizzes()

    while True:
        show_menu()
        choice = read_menu_choice()

        if choice == 1:
            play_quizzes(quizzes)
        elif choice == 2:
            add_quiz(quizzes)
        elif choice == 3:
            print("퀴즈 목록 기능은 다음 단계에서 구현합니다.")
        elif choice == 4:
            print("점수 확인 기능은 다음 단계에서 구현합니다.")
        elif choice == 5:
            print("퀴즈 게임을 종료합니다.")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n사용자 요청으로 퀴즈 게임을 종료합니다.")
    except EOFError:
        print("\n입력이 종료되어 퀴즈 게임을 종료합니다.")