"""
Tests for servants.py.

Each step is only checked once the program shows at least some trace of
its implementation (e.g. the output 'Woche:' for step 2). Until then, the
corresponding test is skipped (SKIPPED) instead of being marked as
failed. This way, only the tests matching the step currently being
worked on actually run.
"""
import pytest

from test_helpers import expected_count, expected_numbers, expected_servants, run_main


# Step 0: Check the setup of this project
def test_setup(monkeypatch, capsys):
    assert True


# Step 1: Create list

def test_list_1(monkeypatch, capsys):
    result, _ = run_main(monkeypatch, capsys, 5, 3)
    if not result:
        pytest.skip('Step 1 (Liste erstellen) noch nicht umgesetzt')
    assert isinstance(result, list)
    assert len(result) == 5


def test_list_2(monkeypatch, capsys):
    result, _ = run_main(monkeypatch, capsys, 8, 2)
    if not result:
        pytest.skip('Step 1 (Liste erstellen) noch nicht umgesetzt')
    assert len(result) == 8
    assert all(isinstance(coins, int) and 0 <= coins <= 3 for coins in result)


# Step 2: Output all weeks

def test_weeks_1(monkeypatch, capsys):
    week_count = 5
    _, output = run_main(monkeypatch, capsys, 10, week_count)
    if 'Woche' not in output:
        pytest.skip('Step 2 (Ausgabe aller Wochen) noch nicht umgesetzt')
    expected = [f'Woche:{week}' for week in range(1, week_count + 1)]
    found = [line for line in output.splitlines() if line.startswith('Woche:')]
    assert found == expected


def test_weeks_2(monkeypatch, capsys):
    week_count = 7
    _, output = run_main(monkeypatch, capsys, 4, week_count)
    if 'Woche' not in output:
        pytest.skip('Step 2 (Ausgabe aller Wochen) noch nicht umgesetzt')
    expected = [f'Woche:{week}' for week in range(1, week_count + 1)]
    found = [line for line in output.splitlines() if line.startswith('Woche:')]
    assert found == expected


def test_weeks_3(monkeypatch, capsys):
    week_count = 11
    _, output = run_main(monkeypatch, capsys, 9, 4)
    if 'Tag' not in output:
        pytest.skip('SKIPPED wird aktuell erwartet')
    expected = [f'Tage={int(week_count * 7)}']
    found = [line for line in output.splitlines() if line.startswith('Tag')]
    assert found == expected


# Step 3: Process numbers

def test_number_1(monkeypatch, capsys):
    servant_count, week_count = 6, 6
    _, output = run_main(monkeypatch, capsys, servant_count, week_count)
    if 'Nummer' not in output:
        pytest.skip('Step 3 (Nummer verarbeiten) noch nicht umgesetzt')
    found = [int(line.split(':')[1]) for line in output.splitlines() if line.startswith('Nummer:')]
    assert found == expected_numbers(servant_count, week_count)


def test_number_2(monkeypatch, capsys):
    servant_count, week_count = 12, 4
    _, output = run_main(monkeypatch, capsys, servant_count, week_count)
    if 'Nummer' not in output:
        pytest.skip('Step 3 (Nummer verarbeiten) noch nicht umgesetzt')
    found = [int(line.split(':')[1]) for line in output.splitlines() if line.startswith('Nummer:')]
    assert found == expected_numbers(servant_count, week_count)


# Step 4: Distribute coins

def test_coins_1(monkeypatch, capsys):
    servant_count, week_count = 13, 13
    result, _ = run_main(monkeypatch, capsys, servant_count, week_count)
    if not result or not any(isinstance(coins, int) and coins > 0 for coins in result):
        pytest.skip('Step 4 (Münzen verteilen) noch nicht umgesetzt')
    assert result == expected_servants(servant_count, week_count)


def test_coins_2(monkeypatch, capsys):
    servant_count, week_count = 30, 8
    result, _ = run_main(monkeypatch, capsys, servant_count, week_count)
    if not result or not any(isinstance(coins, int) and coins > 0 for coins in result):
        pytest.skip('Step 4 (Münzen verteilen) noch nicht umgesetzt')
    assert result == expected_servants(servant_count, week_count)


def test_coins_3(monkeypatch, capsys):
    result, _ = run_main(monkeypatch, capsys, 17, 5)
    if not result or not any(isinstance(coins, str) for coins in result):
        pytest.skip('SKIPPED wird aktuell erwartet')
    assert all(isinstance(coins, int) for coins in result)


# Step 5: Count servants

def test_count_1(monkeypatch, capsys):
    servant_count, week_count = 20, 20
    _, output = run_main(monkeypatch, capsys, servant_count, week_count)
    if 'Diener' not in output:
        pytest.skip('Step 5 (Diener zählen) noch nicht umgesetzt')
    assert f'{expected_count(servant_count, week_count)} Diener' in output


def test_count_2(monkeypatch, capsys):
    servant_count, week_count = 30, 6
    _, output = run_main(monkeypatch, capsys, servant_count, week_count)
    if 'Diener' not in output:
        pytest.skip('Step 5 (Diener zählen) noch nicht umgesetzt')
    assert f'{expected_count(servant_count, week_count)} Diener' in output
