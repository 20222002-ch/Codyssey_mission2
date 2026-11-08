"""Run regression checks and record bonus logs without changing project state."""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import random
import runpy
import shutil
import tempfile
import unittest
from unittest.mock import patch

from test_bonus import QuizTests

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({"name": test.id().split(".")[-1], "result": "PASS"})

    def addFailure(self, test, error):
        super().addFailure(test, error)
        self.records.append({"name": test.id(), "result": "FAIL"})

    def addError(self, test, error):
        super().addError(test, error)
        self.records.append({"name": test.id(), "result": "ERROR"})

    def addSubTest(self, test, subtest, error):
        super().addSubTest(test, subtest, error)
        if error is not None:
            self.records.append({"name": str(subtest), "result": "FAIL"})


def session(program, answers):
    values = iter(answers)
    stream = io.StringIO()
    def read(prompt=""):
        print(prompt, end="")
        value = next(values)  # A missing demo input is a verification error.
        print(value)
        return value
    with contextlib.redirect_stdout(stream), patch("builtins.input", read):
        runpy.run_path(str(program), run_name="__main__")
    return "\n".join(line.rstrip() for line in stream.getvalue().splitlines()) + "\n"


def create_demo_logs():
    with tempfile.TemporaryDirectory(prefix="mission2_bonus_demo_") as folder:
        program = Path(folder) / "main.py"
        shutil.copy2(ROOT / "main.py", program)
        with contextlib.redirect_stdout(io.StringIO()):
            definitions = runpy.run_path(str(program))
        quizzes = definitions["create_default_quizzes"]()
        selected = random.Random(17).sample(quizzes, 3)
        random_state = random.getstate()
        try:
            random.seed(17)
            answers = ["1", "", "abc", "6", "3", "h", "h"]
            answers += [str(q.answer) for q in selected]
            answers += ["5"]
            play = session(program, answers)
        finally:
            random.setstate(random_state)
        # Keep the selection, hint and results together without repeated menus.
        start = play.index("풀 문제 수")
        end = play.index("데이터를 저장했습니다.", start) + len("데이터를 저장했습니다.")
        logs = {
            "bonus-play": play[start:end] + "\n",
            "bonus-history": session(program, ["7", "4", "5"]),
            "bonus-add": session(program, ["2", "Python에서 반복을 즉시 종료하는 키워드는?", "break", "continue", "return", "pass", "1", "반복문 전체를 빠져나오는 키워드입니다.", "5"]),
            "bonus-delete": session(program, ["6", "2", "y", "5"]),
            "bonus-reload": session(program, ["3", "7", "4", "5"]),
        }
        for name, text in logs.items():
            (OUT / (name + ".txt")).write_text(text, encoding="utf-8")


def main():
    before = digest(ROOT / "state.json")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(QuizTests)
    result = unittest.TextTestRunner(verbosity=2, resultclass=RecordedResult).run(suite)
    if result.wasSuccessful():
        create_demo_logs()
    unchanged = digest(ROOT / "state.json") == before
    result.records.append({"name": "original_project_state_unchanged", "result": "PASS" if unchanged else "FAIL"})
    (OUT / "results.json").write_text(json.dumps(result.records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Checks: {result.testsRun}; original state unchanged: {unchanged}")
    if not result.wasSuccessful() or not unchanged:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
