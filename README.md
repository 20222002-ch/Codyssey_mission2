# Codyssey Mission 2 — Python 기초 퀴즈 게임

## 프로젝트 개요

Python 기본 문법, 클래스, JSON 파일 입출력과 Git을 학습하기 위해 만든 콘솔 퀴즈 게임이다. 터미널에서 번호를 선택해 퀴즈를 풀거나 추가하고, 목록과 최고 점수를 확인한다. 추가한 문제와 최고 기록은 재실행 후에도 유지된다.

완성된 기능뿐 아니라 **메뉴부터 기능을 하나씩 구현하고, 확인하고, 커밋한 과정**을 미션 요구사항 순서대로 기록했다. 필수 기능을 완성한 뒤 별도 브랜치에서 보너스 5가지도 구현했다. 1~13단계와 기존 이미지는 필수 기능 개발 당시의 기록으로 보존하고, 이후 변경은 아래 **보너스 과제 개발 과정**에 구분해 기록했다.

## 현재 기능 요약과 문서 읽는 방법

**현재 프로그램에서는 등록된 문제를 전부 풀 필요가 없다.** 게임을 시작할 때 원하는 문제 수를 선택하고, 해당 개수만 중복 없이 랜덤으로 출제한다. 예를 들어 기본 5문제에 1문제를 추가해 총 6개가 등록되어 있어도 2개만 골라 플레이할 수 있다.

