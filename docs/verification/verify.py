import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import runpy
import shutil
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent
results = []

def check(name, test):
    try:
        test()
        results.append({'name': name, 'result': 'PASS'})
    except Exception as exc:
        results.append({'name': name, 'result': 'FAIL', 'detail': repr(exc)})

def require(value):
    assert value

def run(path, answers):
    answers = iter(answers)
    output = io.StringIO()
    def read(prompt=''):
        print(prompt, end='')
        value = next(answers, EOFError())
        if isinstance(value, BaseException):
            raise value
        print(value)
        return value
    with contextlib.redirect_stdout(output), patch('builtins.input', read):
        runpy.run_path(str(path), run_name='__main__')
    return output.getvalue()

original_hash = hashlib.sha256((ROOT/'state.json').read_bytes()).hexdigest()
with tempfile.TemporaryDirectory(prefix='mission2_check_') as folder:
    base = Path(folder)
    program = base/'main.py'
    shutil.copy2(ROOT/'main.py', program)
    state = base/'state.json'
    spec = importlib.util.spec_from_file_location('mission2_checked', program)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    defaults = {'quizzes': [vars(q) for q in mod.create_default_quizzes()], 'best_score': None}
    def reset(data=defaults):
        state.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    def invoke(fn, answers):
        values = iter(answers)
        with contextlib.redirect_stdout(io.StringIO()), patch('builtins.input', side_effect=lambda *a: next(values)):
            return fn()
    check('Quiz display and correct/wrong answers', lambda: require(mod.Quiz('Q', ['a','b','c','d'], 2).check_answer(2) and not mod.Quiz('Q', ['a','b','c','d'], 2).check_answer(1)))
    check('Default quizzes: five, four choices, valid answer', lambda: require(len(defaults['quizzes']) >= 5 and all(len(q['choices']) == 4 and 1 <= q['answer'] <= 4 for q in defaults['quizzes'])))
    check('Menu: blank, spaces, text, out of range, trimmed valid', lambda: require(invoke(mod.read_menu_choice, ['', '  ', 'abc', '0', '9', ' 3 ']) == 3))
    check('Answer: blank, spaces, text, out of range, trimmed valid', lambda: require(invoke(mod.read_answer, ['', ' ', 'abc', '0', '5', ' 2 ']) == 2))
    check('Text: blank and spaces rejected', lambda: require(invoke(lambda: mod.read_non_empty_text('Q:'), ['', '  ', ' question ']) == 'question'))
    check('Empty play returns None', lambda: require(invoke(lambda: mod.play_quizzes([]), []) is None))
    check('Empty list is handled', lambda: require(invoke(lambda: mod.show_quiz_list([]), []) is None))
    first = run(program, ['4','5'])
    check('Missing file uses defaults and saves on exit', lambda: require('저장 파일이 없어' in first and state.exists()))
    check('No completed game message', lambda: require('아직 퀴즈를 완료한 기록' in first))
    reset()
    log = run(program, ['2', '', 'Python에서 리스트 끝에 요소를 추가하는 메서드는?', '', 'append()', 'strip()', 'upper()', 'split()', '0', 'abc', '1', '5'])
    (OUT/'add.txt').write_text(log, encoding='utf-8')
    check('Add quiz with invalid input and save', lambda: require(len(json.loads(state.read_text(encoding='utf-8'))['quizzes']) == 6 and '퀴즈가 추가되었습니다!' in log))
    listing = run(program, ['3','5'])
    check('Added quiz survives restart and appears in list', lambda: require('[6] Python에서 리스트 끝에 요소를 추가하는 메서드는?' in listing))
    log = run(program, ['1','2','3','1','4','1','1','5'])
    start = log.index('[문제 6]')
    end = log.index('데이터를 저장했습니다.', start) + len('데이터를 저장했습니다.')
    (OUT/'play.txt').write_text(log[start:end]+'\n', encoding='utf-8')
    check('Play six quizzes and calculate score', lambda: require('6문제 중 5문제 정답!' in log and '83.33점' in log))
    log = run(program, ['4','5'])
    (OUT/'score.txt').write_text(log, encoding='utf-8')
    (OUT/'reload.txt').write_text(run(program, ['3','4','5']), encoding='utf-8')
    check('Best score survives restart', lambda: require('최고 점수: 83.33점' in log and '기록: 6문제 중 5문제 정답' in log))
    reset()
    run(program, ['1','1','1','2','1','1','5'])
    check('Zero score is completed record', lambda: require(json.loads(state.read_text(encoding='utf-8'))['best_score']['score'] == 0))
    run(program, ['1','2','3','1','4','2','5'])
    check('Higher score replaces best', lambda: require(json.loads(state.read_text(encoding='utf-8'))['best_score']['score'] == 100))
    run(program, ['1','1','1','2','1','1','5'])
    check('Lower score preserves best', lambda: require(json.loads(state.read_text(encoding='utf-8'))['best_score']['score'] == 100))
    run(program, ['1','2','3','1','4','2','5'])
    check('Equal score preserves best', lambda: require(json.loads(state.read_text(encoding='utf-8'))['best_score']['score'] == 100))
    for label, inputs in [('Menu Ctrl+C', [KeyboardInterrupt()]), ('Play Ctrl+C', ['1', KeyboardInterrupt()]), ('Add Ctrl+C', ['2','unfinished',KeyboardInterrupt()]), ('Menu EOF', [EOFError()]), ('Play EOF', ['1',EOFError()]), ('Add EOF', ['2','unfinished',EOFError()])]:
        reset()
        log = run(program, inputs)
        saved = json.loads(state.read_text(encoding='utf-8'))
        check(label+' saves without incomplete data', lambda s=saved, l=log: require(len(s['quizzes'])==5 and s['best_score'] is None and '게임을 종료합니다.' in l and '데이터를 저장했습니다.' in l))
    for label, bad in [('Malformed JSON', 'broken'), ('Wrong quizzes type', '{"quizzes":123,"best_score":null}'), ('Invalid choices', json.dumps({'quizzes':[{'question':'Q','choices':['a'],'answer':1}], 'best_score':None})), ('Invalid score', json.dumps({'quizzes':[], 'best_score':{'score':100,'correct_count':0,'total':5}}))]:
        state.write_text(bad, encoding='utf-8')
        log = run(program, ['5'])
        check(label+' resets safely', lambda l=log: require('손상되었거나 형식이 올바르지' in l and len(json.loads(state.read_text(encoding='utf-8'))['quizzes'])==5))
    reset()
    tmp = base/'state.tmp'
    tmp.mkdir()
    log = run(program, ['5'])
    check('Write error is reported without crash', lambda: require('데이터를 저장하지 못했습니다' in log))
    tmp.rmdir()
    log = run(program, ['5'])
    check('Saving recovers after write error removed', lambda: require('데이터를 저장했습니다.' in log))
    reset()
    with contextlib.redirect_stdout(io.StringIO()):
        game = mod.QuizGame()
    check('Path is based on script directory', lambda: require(game.state_path == state))
check('Original project state unchanged', lambda: require(hashlib.sha256((ROOT/'state.json').read_bytes()).hexdigest() == original_hash))
(OUT/'verification.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(results, ensure_ascii=False, indent=2))
if any(r['result'] != 'PASS' for r in results):
    raise SystemExit(1)

