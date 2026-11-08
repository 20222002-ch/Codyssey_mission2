"""Regression and bonus checks, isolated from the user's saved game."""

import contextlib
import copy
from datetime import datetime
import importlib.util
import io
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


class QuizTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="mission2_bonus_")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.program = self.directory / "main.py"
        shutil.copy2(ROOT / "main.py", self.program)
        spec = importlib.util.spec_from_file_location("checked_quiz", self.program)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.state = self.directory / "state.json"
        self.defaults = {
            "quizzes": [vars(q) for q in self.mod.create_default_quizzes()],
            "best_score": None,
        }

    def reset(self, data=None):
        self.state.write_text(json.dumps(self.defaults if data is None else data, ensure_ascii=False), encoding="utf-8")

    def call(self, function, answers=()):
        values = iter(answers)
        stream = io.StringIO()
        def read(prompt=""):
            print(prompt, end="")
            value = next(values, EOFError())
            if isinstance(value, BaseException):
                raise value
            print(value)
            return value
        with contextlib.redirect_stdout(stream), patch("builtins.input", read):
            result = function()
        return result, stream.getvalue()

    def game(self):
        return self.call(self.mod.QuizGame)[0]

    def run_session(self, answers):
        # Deterministic order for assertions; production uses random.sample.
        with patch.object(self.mod.random, "sample", side_effect=lambda values, k: list(values)[:k]):
            return self.call(lambda: runpy.run_path(str(self.program), run_name="__main__"), answers)[1]

    def saved(self):
        return json.loads(self.state.read_text(encoding="utf-8"))

    def test_default_quizzes(self):
        quizzes = self.mod.create_default_quizzes()
        self.assertGreaterEqual(len(quizzes), 5)
        self.assertTrue(all(len(q.choices) == 4 and 1 <= q.answer <= 4 and q.hint for q in quizzes))

    def test_quiz_display_and_answers(self):
        q = self.mod.Quiz("Question", ["A", "B", "C", "D"], 2)
        _, output = self.call(q.display)
        self.assertIn("1. A", output)
        self.assertIn("4. D", output)
        self.assertTrue(q.check_answer(2))
        self.assertFalse(q.check_answer(1))

    def test_menu_validation_and_bonus_numbers(self):
        for valid in (" 3 ", "6", "7", "5"):
            with self.subTest(valid=valid):
                value, _ = self.call(self.mod.read_menu_choice, ["", " ", "abc", "0", "8", valid])
                self.assertEqual(value, int(valid))

    def test_registration_answer_validation(self):
        value, _ = self.call(self.mod.read_answer, ["", " ", "abc", "0", "5", " 2 "])
        self.assertEqual(value, 2)

    def test_text_validation(self):
        value, _ = self.call(lambda: self.mod.read_non_empty_text("Q:"), ["", "  ", " text "])
        self.assertEqual(value, "text")

    def test_count_validation(self):
        value, _ = self.call(lambda: self.mod.read_number("count:", 0, 5), ["", " ", "abc", "1.5", "-1", "6", " 2 "])
        self.assertEqual(value, 2)

    def test_empty_play_and_list(self):
        for function in (self.mod.play_quizzes, self.mod.show_quiz_list):
            result, output = self.call(lambda: function([]))
            self.assertIsNone(result)
            self.assertIn("등록된 퀴즈가 없습니다", output)

    def test_count_cancel_has_no_result(self):
        result, _ = self.call(lambda: self.mod.play_quizzes(self.mod.create_default_quizzes()), ["0"])
        self.assertIsNone(result)

    def test_sample_uses_selected_count_and_keeps_original_order(self):
        quizzes = self.mod.create_default_quizzes()
        original = quizzes[:]
        selected = [quizzes[3], quizzes[0]]
        with patch.object(self.mod.random, "sample", return_value=selected) as sample:
            result, output = self.call(lambda: self.mod.play_quizzes(quizzes), ["2", "4", "2"])
        sample.assert_called_once_with(quizzes, 2)
        self.assertEqual(quizzes, original)
        self.assertEqual(result["score"], 100)
        self.assertLess(output.index(selected[0].question), output.index(selected[1].question))
        self.assertNotIn(quizzes[2].question, output)

    def test_real_random_sample_has_no_duplicates(self):
        quizzes = self.mod.create_default_quizzes()
        before = self.mod.random.getstate()
        try:
            self.mod.random.seed(17)
            selected = self.mod.random.sample(quizzes, len(quizzes))
        finally:
            self.mod.random.setstate(before)
        self.assertEqual(len({id(q) for q in selected}), len(quizzes))
        self.assertEqual(set(selected), set(quizzes))
        self.assertNotEqual(selected, quizzes)

    def test_hint_repeated_once_and_case_insensitive(self):
        q = self.mod.Quiz("Q", ["a", "b", "c", "d"], 1, "Hint")
        result, output = self.call(lambda: self.mod.read_quiz_answer(q), [" H ", "h", "1"])
        self.assertEqual(result, (1, True))
        self.assertEqual(output.count("최종 점수에서 5점 차감"), 1)
        self.assertIn("추가 감점은 없습니다", output)

    def test_missing_hint_is_free(self):
        q = self.mod.Quiz("Q", ["a", "b", "c", "d"], 1)
        result, output = self.call(lambda: self.mod.read_quiz_answer(q), ["h", "h", "1"])
        self.assertEqual(result, (1, False))
        self.assertIn("감점하지 않습니다", output)

    def test_play_answer_validation(self):
        q = self.mod.create_default_quizzes()[0]
        result, _ = self.call(lambda: self.mod.read_quiz_answer(q), ["", " ", "abc", "0", "5", " 2 "])
        self.assertEqual(result, (2, False))

    def test_hint_scoring_and_zero_floor(self):
        self.assertEqual(self.mod.calculate_score(2, 3, 1), 61.67)
        self.assertEqual(self.mod.calculate_score(0, 1, 1), 0)
        self.assertEqual(self.mod.calculate_score(1, 1, 1), 95)
        self.assertEqual(self.mod.calculate_score(2, 3), 66.67)

    def test_play_counts_hinted_questions(self):
        quizzes = self.mod.create_default_quizzes()
        with patch.object(self.mod.random, "sample", return_value=quizzes[:2]):
            result, _ = self.call(lambda: self.mod.play_quizzes(quizzes), ["2", "h", "h", "2", "h", "3"])
        self.assertEqual(result, dict(score=90, correct_count=2, total=2, hints_used=2, hint_penalty=5))

    def test_missing_file_and_exit_save(self):
        output = self.run_session(["4", "7", "5"])
        self.assertIn("저장 파일이 없어", output)
        self.assertIn("아직 퀴즈를 완료한 기록", output)
        self.assertIn("아직 완료한 게임 기록", output)
        self.assertEqual(len(self.saved()["quizzes"]), 5)

    def test_add_and_restart_with_hint(self):
        self.reset()
        self.run_session(["2", "", "Q", "", "a", "b", "c", "d", "0", "1", " Hint ", "5"])
        saved = self.saved()
        self.assertEqual(len(saved["quizzes"]), 6)
        self.assertEqual(saved["quizzes"][-1]["hint"], "Hint")
        self.assertIn("[6] Q", self.run_session(["3", "5"]))

    def test_optional_hint_may_be_empty(self):
        self.reset()
        self.run_session(["2", "Q", "a", "b", "c", "d", "1", "", "5"])
        self.assertEqual(self.saved()["quizzes"][-1]["hint"], "")

    def test_old_save_with_score_migrates_without_loss(self):
        legacy = copy.deepcopy(self.defaults)
        for q in legacy["quizzes"]:
            q.pop("hint")
        legacy["quizzes"].append(dict(question="Custom", choices=["a", "b", "c", "d"], answer=3))
        legacy["best_score"] = dict(score=80, correct_count=4, total=5)
        self.reset(legacy)
        game = self.game()
        self.assertEqual(len(game.quizzes), 6)
        self.assertEqual(game.best_score["score"], 80)
        self.assertEqual(game.best_score["hints_used"], 0)
        self.assertTrue(game.quizzes[0].hint)
        self.assertEqual(game.quizzes[-1].hint, "")
        self.assertEqual(game.history, [])
        self.call(game.save_state)
        again = self.game()
        self.assertEqual(again.quizzes[-1].answer, 3)
        self.assertEqual(again.best_score["score"], 80)

    def test_hint_penalty_and_history_survive_restart(self):
        self.reset()
        self.run_session(["1", "1", "h", "h", "2", "5"])
        game = self.game()
        self.assertEqual(game.best_score["score"], 95)
        self.assertEqual(game.history[0]["hints_used"], 1)
        self.assertIsNotNone(datetime.fromisoformat(game.history[0]["played_at"]).utcoffset())

    def test_zero_higher_equal_and_lower_records(self):
        self.reset()
        self.run_session(["1", "1", "1", "5"])
        self.assertEqual(self.saved()["best_score"]["score"], 0)
        self.run_session(["1", "1", "2", "5"])
        best = self.saved()["best_score"]
        self.assertEqual(best["score"], 100)
        self.run_session(["1", "1", "2", "5"])
        self.run_session(["1", "1", "1", "5"])
        self.assertEqual(self.saved()["best_score"], best)
        self.assertEqual(len(self.saved()["history"]), 4)

    def test_history_shows_latest_first(self):
        self.reset()
        game = self.game()
        game.history = [dict(score=0, correct_count=0, total=1, hints_used=0, played_at="2026-11-08T10:00:00+09:00"), dict(score=100, correct_count=1, total=1, hints_used=0, played_at="2026-11-08T11:00:00+09:00")]
        _, output = self.call(game.show_history)
        self.assertLess(output.index("11:00:00"), output.index("10:00:00"))
        self.assertIn("+09:00", output)

    def test_cancelled_start_adds_no_history(self):
        self.reset()
        self.run_session(["1", "0", "5"])
        self.assertEqual(self.saved()["history"], [])
        self.assertIsNone(self.saved()["best_score"])

    def test_interrupts_and_eof_preserve_completed_state(self):
        for error_type in (KeyboardInterrupt, EOFError):
            for inputs in ([], ["1"], ["1", "1", "h"], ["2", "partial"], ["2", "Q", "a", "b", "c", "d", "1"], ["6", "1"]):
                with self.subTest(error=error_type.__name__, inputs=inputs):
                    self.reset()
                    output = self.run_session([*inputs, error_type()])
                    self.assertIn("게임을 종료합니다", output)
                    saved = self.saved()
                    self.assertEqual(len(saved["quizzes"]), 5)
                    self.assertIsNone(saved["best_score"])
                    self.assertEqual(saved["history"], [])

    def test_delete_confirm_and_restart(self):
        self.reset()
        self.run_session(["6", "2", "y", "5"])
        game = self.game()
        self.assertEqual(len(game.quizzes), 4)
        self.assertNotIn(self.defaults["quizzes"][1]["question"], [q.question for q in game.quizzes])

    def test_delete_cancel_and_invalid_confirmation(self):
        for answers in (["6", "0", "5"], ["6", "1", "", "yes", " n ", "5"]):
            with self.subTest(answers=answers):
                self.reset()
                self.run_session(answers)
                self.assertEqual(len(self.saved()["quizzes"]), 5)

    def test_delete_count_validation(self):
        self.reset()
        self.run_session(["6", "", "abc", "-1", "6", " 1 ", " Y ", "5"])
        self.assertEqual(len(self.saved()["quizzes"]), 4)

    def test_delete_failure_restores_same_object_and_order(self):
        self.reset()
        game = self.game()
        original = game.quizzes[:]
        with patch.object(game, "save_state", return_value=False):
            _, output = self.call(game.delete_quiz, ["2", "y"])
        self.assertEqual(game.quizzes, original)
        self.assertIs(game.quizzes[1], original[1])
        self.assertIn("문제를 복원", output)

    def test_delete_last_preserves_empty_list_on_reload(self):
        data = copy.deepcopy(self.defaults)
        data["quizzes"] = data["quizzes"][:1]
        self.reset(data)
        self.run_session(["6", "1", "y", "5"])
        output = self.run_session(["1", "3", "6", "5"])
        self.assertEqual(self.saved()["quizzes"], [])
        self.assertEqual(output.count("등록된 퀴즈가 없습니다"), 3)

    def test_delete_keeps_historical_score_and_count(self):
        self.reset()
        self.run_session(["1", "1", "2", "6", "1", "y", "5"])
        game = self.game()
        self.assertEqual(game.best_score["total"], 1)
        self.assertEqual(game.history[0]["score"], 100)
        self.assertEqual(len(game.quizzes), 4)

    def test_corrupt_files_recover(self):
        bad_inputs = ["broken", "[]", '{"quizzes":123,"best_score":null}', '{"quizzes":[],"best_score":null,"history":{}}']
        for bad in bad_inputs:
            with self.subTest(bad=bad):
                self.state.write_text(bad, encoding="utf-8")
                output = self.run_session(["5"])
                self.assertIn("손상되었거나 형식", output)
                self.assertEqual(len(self.saved()["quizzes"]), 5)

    def test_invalid_quiz_fields_rejected(self):
        for key, value in (("question", " "), ("choices", ["a"]), ("choices", ["a", "b", "c", " "]), ("answer", True), ("answer", 5), ("hint", None)):
            with self.subTest(key=key, value=value):
                data = copy.deepcopy(self.defaults)
                data["quizzes"][0][key] = value
                with self.assertRaises((ValueError, TypeError, KeyError)):
                    self.game().parse_state(data)

    def test_invalid_record_fields_rejected(self):
        valid = dict(score=100, correct_count=1, total=1, hints_used=0)
        for key, value in (("score", float("nan")), ("score", True), ("score", 99), ("total", 0), ("total", True), ("correct_count", 2), ("hints_used", -1), ("hints_used", 2), ("hints_used", True)):
            with self.subTest(key=key, value=value):
                record = {**valid, key: value}
                with self.assertRaises(ValueError):
                    self.game().parse_record(record)

    def test_history_dates_rejected_when_missing_or_naive(self):
        valid = dict(score=100, correct_count=1, total=1, hints_used=0)
        for date in (None, "bad", "2026-11-08T12:00:00"):
            with self.subTest(date=date):
                with self.assertRaises((ValueError, KeyError)):
                    self.game().parse_record({**valid, "played_at": date}, require_date=True)

    def test_write_failure_does_not_destroy_saved_file(self):
        self.reset()
        original = self.state.read_bytes()
        (self.directory / "state.tmp").mkdir()
        game = self.game()
        saved, output = self.call(game.save_state)
        self.assertFalse(saved)
        self.assertEqual(self.state.read_bytes(), original)
        self.assertIn("저장하지 못했습니다", output)
        (self.directory / "state.tmp").rmdir()
        self.assertTrue(self.call(game.save_state)[0])

    def test_read_error_uses_defaults(self):
        self.state.mkdir()
        game, output = self.call(self.mod.QuizGame)
        self.assertEqual(len(game.quizzes), 5)
        self.assertIn("읽을 수 없습니다", output)

    def test_non_utf8_file_recovers(self):
        self.state.write_bytes(b"\xff\xfe\x80")
        game = self.game()
        self.assertEqual(len(game.quizzes), 5)

    def test_save_path_is_script_relative(self):
        self.assertEqual(self.game().state_path, self.state)

    def test_real_process_bonus_game_and_restart(self):
        self.reset()
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", str(self.program)],
            input="1\n1\nh\n1\n7\n5\n", text=True, encoding="utf-8",
            capture_output=True, cwd=self.directory.parent, timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        record = self.saved()["history"][0]
        self.assertEqual(record["total"], 1)
        self.assertEqual(record["hints_used"], 1)
        self.assertLessEqual(record["score"], 95)
        again = subprocess.run(
            [sys.executable, "-X", "utf8", str(self.program)],
            input="7\n5\n", text=True, encoding="utf-8",
            capture_output=True, cwd=self.directory.parent, timeout=10,
        )
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertIn("점수 히스토리 (총 1회", again.stdout)

    def test_real_process_eof_saves(self):
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", str(self.program)],
            input="", text=True, encoding="utf-8", capture_output=True, timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("입력이 종료되어", completed.stdout)
        self.assertEqual(len(self.saved()["quizzes"]), 5)

    def test_old_ten_point_records_and_new_five_point_records_coexist(self):
        old = dict(score=90, correct_count=1, total=1, hints_used=1)
        data = copy.deepcopy(self.defaults)
        data["best_score"] = old.copy()
        data["history"] = [{**old, "played_at": "2026-11-08T20:00:00+09:00"}]
        self.reset(data)
        self.run_session(["1", "1", "h", "2", "5"])
        game = self.game()
        self.assertEqual(game.best_score["score"], 95)
        self.assertEqual(game.best_score["hint_penalty"], 5)
        self.assertEqual([r["score"] for r in game.history], [90, 95])
        self.assertEqual([r["hint_penalty"] for r in game.history], [10, 5])


if __name__ == "__main__":
    unittest.main(verbosity=2)