| 현재 기능 | 동작과 자세한 설명 |
| --- | --- |
| 문제 수 선택·랜덤 출제 | 1~등록된 전체 문제 수 중 선택, 0은 시작 취소. [B1 설명](#b1-랜덤-출제와-문제-수-선택) |
| 힌트 | 풀이 중 h로 확인. 사용한 문제당 5점 감점, 같은 문제 반복 조회는 추가 감점 없음. [B2 설명](#b2-힌트와-감점) |
| 문제 추가·목록·삭제 | 등록된 전체 목록을 관리하며 출제 수와는 별개다. 삭제 전 확인하고 저장한다. [기능 목록](#기능-목록), [B3 설명](#b3-퀴즈-삭제) |
| 최고 점수·게임 기록 | 완료한 결과를 기록하며 문제·최고 점수·히스토리는 재실행 후에도 유지된다. [데이터 설명](#데이터-파일-설명), [B4 설명](#b4-점수-히스토리) |

> **개발 기록 안내:** 아래 1~13단계는 해당 시점에 구현한 내용이고, 현재 기능은 위 요약과 하단의 기능 목록을 기준으로 읽으면 된다. 일부 이미지는 각 단계의 커밋 직후가 아니라 기능을 연결한 뒤 촬영한 통합 검증 화면이다. 당시에는 없던 기능과 이후 확장 내용은 각 항목의 안내 및 각주로 연결했다. 과거 화면의 메뉴·문제 수·점수는 현재 버전의 제한을 의미하지 않는다.

## 퀴즈 주제와 선정 이유

주제는 **Python 기초 문법**이다. 미션에서 배우는 자료형, 조건문, 함수, 불리언, 리스트 인덱스를 문제로 구성해 개발과 학습 내용을 연결했다. 기본 문제는 5개이며, 각 문제는 선택지 4개와 1~4의 정답 번호를 갖는다.

## 개발 환경

| 항목 | 환경 |
| --- | --- |
| 운영체제 | Windows |
| 편집기 | Visual Studio Code |
| Python | 3.14.5 — 미션 기준은 3.10 이상 |
| Git | 2.51.2.windows.1 |
| 라이브러리 | 표준 라이브러리 `json`, `pathlib`, `random`, `datetime` |

![Python 버전](docs/screenshots/python-version.png)
![Git 버전](docs/screenshots/git-version.png)
![Git 사용자 설정](docs/screenshots/git-user.png)

## 개발 과정

### 1. 개발 환경 및 저장소 초기 설정

**목표와 진행:** 미션 1과 구분되는 `Codyssey_mission2` 저장소와 작업 폴더를 준비했다. `.gitignore`, `README.md`, `main.py`를 만들고 환영 문구 한 줄을 실행하는 것부터 시작했다. 초기 구성: [`b0348cf`](https://github.com/20222002-ch/Codyssey_mission2/commit/b0348cf).

**겪은 문제와 해결:** VS Code에서 이전 미션 폴더가 열려 있어 예전 저장소가 연결된 것처럼 보였다. 기존 원격 주소를 바꾸는 대신 미션 2 폴더를 따로 열고 `git remote -v`로 대상을 확인하는 방식으로 구분했다. `python --version`에서는 숫자 없이 `Python`만 출력되었다. 이후 `py --version`으로 Python 3.14.5를 확인했고 실행도 `py main.py`를 사용했다. 당시 현상만으로 별칭과 PATH 중 어느 것이 원인인지는 단정하지 않았다.

**정리한 개념:** VS Code에서 연 폴더, 로컬 저장소, GitHub 원격 저장소는 각각 확인해야 한다. `.gitignore`에는 캐시와 가상환경 등을 지정했다.

### 2. 메뉴 및 입력 처리 구현

> **화면 버전 안내:** 아래는 필수 메뉴 1~5번을 구현하던 시점의 화면이다. 현재는 5번 종료를 유지하면서 6번 삭제와 7번 히스토리가 추가되어 있다. [현재 기능 목록](#기능-목록)을 참고한다.

**진행:** `show_menu()`, `read_menu_choice()`, `main()`으로 출력·입력·진행을 나눴다. `while`로 반복하고 `if/elif`로 분기했다. `strip()`으로 공백을 제거하고 정수로 변환하며 빈 입력·문자·범위 밖 번호는 다시 받는다. 커밋: [`ad3ca07`](https://github.com/20222002-ch/Codyssey_mission2/commit/ad3ca07).

**선택 이유와 확인:** 잘못된 입력 때문에 프로그램이 끝나지 않도록 `ValueError`를 처리했다. 개발 중 캡처에서 문자, 0, 빈 입력의 재입력과 `Ctrl+C` 종료 안내를 확인할 수 있다. 최종 검증에서도 재확인했다.

![메뉴](docs/screenshots/menu.png)
![입력 오류와 Ctrl+C 종료](docs/screenshots/invalid-input.png)

### 3. Quiz 클래스 작성

> **현재 확장:** 이 단계는 문제·선택지·정답을 묶은 초기 클래스에 대한 설명이다. 현재 `Quiz`에는 선택적 `hint` 속성도 있다. [B2. 힌트와 감점](#b2-힌트와-감점)을 참고한다.

**진행:** 개별 문제의 `question`, `choices`, `answer`를 객체에 담았다. `display()`는 문제와 선택지를 출력하고 `check_answer()`는 정답 여부를 반환한다. 커밋: [`7aa7665`](https://github.com/20222002-ch/Codyssey_mission2/commit/7aa7665).

**선택 이유와 확인:** 관련 데이터와 동작을 한 객체로 묶었다. `__init__`은 초기화, `self`는 현재 객체의 속성과 메서드 접근에 사용한다. 정답 입력은 `True`, 오답은 `False`를 반환하는 것을 검증했다.

### 4. 기본 퀴즈 데이터 작성

> **문제 수 안내:** 기본 5개는 저장 파일이 없을 때 시작하는 문제 수다. 추가·삭제 후에는 저장된 목록을 불러오므로 항상 5개로 고정되는 것이 아니다. 등록된 문제 수와 한 게임의 출제 수는 구분한다.[^question-count]

**진행:** `create_default_quizzes()`에서 기본 문제 5개를 `Quiz` 객체로 만들어 리스트로 반환했다. 선택지 4개와 1~4의 정수 정답 번호를 사용했다. 커밋: [`300b886`](https://github.com/20222002-ch/Codyssey_mission2/commit/300b886).

**선택 이유와 확인:** 생성 함수를 분리해 첫 실행과 파일 복구에 재사용했다. 문제 수·선택지 수·정답 범위를 검증했다. 리스트 인덱스는 0부터 시작하지만 사용자에게 보여주는 번호는 1부터 시작한다는 기준을 유지했다.

### 5. 별도 브랜치에서 퀴즈 풀기 구현 및 병합

> **당시와 현재:** 이 단계에서는 등록된 전체 문제를 순서대로 풀었다. 현재는 원하는 개수만 랜덤으로 출제한다. 아래 ‘6문제 중 5문제 정답’ 이미지는 기본 5문제에 테스트 문제 1개를 추가하고 등록·저장 기능까지 연결한 **필수 기능 통합 검증 화면**이며, 5번 단계의 커밋 직후 화면은 아니다.[^play-snapshot]

**진행:** `git checkout -b codex/quiz-play`로 브랜치를 만들었다. `play_quizzes()`에서 순서대로 출제하고 `read_answer()`로 답을 받았다. 정답·오답을 안내하고 완료 시 정답 수와 점수를 출력했다. 빈 목록은 안내 후 반환한다. 기능: [`12072df`](https://github.com/20222002-ch/Codyssey_mission2/commit/12072df), 병합: [`339a69e`](https://github.com/20222002-ch/Codyssey_mission2/commit/339a69e).

**선택 이유와 확인:** `Quiz`의 출력·판별 메서드를 재사용하고 전체 진행은 함수로 분리했다. 빈 목록을 먼저 처리해 0으로 나누는 계산을 방지했다. `--no-ff`로 병합 기록을 남겨 아래 그래프에서 갈라졌다 합쳐지는 흐름을 확인했다.

프로젝트 루트에서 다음 명령으로 아래 풀이 결과 로그 창을 연다.

```powershell
py docs/verification/view_log.py docs/verification/play.txt
```

![마지막 문제와 풀이 결과 실행 로그](docs/screenshots/play.jpg)

![브랜치 병합 당시 기록](docs/screenshots/branch-merge.png)

### 6. 퀴즈 추가 기능 구현

> **현재 동작:** 한 문제를 추가하면 등록 목록이 한 개 늘어나지만, 다음 게임에서 반드시 그 전체 개수를 풀어야 하는 것은 아니다. 출제 수는 게임 시작 시 별도로 선택한다. 이 단계에서는 메모리에 등록했고 [10단계](#10-statejson-저장-및-불러오기-구현)에서 파일 저장 연결을 완료했으므로, 현재 추가한 문제는 재실행 후에도 유지된다.[^question-count]

**진행:** 문제, 선택지 4개, 정답 번호를 받아 새 객체를 추가했다. `read_non_empty_text()`로 빈 문장을 막고 기존 `read_answer()`로 정답 범위를 검증했다. 커밋: [`91484e3`](https://github.com/20222002-ch/Codyssey_mission2/commit/91484e3).

**선택 이유와 확인:** 모든 입력이 끝나야 등록해 입력 도중 취소된 문제가 남지 않도록 했다. 처음에는 실행 중 리스트에만 추가했고 10단계에서 저장을 연결했다. 최종 검증에서 빈 문제·선택지와 잘못된 정답 번호를 재입력한 뒤 6번째 문제가 등록되는 것을 확인했다.

프로젝트 루트에서 다음 명령으로 아래 등록 로그 창을 연다.

```powershell
py docs/verification/view_log.py docs/verification/add.txt
```

![등록과 입력 검증 실행 로그](docs/screenshots/add_quiz.jpg)

### 7. 퀴즈 목록 기능 구현

> **목록과 출제 수의 차이:** 아래 5개→6개는 저장된 전체 문제 목록의 변화다. 현재 게임에서 실제로 풀 문제 수는 사용자가 따로 선택한다. 목록 화면은 출제 대기 문제 전체를 보여주는 것이며, 전부 풀어야 한다는 뜻은 아니다.[^question-count]

**진행:** `show_quiz_list()`로 전체 문제 수와 번호별 문제 문장을 출력했다. 빈 목록에는 안내를 추가했다. 커밋: [`f3ac6b7`](https://github.com/20222002-ch/Codyssey_mission2/commit/f3ac6b7).

**선택 이유와 확인:** 추가와 조회가 같은 리스트를 사용하도록 했다. 개발 중 저장한 화면에서 5개였던 목록이 등록 후 6개가 된 것을 확인할 수 있다.

추가 전:

![추가 전 목록](docs/screenshots/list-before.png)

추가 후:

![추가 후 목록](docs/screenshots/list.png)

### 8. 최고 점수 기능 구현

> **기록 버전 안내:** 아래 점수 화면은 힌트 기능 도입 전의 필수 기능 검증 결과다. 현재는 힌트 사용 문제당 5점을 차감하며 기존 기록은 당시 계산 기준으로 보존한다. 또한 초기 메모리상 기록은 [10단계](#10-statejson-저장-및-불러오기-구현)에서 저장을 연결해 현재는 재실행 후에도 유지된다. [현재 점수 규칙](#b2-힌트와-감점)을 참고한다.

**진행:** 결과를 `score`, `correct_count`, `total` 딕셔너리로 반환하고 높은 점수일 때만 최고 기록을 갱신했다. 메뉴 4번에 조회를 연결했다. 커밋: [`fc29e72`](https://github.com/20222002-ch/Codyssey_mission2/commit/fc29e72).

**설계상 고려와 해결:** 미플레이를 0으로 표현하면 실제 0점 기록과 구분하기 어렵다. 미플레이는 `None`, 완료한 게임은 0점이어도 딕셔너리로 관리했다. 문제 수가 달라도 비교할 수 있도록 100점으로 환산하고 소수점 둘째 자리까지 반올림한다. 동점은 기존 기록을 유지한다.

**확인:** 미플레이 안내, 0점 등록, 높은 점수 갱신, 낮거나 같은 점수에서 유지되는 동작을 검증했다. 이 단계의 메모리상 기록은 10단계에서 파일 저장과 연결했다.

프로젝트 루트에서 다음 명령으로 아래 최고 점수 로그 창을 연다.

```powershell
py docs/verification/view_log.py docs/verification/score.txt
```

![최고 점수 조회 실행 로그](docs/screenshots/score.jpg)

### 9. QuizGame 클래스로 구조 정리

**진행:** 기존 `main()`의 목록과 최고 기록을 `QuizGame` 속성으로 옮겼다. `run()`은 메뉴 반복, `play()`는 게임 진행과 기록 갱신을 맡는다. 등록·목록·점수 조회는 기존 함수와 연결했다. 커밋: [`b104406`](https://github.com/20222002-ch/Codyssey_mission2/commit/b104406).

**선택 이유와 확인:** `Quiz`는 개별 문제, `QuizGame`은 전체 상태를 담당한다. 세부 함수는 재사용하고 `main()`은 객체 생성과 실행 중심으로 줄였다. 구조 변경 후 등록·조회·풀이·점수 흐름을 최종 검증했다.

### 10. state.json 저장 및 불러오기 구현

> **복원 예시 안내:** 아래 6개 문제는 기본 5개에 1개를 추가한 상태가 저장·복원됐다는 의미다. 현재도 저장된 전체 목록을 복원하지만, 게임에서 풀 개수는 별도로 선택한다. 현재 저장 구조에는 보너스에서 추가한 힌트·히스토리 필드도 포함된다. [현재 데이터 설명](#데이터-파일-설명)을 참고한다.

**진행:** `save_state()`, `load_state()`, `parse_state()`를 추가했다. 객체를 딕셔너리로 변환해 UTF-8 JSON으로 저장하고 불러올 때 검증 후 복원한다. 등록 직후, 게임 완료 후, 종료 시 저장한다. 커밋: [`d56f49d`](https://github.com/20222002-ch/Codyssey_mission2/commit/d56f49d).

**진행 중 확인한 점:** `state.json`의 위치가 혼동되었다. 경로는 `Path(__file__).resolve().parent / "state.json"`이므로 터미널 위치가 아니라 `main.py` 옆이다. 저장이 실행되면 파일이 생성된다.

**설계상 고려와 해결:** 누락·손상 파일은 기본 데이터로 시작하고, 검증을 모두 통과해야 불러온 상태를 적용한다. 저장은 `state.tmp`에 먼저 쓰고 교체한다. 읽기·쓰기 오류는 안내하고 종료 시 `finally`에서 저장을 시도한다. 손상 파일로 시작한 후 저장하면 기본 데이터로 덮어쓰므로 중요한 기록은 백업해야 한다.

**확인:** 검증 폴더에서 6번째 문제와 83.33점 기록을 저장한 뒤 재실행해 복원했다. 파일 누락·손상·저장 실패 및 원인 제거 후 재저장도 확인했다.

프로젝트 루트에서 다음 명령으로 아래 재실행 로그 창을 연다.

```powershell
py docs/verification/view_log.py docs/verification/reload.txt
```

![재실행 후 문제 복원 실행 로그](docs/screenshots/reload.jpg)

### 11. 전체 기능 및 예외 처리 검증

필수 기능 완성 당시 기존 개발 화면을 확인하고, 동일 `main.py`를 임시 폴더에 복사해 검증했다. 입력과 `KeyboardInterrupt`·`EOFError`는 검증 코드에서 주입했다. 당시 **31개 확인 항목이 통과**했으며 결과는 [`results-required-v1.json`](docs/verification/results-required-v1.json)에 보존했다. 이후 보너스 구현에 맞춰 검증 코드를 확장했다. 현재 검증 결과는 아래 보너스 절과 `results.json`을 기준으로 한다.

| 검증 항목 | 결과 |
| --- | --- |
| 기본 문제·선택지·정답 범위, 정답·오답 판별 | 통과 |
| 메뉴·정답의 빈 입력, 공백, 문자, 범위 밖 숫자 처리 | 통과 |
| 빈 문제·선택지 재입력과 등록 | 통과 |
| 추가한 문제의 조회·출제와 점수 계산 | 통과 |
| 미플레이와 0점 구분, 최고 기록 갱신·유지 | 통과 |
| 재실행 후 퀴즈·최고 기록 복원 | 통과 |
| 메뉴·풀이·등록 중 중단·EOF, 미완성 데이터 제외 | 통과 |
| 파일 누락, JSON 문법·구조·점수 오류 복구 | 통과 |
| 쓰기 오류 안내 및 원인 제거 후 재저장 | 통과 |
| 빈 목록 처리와 스크립트 기준 저장 경로 | 통과 |

현재 검증 실행기: [`verify.py`](docs/verification/verify.py), 테스트: [`test_bonus.py`](docs/verification/test_bonus.py), 세부 결과: [`results.json`](docs/verification/results.json). 다음 명령으로 임시 폴더에서 재검증할 수 있다. 원래 게임 데이터는 변경하지 않는다.

```powershell
py docs/verification/verify.py
```

실제 터미널에서 입력 스트림 종료를 확인한 화면:

![Ctrl+Z 입력 종료](docs/screenshots/eof.png)

### 12. README와 실행 증거 정리

초기 문서에 남은 작성 안내 문구, 중복 제목, 이스케이프된 Markdown을 정리했다. 실제로 겪은 문제와 설계 시 고려한 문제를 구분하고 필수 설명·실행 증거를 보완했다.

바탕화면의 기존 스크린샷은 원본을 보존하고 `docs/screenshots`로 복사했다. 메뉴·환경·목록 전후·입력 오류·종료·Git 기록은 기존 화면을 사용했다. 부족한 등록·풀이·점수·재실행 이미지는 **실제 검증 실행 로그를 읽기 전용 창에 표시해 촬영**했다. 이 보완 화면은 새 GUI 게임이 아니다. 검증 입력값을 로그에 함께 표시했고 풀이 이미지는 마지막 문제와 결과를 발췌했다. 선택 강조와 마우스 포인터가 보이지 않도록 촬영했다.

로그 텍스트: [등록](docs/verification/add.txt), [풀이](docs/verification/play.txt), [점수](docs/verification/score.txt), [재실행](docs/verification/reload.txt).

#### 어떤 파일을 실행하고 촬영했는가

| 파일 | 역할 |
| --- | --- |
| [`main.py`](main.py) | 실제 콘솔 게임. 직접 입력하며 플레이할 때 실행 |
| [`verify.py`](docs/verification/verify.py) | 현재 게임 코드를 임시 폴더에서 검증하고 `bonus-*.txt` 실행 로그를 생성 |
| [`view_log.py`](docs/verification/view_log.py) | 저장된 UTF-8 로그를 `tkinter` 읽기 전용 창으로 표시 |
| `add.txt` | 퀴즈 등록과 잘못된 입력 재입력 로그 |
| `play.txt` | 마지막 문제 풀이와 최종 결과 발췌 |
| `score.txt` | 다시 실행한 뒤 최고 점수를 조회한 로그 |
| `reload.txt` | 다시 실행한 뒤 목록과 점수를 확인한 로그 |
| `results.json` | 검증 항목별 통과 여부 |

보완 촬영에는 `main.py`의 실제 실행 결과를 저장한 위 텍스트 파일을 사용했다. `view_log.py`는 `Path.read_text()`로 파일을 읽고, `tkinter`의 `Text` 위젯에 표시한 뒤 `state="disabled"`로 편집을 막고 `mainloop()`로 창을 유지한다. 화면의 선택 강조 없이 촬영했다. 저장소에 포함한 뷰어에는 긴 로그를 끝까지 볼 수 있도록 가로·세로 스크롤바도 추가했다.

#### 로그 창 여는 방법

1. VS Code에서 **`Codyssey_mission2` 프로젝트 폴더**를 연다.
2. **터미널 → 새 터미널**을 선택한다. 아래 명령은 `main.py`와 `README.md`가 있는 프로젝트 루트에서 실행한다.
3. 보고 싶은 로그에 해당하는 명령 하나를 실행한다.

```powershell
# 퀴즈 등록 로그
py docs/verification/view_log.py docs/verification/add.txt

# 마지막 문제와 풀이 결과
py docs/verification/view_log.py docs/verification/play.txt

# 최고 점수 조회
py docs/verification/view_log.py docs/verification/score.txt

# 재실행 후 저장 데이터 확인
py docs/verification/view_log.py docs/verification/reload.txt
```

창이 열리면 스크롤로 내용을 확인하고 오른쪽 위 닫기 버튼으로 종료한다. 환경에 따라 맨 앞의 `py`를 `python` 또는 `python3`로 바꾼다. `tkinter`가 포함된 Python과 그래픽 화면을 사용할 수 있는 환경이 필요하며, 표준 Windows Python 환경에서는 별도 pip 패키지가 필요 없다. `No module named tkinter` 오류가 나오면 Python 설치 구성에서 Tcl/Tk 지원을 확인한다.

위 명령은 **기존 로그를 보여줄 뿐 게임을 새로 실행하거나 점수를 변경하지 않는다.** 실제로 직접 게임을 하려면 `py main.py`를 실행한다.

#### 로그를 새로 생성하는 방법

같은 프로젝트 루트에서 검증 코드를 먼저 실행한다.

```powershell
py docs/verification/verify.py
```

검증은 게임 코드를 임시 폴더에 복사해 수행하며 원본 `state.json`은 유지한다. 현재 실행기는 `docs/verification`의 `bonus-play.txt`, `bonus-history.txt`, `bonus-add.txt`, `bonus-delete.txt`, `bonus-reload.txt`와 `results.json`을 새 결과로 덮어쓴다. 기존 네 로그(`add.txt` 등)는 필수 기능 당시 기록으로 보존한다. 새 로그는 아래 보너스 절의 명령으로 연다. 텍스트를 재생성해도 스크린샷은 자동 갱신되지 않으므로 새 결과는 다시 촬영해야 한다.

### 13. 저장소 clone 및 pull 실습

**진행:** 별도 `Codyssey_mission2_clone` 폴더에 복제하고 README를 수정해 커밋·푸시했다. 기존 폴더에서 원격 변경을 가져와 반영을 확인했다.

```powershell
# 기존 프로젝트의 상위 폴더에서
git clone https://github.com/20222002-ch/Codyssey_mission2.git Codyssey_mission2_clone
cd Codyssey_mission2_clone
# README 수정 후
git add README.md
git commit -m "Docs: 복제한 저장소에서 Git 동기화 실습 기록 추가"
git push origin main

# 기존 폴더에서 원격 변경 반영
cd ..\Codyssey_mission2
git pull --ff-only origin main
```

**확인:** 복제 폴더 reflog에 clone 기록과 README 수정 커밋 [`5d14ece`](https://github.com/20222002-ch/Codyssey_mission2/commit/5d14ece)가 있다. 기존 폴더 reflog에는 해당 커밋을 가져온 `pull --ff-only origin main: Fast-forward`가 있다. 이후 실습 결과를 [`b0c911c`](https://github.com/20222002-ch/Codyssey_mission2/commit/b0c911c)에 기록했다.

**정리한 개념:** `clone`은 새 폴더에 저장소를 복제하고 `pull`은 기존 저장소에 원격 변경을 반영한다. 두 폴더 사이에 파일을 직접 복사하지 않아도 같은 커밋을 공유할 수 있다.

### Git 조회 화면에서 겪은 문제

`git diff` 후 명령 입력으로 돌아오지 못했다. 내용이 길 때 열리는 pager의 `(END)` 화면이었고 영문 `q`로 종료했다. 이후 로그를 한 번에 확인할 때는 `git --no-pager log --oneline --graph --all`을 사용했다.

![git diff 조회 화면](docs/screenshots/git-diff.png)

## Git 변경 이력

### 커밋 단위와 메시지 규칙

이 프로젝트는 **하나의 기능 또는 하나의 작업 목적을 한 커밋으로 기록**한다. 메뉴, Quiz 클래스, 기본 문제, 출제, 추가, 목록, 점수, 저장·불러오기처럼 기능 단위로 나누며, 오류 수정·구조 정리·검증·문서 작성도 각각 작업 목적에 따라 구분한다. 관련 없는 변경을 한 커밋에 섞지 않고, 같은 기능을 완성하는 데 필요한 코드와 직접 관련된 설명은 함께 기록할 수 있다.

커밋 전에는 해당 작업을 실행하거나 검증하고, `git diff`로 변경 범위를 확인한 뒤 필요한 파일만 `git add`한다. 변경 내용 없이 개수만 채우는 커밋은 만들지 않는다.

커밋 제목은 다음 형식으로 작성한다.

```text
유형: 변경 내용을 구체적으로 요약
```

유형은 아래 영문 표기를 사용하며, 콜론 뒤에 공백 한 칸과 한국어 변경 요약을 적는다. `수정`, `작업 완료`처럼 대상을 알 수 없는 문구 대신 무엇을 구현·수정했는지 드러낸다.

| 유형 | 사용하는 작업 | 이 프로젝트의 예시 |
| --- | --- | --- |
| `Feat` | 새로운 기능 추가 | `Feat: 퀴즈 출제와 정답 입력 및 결과 표시 구현` |
| `Fix` | 오류 수정 또는 기존 동작 변경 | `Fix: 힌트 감점을 5점으로 변경하고 기존 점수 기록 호환 유지` |
| `Refactor` | 기능을 유지하면서 코드 구조 개선 | `Refactor: QuizGame 클래스로 게임 상태와 진행 관리` |
| `Test` | 테스트 추가·수정 | `Test: 보너스 기능과 기존 데이터 호환 및 종료 처리 검증` |
| `Docs` | README, 개발 기록, 실행 증거 정리 | `Docs: 각 실행 로그 이미지 바로 위에 열기 명령 추가` |
| `Chore` | 초기 환경 구성 등 개발 준비 | `Chore: 퀴즈 게임 개발 환경 및 초기 파일 구성` |
| `Merge` | 작업 브랜치를 합친 병합 기록 | `Merge: 퀴즈 풀기 기능 브랜치 병합` |

저장소 생성 시 자동으로 만들어진 `Initial commit`은 초기 이력으로 유지하고, 이후 작업 커밋에는 위 규칙을 적용한다. 여러 줄의 설명이 필요한 변경은 제목 아래 빈 줄을 두고 변경 이유와 확인 결과를 본문에 덧붙인다.

### 개발 이력 확인

문서 최종 정리 직전 총 15개 커밋이며 병합을 제외하면 14개다. 메뉴, 클래스, 기본 데이터, 출제, 등록, 목록, 점수, 구조 정리, 파일 입출력 등을 기능별로 커밋했다. 아래 이미지는 `b0c911c`까지의 개발 기록이며 이후 문서 정리 커밋은 포함하지 않는다.

![개발 커밋과 병합 그래프](docs/screenshots/git-log.png)

| 명령 | 역할 |
| --- | --- |
| `init` | 로컬 저장소 초기화 |
| `add` | 다음 커밋에 포함할 변경 선택 |
| `commit` | 변경 이력 기록 |
| `push` | 로컬 커밋을 GitHub로 전송 |
| `checkout` | 브랜치 생성·이동 |
| `merge` | 작업 브랜치 병합 |
| `clone` | 새 폴더에 원격 저장소 복제 |
| `pull` | 기존 저장소에 원격 변경 반영 |

## 실행 방법

Python 3.10 이상이 필요하다. 별도 패키지 설치는 필요 없다.

```powershell
git clone https://github.com/20222002-ch/Codyssey_mission2.git
cd Codyssey_mission2
py main.py
```

환경에 따라 `python main.py` 또는 `python3 main.py`를 사용한다. 번호로 메뉴를 선택하고 5번으로 종료한다. `state.json`이 있으면 저장 데이터를, 없으면 기본 5문제를 사용한다. 기존 저장 파일은 삭제할 필요가 없다.

퀴즈 풀기를 선택하면 풀 문제 수를 입력한다. `0`은 시작 취소이며, 출제 중 `h`로 힌트를 볼 수 있다. 6번은 삭제, 7번은 게임 기록 조회다.

## 기능 목록

| 메뉴 | 기능 |
| --- | --- |
| 1. 퀴즈 풀기 | 문제 수 선택 후 중복 없이 랜덤 출제, 힌트 및 결과 안내 |
| 2. 퀴즈 추가 | 문제·선택지 4개·정답 번호·선택적 힌트 입력 후 저장 |
| 3. 퀴즈 목록 | 등록된 문제 수와 제목 조회 |
| 4. 점수 확인 | 최고 점수와 당시 정답 수·문제 수 조회 |
| 5. 종료 | 현재 데이터 저장 시도 후 종료 |
| 6. 퀴즈 삭제 | 문제 선택과 y/n 확인 후 삭제·저장, 0으로 취소 |
| 7. 점수 히스토리 | 모든 완료 게임의 날짜·시간·문제 수·정답 수·점수·힌트 사용을 최신순 조회 |

잘못된 입력, 빈 목록, 파일 누락·손상, 읽기·쓰기 오류와 입력 중단을 처리한다. 랜덤 출제·문제 수 선택·힌트·삭제·점수 히스토리 보너스 5가지를 모두 제공한다.

## 파일 구조

```text
Codyssey_mission2/
├── docs/
│   ├── screenshots/       # 개발 화면과 보완 실행 로그 이미지
│   └── verification/
│       ├── verify.py      # 임시 폴더에서 게임 검증 및 로그 생성
│       ├── test_bonus.py  # 기존 기능 및 보너스 회귀 테스트
│       ├── view_log.py    # 저장된 로그를 읽기 전용 창으로 표시
│       ├── results.json   # 검증 항목별 결과
│       ├── results-required-v1.json # 필수 기능 당시 31개 검증 결과
│       ├── bonus-*.txt    # 현재 보너스 기능 실행 로그 5개
│       ├── add.txt        # 등록 로그
│       ├── play.txt       # 마지막 문제와 결과 발췌
│       ├── score.txt      # 최고 점수 조회 로그
│       └── reload.txt     # 재실행 후 조회 로그
├── .gitignore
├── README.md
├── main.py                # Quiz, QuizGame, 입력·출력 및 실행 함수
└── state.json             # 퀴즈와 최고 기록
```

`state.tmp`는 저장 시 사용하는 임시 파일이다. 캐시, 가상환경, 임시 파일과 `state.backup.json`은 Git 관리에서 제외한다.

## 요구사항 변경 시 수정 가이드

### 수정 대상 파일과 관련 함수·메서드 매핑

게임 구현은 [`main.py`](main.py)에 있다. 아래 표는 요구사항이 바뀌었을 때 **어느 파일의 어느 함수·메서드를 먼저 수정하고, 무엇을 함께 확인해야 하는지** 정리한 변경 매뉴얼이다. `QuizGame.add_quiz()` 같은 클래스 메서드와 `add_quiz()` 같은 파일 수준 함수는 서로 다른 수정 대상이다.

| 변경할 요구사항 | 수정 대상 파일 | 관련 함수·메서드·상수 | 함께 확인할 영향 범위 |
| --- | --- | --- | --- |
| 메뉴 항목·번호 추가 또는 변경 | `main.py` | `show_menu()`, `read_menu_choice()`, `QuizGame.run()` | 표시 문구, 허용 번호 범위, 실제 실행 분기를 함께 변경. 기존 5번 종료 동작과 README 기능 목록 확인 |
| 기본 문제·주제 변경 | `main.py` | `create_default_quizzes()`, `QuizGame.parse_state()` | 문제·선택지·정답·힌트를 함께 검토. 기본 힌트는 문제 문장으로 연결되며 기존 `state.json`이 있으면 저장된 문제가 우선됨 |
| 퀴즈 속성 추가 또는 선택지 수 변경 | `main.py` | `Quiz.__init__()`, `Quiz.display()`, `Quiz.check_answer()`, `create_default_quizzes()`, `add_quiz()`, `read_answer()`, `read_quiz_answer()`, `QuizGame.parse_state()`, `QuizGame.save_state()` | 입력, 객체 생성, 정답 범위, JSON 읽기·쓰기를 함께 맞춤. 기존 파일에서 새 속성이 없을 때의 기본값과 README 스키마 확인 |
| 문제 등록 흐름 변경 | `main.py` | `read_non_empty_text()`, `read_answer()`, `add_quiz()`, `QuizGame.add_quiz()` | 모든 입력 완료 후 등록되는지, 취소된 문제가 남지 않는지, 등록 직후 저장되는지 확인 |
| 목록 표시 방식 변경 | `main.py` | `show_quiz_list()`, `QuizGame.show_quiz_list()`, `QuizGame.delete_quiz()` | 삭제에서도 같은 목록을 사용하므로 화면의 번호와 실제 삭제 인덱스가 일치하는지 확인 |
| 출제 수·랜덤 출제 방식 변경 | `main.py` | `read_number()`, `play_quizzes()`, `QuizGame.play()` | 빈 목록, 시작 취소, 중복 출제, 원본 목록 순서, 결과의 `total` 확인. 히스토리의 문제 수와 점수 분모도 함께 확인 |
| 힌트 입력·조회 방식 변경 | `main.py` | `Quiz.__init__()`, `create_default_quizzes()`, `add_quiz()`, `read_quiz_answer()`, `play_quizzes()` | 힌트 없음·반복 조회·중간 취소 처리와 `hints_used` 집계, JSON의 `hint` 호환 확인 |
| 점수 계산·힌트 감점 변경 | `main.py` | `HINT_PENALTY`, `calculate_score()`, `play_quizzes()`, `QuizGame.play()`, `QuizGame.parse_record()`, `show_best_score()`, `QuizGame.show_history()` | 계산·표시·최고 기록 비교뿐 아니라 저장된 `hint_penalty` 검증도 확인. 과거 기록의 감점 기준을 새 기준으로 덮어쓰지 않음 |
| 최고 기록 갱신 기준 변경 | `main.py` | `QuizGame.play()`, `show_best_score()`, `QuizGame.show_best_score()`, `QuizGame.parse_record()` | 미플레이 `None`, 실제 0점, 동점 처리, 정답 수·문제 수·감점 기준과 점수의 일관성 확인 |
| 삭제·확인·취소 방식 변경 | `main.py` | `QuizGame.delete_quiz()`, `read_number()`, `show_quiz_list()`, `QuizGame.save_state()` | y/n 확인, 0 취소, 마지막 문제 삭제, 저장 실패 시 원래 위치 복원, 과거 점수 보존 확인 |
| 히스토리 항목·정렬·날짜 형식 변경 | `main.py` | `QuizGame.play()`, `QuizGame.show_history()`, `QuizGame.parse_record()`, `QuizGame.parse_state()`, `QuizGame.save_state()` | 새 기록 생성·조회·불러오기·저장 모두 반영. 시간대와 누락 필드의 호환, 완료한 게임만 기록되는지 확인 |
| 파일 경로·JSON 키·스키마·오류 복구 변경 | `main.py` | `QuizGame.__init__()`, `QuizGame.load_state()`, `QuizGame.parse_state()`, `QuizGame.parse_record()`, `QuizGame.save_state()`, `main()` | UTF-8, 프로젝트 루트 경로, 임시 파일 교체, 누락·손상·읽기·쓰기 오류, 종료 시 저장과 구형 파일 복원 확인 |
| 입력 검증·안전한 종료 변경 | `main.py` | `read_menu_choice()`, `read_answer()`, `read_number()`, `read_non_empty_text()`, `read_quiz_answer()`, `main()`과 파일 끝의 예외 처리 | 공백·빈 입력·문자·범위 밖 숫자, Ctrl+C·EOF, 미완성 문제·미완료 게임 제외와 `finally` 저장 확인 |
| 자동 검증·재현 로그 변경 | `docs/verification/test_bonus.py`, `docs/verification/verify.py` | `QuizTests`의 관련 `test_*()` 메서드, `session()`, `create_demo_logs()`, `main()` | 새 프롬프트에 맞는 입력 순서와 기대 결과 수정. 실제 프로세스 테스트 및 원본 데이터 보존 확인, 필요한 로그만 재생성 |
| 로그 창·실행 증거 변경 | `docs/verification/view_log.py`, `README.md`, `docs/screenshots/` | 뷰어의 `main()`, README 이미지 위 실행 명령과 상대 경로 | 읽기 전용·스크롤 동작, 파일 존재, 이미지와 로그의 버전 일치 확인. 로그를 생성해도 이미지는 자동 갱신되지 않음 |

`state.json`은 실행 중 생성·갱신되는 사용자 데이터다. 요구사항 변경을 적용하기 위해 기록을 일괄 삭제하거나 직접 덮어쓰지 않고, 위 읽기·검증·저장 메서드에서 구형 데이터의 기본값 또는 변환 규칙을 마련한다. `docs/verification/results.json`과 `bonus-*.txt`도 검증 실행기가 만드는 결과 파일이며 수동으로 통과 결과를 작성하지 않는다.

### 변경 영향 범위를 줄이는 작업 절차

1. **변경 전 확인:** `git status`와 현재 실행 결과를 확인하고, 사용자 데이터가 필요한 경우 `state.json`을 `state.backup.json`으로 복사한다. 백업은 Git에서 제외한다.
2. **수정 범위 선택:** 위 표에서 해당 요구사항의 파일과 함수·메서드를 고른다. 입력 → 객체 → 게임 진행 → 저장·복원 → 출력 순서로 연결된 부분을 확인하고, 관련 없는 기능은 수정 범위에서 제외한다.
3. **기존 동작 보호:** 관련 회귀 테스트를 먼저 확인하고 새 기준의 기대값을 정한다. 데이터 필드나 점수 기준이 바뀌면 구형 저장 파일과 새 파일을 모두 읽는 테스트를 포함한다.
4. **작업 브랜치에서 수정:** 하나의 요구사항 변경을 한 작업 단위로 구현한다. 문구만 바뀌는 경우에는 계산·저장 구조를 바꾸지 않는다. 저장 구조가 바뀌면 `parse_state()`·`parse_record()`·`save_state()`를 함께 점검한다.
5. **검증:** 아래 명령으로 41개 회귀 테스트를 실행한다. 이 명령은 로그·이미지를 다시 만들지 않고 임시 폴더에서 게임을 검사한다. 잘못된 입력, 취소, EOF, 재실행과 기존 기록 보존도 확인한다.

   ```powershell
   py -m unittest discover -s docs/verification -p test_bonus.py -v
   ```

6. **설명과 증거 동기화:** README의 기능 목록·필드 설명·사용법을 실제 동작에 맞춘다. 실행 결과가 바뀌면 `py docs/verification/verify.py`로 결과와 보너스 로그를 갱신하고 해당 스크린샷도 다시 촬영한다. 이전 개발 기록은 당시 버전임을 표시해 보존한다.
7. **커밋과 병합:** `git diff`와 `git diff --check`로 변경을 확인하고 수정한 파일만 스테이징한다. 위 커밋 규칙에 맞춰 기록한 뒤 병합·푸시하고 GitHub의 README 링크와 파일 반영을 확인한다.

### 변경 예시: 힌트 감점 10점에서 5점으로 조정

- **변경한 코드:** `main.py`의 `HINT_PENALTY`와 `calculate_score()`를 기준으로 새 게임 점수를 계산하고, `play_quizzes()`의 반환값에 `hint_penalty`를 저장했다. `QuizGame.parse_record()`는 새 5점 기준과 예전 10점 기준을 구분해 검증하도록 변경했다.
- **유지한 동작:** `QuizGame.play()`의 최고 점수 비교와 히스토리 저장 흐름을 확인하되, 기존 사용자 문제·날짜·점수를 소급 수정하지 않았다. `show_best_score()`·`QuizGame.show_history()`는 저장된 점수를 그대로 표시한다.
- **검증한 위치:** `docs/verification/test_bonus.py`의 `test_hint_scoring_and_zero_floor()`, `test_hint_repeated_once_and_case_insensitive()`, `test_hint_penalty_and_history_survive_restart()`, `test_old_ten_point_records_and_new_five_point_records_coexist()`에서 계산·중복 조회·재실행·구형 기록 호환을 확인했다.
- **함께 갱신한 파일:** `README.md`, `docs/verification/results.json`, 영향을 받는 `bonus-*.txt`, `docs/screenshots/bonus-*.jpg`를 맞췄다. 게임과 무관한 로그 뷰어 코드는 수정할 필요가 없었다.

## 데이터 파일 설명

- **경로:** `main.py`와 같은 프로젝트 루트의 `state.json`
- **인코딩:** UTF-8. `ensure_ascii=False`로 한글을 읽을 수 있게 저장
- **저장:** 등록 후, 게임 완료 후, 정상 종료 또는 입력 중단 시 저장 시도
- **불러오기:** 시작 시 JSON과 필드 구조를 검사한 뒤 상태에 반영

| 필드 | 내용 |
| --- | --- |
| `quizzes` | 퀴즈 목록. 빈 목록도 허용 |
| `question` | 비어 있지 않은 문제 문자열 |
| `choices` | 비어 있지 않은 선택지 문자열 4개 |
| `answer` | 1~4의 정수 정답 번호 |
| `best_score` | 미플레이는 `null`, 완료 기록은 아래 객체 |
| `hint` | 선택적 힌트 문자열. 빈 문자열이면 힌트 없음 |
| `score` | 정답 비율 × 100 - 힌트 사용 문제 수 × 해당 기록의 hint_penalty (현재 5), 최소 0점, 소수점 둘째 자리 반올림 |
| `correct_count` | 최고 기록의 정답 수 |
| `total` | 최고 기록의 전체 문제 수 |
| `hints_used` | 해당 게임에서 힌트를 사용한 문제 수 |
| `hint_penalty` | 해당 기록의 힌트 1회 감점. 현재 5점, 이전 기록은 10점 |
| `history` | 완료한 모든 게임 기록의 목록 |
| `played_at` | 히스토리의 실행 컴퓨터 현지 시각. 시간대가 포함된 ISO 8601 문자열 |

필드 구조 예시이며 실제 파일에는 전체 문제가 들어간다.

```json
{
  "quizzes": [
    {
      "question": "Python에서 문자열을 나타내는 자료형은?",
      "choices": ["int", "str", "bool", "list"],
      "answer": 2,
      "hint": "string의 약자입니다."
    }
  ],
  "best_score": {"score": 95.0, "correct_count": 1, "total": 1, "hints_used": 1, "hint_penalty": 5},
  "history": [
    {"score": 95.0, "correct_count": 1, "total": 1, "hints_used": 1, "hint_penalty": 5, "played_at": "2026-11-08T20:00:00+09:00"}
  ]
}
```

파일이 없거나 손상되면 기본 5문제와 미플레이 상태로 시작한다. 저장 실패 시 안내하고 실행 중 데이터는 메모리에 유지한다. 등록 도중 취소한 문제와 미완료 게임 결과는 기록에 반영하지 않는다.

**기존 파일 호환:** `history`가 없으면 빈 목록, 기록에 `hints_used`가 없으면 0으로 읽는다. 퀴즈의 `hint`가 누락되면 기본 문제는 문제 문장이 일치하는 기본 힌트로 보완하고 사용자 문제는 힌트 없이 읽는다. 사용자가 명시적으로 저장한 빈 힌트는 유지한다. 예전 최고 점수는 보존하며 날짜를 알 수 없는 예전 기록을 히스토리로 만들어 넣지는 않는다. 실제 저장은 다음 등록·완료·종료 시 새 구조로 이루어진다.

### JSON 저장 방식의 한계와 확장 방향

현재는 문제 수가 적고 한 사용자가 실행하는 콘솔 게임이므로, 별도 설치 없이 내용을 확인할 수 있는 JSON 파일을 사용했다. 다만 데이터가 많아지면 다음 한계가 있다.

| 구분 | 현재 구현의 한계 |
| --- | --- |
| 읽기 성능 | 시작할 때 `json.load()`로 파일 전체를 읽고 모든 퀴즈와 게임 기록을 검증한다. 문제 한 개나 최근 기록만 필요해도 전체 데이터를 처리한다. |
| 쓰기 성능 | 문제 하나를 추가하거나 게임 한 번을 완료해도 `save_state()`는 전체 목록과 기록을 다시 JSON으로 저장한다. 파일이 커질수록 직렬화와 디스크 쓰기 시간이 늘어난다. 종료 시에도 저장하므로 데이터가 크면 종료가 지연될 수 있다. |
| 메모리 부담 | 퀴즈와 전체 히스토리를 실행 중 메모리에 유지한다. 불러올 때는 JSON 딕셔너리와 복원 중인 객체가, 저장할 때는 기존 객체와 저장용 딕셔너리·리스트가 함께 존재해 추가 메모리가 필요하다. 특히 히스토리는 완료할 때마다 계속 늘어난다. |
| 조회·동시 사용 | 날짜별 검색이나 통계는 목록을 순회해야 한다. 여러 프로그램이 같은 파일을 동시에 수정하면 나중에 저장한 내용이 앞선 변경을 덮어쓸 수 있다. |

임시 파일을 먼저 작성한 뒤 교체하는 방식은 저장 중 원본이 일부만 덮어써지는 위험을 줄이지만, 전체 파일을 읽고 쓰는 비용이나 여러 실행 간 동시 수정 충돌을 해결하지는 않는다.

**확장 대안:** 문제와 기록이 많아지면 표준 라이브러리 `sqlite3`를 이용해 SQLite로 옮길 수 있다. 퀴즈와 게임 기록을 각각 테이블로 나누고, 등록·삭제·게임 완료 시 필요한 행만 변경한다. 날짜 인덱스와 `ORDER BY`, `LIMIT`을 사용하면 최신 기록을 필요한 개수만 조회할 수 있어 전체 히스토리를 메모리에 올리는 부담도 줄일 수 있다. 트랜잭션으로 관련 변경을 묶어 저장할 수 있지만, SQLite도 여러 쓰기 작업을 동시에 처리하는 데 제약이 있으므로 다중 사용자 서비스로 커지면 서버형 데이터베이스를 검토한다.

JSON을 유지하는 단계에서는 오래된 히스토리 분리 보관이나 저장 데이터 분할을 고려할 수 있다. 실제 전환 시점은 임의의 문제 개수로 정하기보다 시작·저장 시간과 메모리 사용량을 측정해 판단한다. 현재 버전에는 이 확장 대안을 구현하지 않았으며, 미션의 `state.json` 저장 규칙을 유지한다.

## 보너스 과제 개발 과정

필수 개발 기록을 유지하기 위해 `codex/bonus-features` 브랜치에서 기능별로 작업했다. 원래 `state.json`을 덮어쓰지 않고 임시 폴더에서 기존 형식과 새 형식을 모두 검증했다.

### B1. 랜덤 출제와 문제 수 선택

**구현:** 퀴즈가 있으면 1~전체 문제 수를 선택하고 `random.sample(quizzes, total)`로 중복 없이 뽑는다. 0은 취소다. 빈 입력·문자·음수·범위 초과를 재입력하게 했다. 기능 커밋: [`55ecf60`](https://github.com/20222002-ch/Codyssey_mission2/commit/55ecf60).

**고려와 해결:** 원본 목록을 직접 섞으면 목록 순서와 삭제 번호도 달라진다. 별도 표본 리스트를 사용해 원본은 유지했다. 무작위 기능을 검증할 때는 특정 출제 순서를 지정한 테스트와 실제 `random.sample`의 중복 없는 표본 테스트를 나눴다. 실행 로그 생성에만 seed 17을 사용하며 실제 게임은 seed를 고정하지 않는다.

### B2. 힌트와 감점

**구현:** `Quiz.hint`를 추가하고 등록 시 Enter로 생략할 수 있게 했다. 풀이 중 `h` 또는 `H`로 조회한다. 힌트를 사용한 문제마다 최종 점수에서 5점을 차감하고 0점 미만으로 내려가지 않는다. 같은 문제에서 반복 조회해도 한 번만 차감하며, 힌트가 없는 문제는 차감하지 않는다. 기능 커밋: [`14d89ae`](https://github.com/20222002-ch/Codyssey_mission2/commit/14d89ae).

**고려와 해결:** 기존 최고 기록 검증은 정답 비율만 계산했기 때문에 감점된 기록을 손상 데이터로 처리할 수 있었다. 저장·불러오기와 점수 계산이 같은 `calculate_score()`를 사용하도록 바꾸고 `hints_used`를 함께 저장했다. 힌트 횟수가 없는 예전 기록은 0회로 해석한다. 이후 사용자 요청으로 감점을 10점에서 5점으로 줄였다. 새 기록은 `hint_penalty: 5`를 저장하고, 감점 필드가 없는 기존 보너스 기록은 10점 기준으로 읽어 원래 점수와 날짜를 보존한다. 과거 기록을 소급해서 다시 계산하지 않는다.

**확인:** 3문제 전부 정답에 힌트 1회면 95점, 같은 힌트를 두 번 확인해도 95점이다. 오답과 힌트 감점이 겹쳐도 최소 0점이다. 아래 화면은 문제 수 입력 검증과 첫 문제의 반복 힌트 확인 부분이다. 스크롤하면 최종 95점 결과까지 볼 수 있다.

```powershell
py docs/verification/view_log.py docs/verification/bonus-play.txt
```

![문제 수 선택과 힌트 반복 조회 로그](docs/screenshots/bonus-play.jpg)

### B3. 퀴즈 삭제

**구현:** 메뉴 6번에서 목록과 문제 번호를 보여주고 `y/n`으로 다시 확인한다. 0 또는 n은 취소하며 y일 때만 삭제하고 저장한다. 마지막 문제를 삭제한 빈 목록도 다시 실행했을 때 유지한다. 기능 커밋: [`73c2efe`](https://github.com/20222002-ch/Codyssey_mission2/commit/73c2efe).

**고려와 해결:** 메모리에서만 지워진 뒤 저장에 실패하면 재실행 결과가 달라진다. 저장 실패 시 같은 객체를 원래 인덱스에 다시 넣고 삭제 취소를 안내하도록 했다. 이미 완료한 점수와 히스토리는 과거 기록이므로 문제 삭제 후에도 보존한다.

```powershell
py docs/verification/view_log.py docs/verification/bonus-delete.txt
```

![문제 선택과 삭제 확인 및 저장 로그](docs/screenshots/bonus-delete.jpg)

### B4. 점수 히스토리

**구현:** 게임을 끝까지 완료할 때마다 `history`에 결과와 `datetime.now().astimezone().isoformat()` 날짜를 추가한다. 메뉴 7번은 최신순으로 날짜·시간대, 문제 수, 정답 수, 점수, 힌트 횟수를 표시한다. 새 최고 점수가 아닌 게임도 남긴다. 기능 커밋: [`73c2efe`](https://github.com/20222002-ch/Codyssey_mission2/commit/73c2efe).

**고려와 해결:** 취소하거나 중단한 게임을 기록하지 않도록 결과를 받은 뒤에만 추가한다. 과거 기록의 문제 수를 현재 목록 개수와 비교하지 않아 문제 삭제 후에도 유효하게 불러온다. 시간대 없는 날짜나 잘못된 점수·힌트 횟수는 검증에서 거른다.

```powershell
py docs/verification/view_log.py docs/verification/bonus-history.txt
```

![재실행 후 날짜와 점수 히스토리 조회 로그](docs/screenshots/bonus-history.jpg)

힌트 포함 문제 등록과 삭제 후 재실행도 로그로 확인할 수 있다.

```powershell
py docs/verification/view_log.py docs/verification/bonus-add.txt
py docs/verification/view_log.py docs/verification/bonus-reload.txt
```

### B5. 회귀 검증과 재현

[`test_bonus.py`](docs/verification/test_bonus.py)의 **41개 테스트가 통과**했다. `results.json`에는 41개 테스트 결과와 원본 데이터 보존 확인 1개를 별도로 기록한다. 테스트 안의 여러 입력 조합은 subtest로 확인한다.

- 랜덤 표본 크기·중복·순서와 원본 목록 보존
- 문제 수 취소·잘못된 입력, 힌트 반복·없음·감점 하한
- 힌트 포함 등록과 구형 저장 파일의 최고 기록·사용자 문제 보존
- 최고 점수 갱신·동점·낮은 점수 유지와 모든 완료 게임 기록
- 삭제 확인·취소·저장 실패 복원·마지막 문제 삭제 후 재실행
- 메뉴·문제 수·풀이·등록·삭제 확인 도중 Ctrl+C·EOF에 해당하는 예외
- 손상 데이터·파일 읽기·쓰기 오류와 재저장
- 실제 Python 프로세스에서 게임·힌트·히스토리·재실행 및 EOF 종료

```powershell
py docs/verification/verify.py
```

검증 결과와 보너스 로그는 재생성되며 현재 게임 데이터는 변경하지 않는다. 새 보너스 이미지 3장은 기존과 같은 읽기 전용 로그 창을 촬영했다. 필수 기능 당시 스크린샷·로그는 개발 이력으로 유지하며 현재 화면과 메뉴·프롬프트가 다를 수 있다.

[^question-count]: ‘기본 문제 수’, ‘등록된 전체 문제 수’, ‘이번 게임의 출제 수’는 각각 다른 개념이다. 현재 출제 수 선택은 [B1. 랜덤 출제와 문제 수 선택](#b1-랜덤-출제와-문제-수-선택)에서 구현했다. 문제를 추가해도 매번 전체를 풀 필요는 없다.

[^play-snapshot]: `docs/verification/play.txt`와 해당 이미지는 문제 추가·저장까지 연결한 필수 기능 버전의 검증 기록이다. 당시에는 전체 6문제를 풀었고 힌트 감점은 없었다. 현재 동작은 [B1. 출제 수 선택](#b1-랜덤-출제와-문제-수-선택)과 [B2. 힌트와 감점](#b2-힌트와-감점), 최신 검증은 [B5. 회귀 검증과 재현](#b5-회귀-검증과-재현)을 참고한다.
