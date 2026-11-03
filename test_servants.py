"""
Tests for servants.py.

Each step is only checked once the program shows at least some trace of
its implementation (e.g. the output 'Woche:' for step 2). Until then, the
corresponding test is skipped (SKIPPED) instead of being marked as
failed. This way, only the tests matching the step currently being
worked on actually run.

Every step has tests with fixed inputs and one test with random inputs
(test_*_random). The inputs used are shown in the failure message.
"""
import pytest

from test_helpers import (check_coins, check_count, check_list, check_numbers, check_weeks,
                          random_inputs, run_main)


# Step 0: Check the setup of this project
def test_setup(monkeypatch, capsys):
    assert True


# Step 1: Create list

def run_list(monkeypatch, capsys, servant_count, week_count):
    result, _ = run_main(monkeypatch, capsys, servant_count, week_count)
    if not result:
        pytest.skip('Step 1 (Liste erstellen) noch nicht umgesetzt: Es wurde keine Liste (oder eine leere Liste) zurückgegeben')
    check_list(result, servant_count, week_count)


def test_list_1(monkeypatch, capsys):
    run_list(monkeypatch, capsys, 5, 3)


def test_list_2(monkeypatch, capsys):
    run_list(monkeypatch, capsys, 8, 2)


def test_list_random(monkeypatch, capsys):
    run_list(monkeypatch, capsys, *random_inputs())


# Step 2: Output all weeks

def run_weeks(monkeypatch, capsys, servant_count, week_count):
    _, output = run_main(monkeypatch, capsys, servant_count, week_count)
    if 'Woche' not in output:
        pytest.skip("Step 2 (Ausgabe aller Wochen) noch nicht umgesetzt: Im Output wurde 'Woche' nicht gefunden")
    check_weeks(output, servant_count, week_count)


def test_weeks_1(monkeypatch, capsys):
    run_weeks(monkeypatch, capsys, 10, 5)


def test_weeks_2(monkeypatch, capsys):
    run_weeks(monkeypatch, capsys, 4, 7)


def test_weeks_random(monkeypatch, capsys):
    run_weeks(monkeypatch, capsys, *random_inputs())


def test_weeks_3(monkeypatch, capsys):
    week_count = 11
    _, output = run_main(monkeypatch, capsys, 9, 4)
    if 'Tag' not in output:
        pytest.skip("SKIPPED wird aktuell erwartet: Im Output wurde 'Tag' nicht gefunden")
    expected = [f'Tage={int(week_count * 7)}']
    found = [line for line in output.splitlines() if line.startswith('Tag')]
    assert found == expected


# Step 3: Process numbers

def run_numbers(monkeypatch, capsys, servant_count, week_count):
    _, output = run_main(monkeypatch, capsys, servant_count, week_count)
    if 'Nummer' not in output:
        pytest.skip("Step 3 (Nummer verarbeiten) noch nicht umgesetzt: Im Output wurde 'Nummer' nicht gefunden")
    check_numbers(output, servant_count, week_count)


def test_number_1(monkeypatch, capsys):
    run_numbers(monkeypatch, capsys, 6, 6)


def test_number_2(monkeypatch, capsys):
    run_numbers(monkeypatch, capsys, 12, 4)


def test_number_random(monkeypatch, capsys):
    run_numbers(monkeypatch, capsys, *random_inputs())


# Step 4: Distribute coins

def run_coins(monkeypatch, capsys, servant_count, week_count):
    result, _ = run_main(monkeypatch, capsys, servant_count, week_count)
    if not result or not any(isinstance(coins, int) and coins > 0 for coins in result):
        pytest.skip('Step 4 (Münzen verteilen) noch nicht umgesetzt: In der Liste wurde keine Münzanzahl grösser als 0 gefunden')
    check_coins(result, servant_count, week_count)


def test_coins_1(monkeypatch, capsys):
    run_coins(monkeypatch, capsys, 13, 13)


def test_coins_2(monkeypatch, capsys):
    run_coins(monkeypatch, capsys, 30, 8)


def test_coins_random(monkeypatch, capsys):
    run_coins(monkeypatch, capsys, *random_inputs())


def test_coins_3(monkeypatch, capsys):
    result, _ = run_main(monkeypatch, capsys, 17, 5)
    if not result or not any(isinstance(coins, str) for coins in result):
        pytest.skip('SKIPPED wird aktuell erwartet: In der Liste wurde kein String gefunden')
    assert all(isinstance(coins, int) for coins in result)


# Step 5: Count servants

def run_count(monkeypatch, capsys, servant_count, week_count):
    _, output = run_main(monkeypatch, capsys, servant_count, week_count)
    if 'Diener' not in output:
        pytest.skip("Step 5 (Diener zählen) noch nicht umgesetzt: Im Output wurde 'Diener' nicht gefunden")
    check_count(output, servant_count, week_count)


def test_count_1(monkeypatch, capsys):
    run_count(monkeypatch, capsys, 20, 20)


def test_count_2(monkeypatch, capsys):
    run_count(monkeypatch, capsys, 30, 6)


def test_count_random(monkeypatch, capsys):
    run_count(monkeypatch, capsys, *random_inputs())
