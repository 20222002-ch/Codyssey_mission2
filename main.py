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


def main():
    while True:
        show_menu()
        choice = read_menu_choice()

        if choice == 1:
            print("퀴즈 풀기 기능은 다음 단계에서 구현합니다.")
        elif choice == 2:
            print("퀴즈 추가 기능은 다음 단계에서 구현합니다.")
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