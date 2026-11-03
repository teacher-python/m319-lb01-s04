"""Shared helper functions for the servants.py test suite."""
import random

import pytest

import servants


def run_main(monkeypatch, capsys, servant_count, week_count):
    """Runs servants.main() with the given inputs and returns
    (return value, full console output)."""
    inputs = iter([str(servant_count), str(week_count)])
    monkeypatch.setattr("builtins.input", lambda *_args: next(inputs))
    result = servants.main()
    output = capsys.readouterr().out
    return result, output


def expected_numbers(servant_count, week_count):
    """Reference sequence of all "Nummer:" values printed by a correct solution."""
    numbers = []
    for week in range(1, week_count + 1):
        number = week
        while number < servant_count:
            numbers.append(number)
            number += week
    return numbers


def expected_servants(servant_count, week_count):
    """Reference list of coins per servant.

    servants[index] receives one coin for every divisor of `index` that is
    not larger than week_count. Whenever a servant would have more than
    3 coins, the king takes all of them away, so the coins cycle
    1, 2, 3, 0, 1, ... and end up as (number of such divisors) % 4.
    Index 0 is never reached by the loops (week and number start at 1).
    """
    coin_list = []
    for index in range(servant_count):
        if index == 0:
            coin_list.append(0)
            continue
        divisors = sum(1 for week in range(1, week_count + 1) if index % week == 0)
        coin_list.append(divisors % 4)
    return coin_list


def expected_count(servant_count, week_count):
    """Number of servants having 1 or 2 coins at the end."""
    return sum(1 for coins in expected_servants(servant_count, week_count) if coins in (1, 2))


def random_inputs():
    """Random (servant_count, week_count) within a range where every check is meaningful."""
    return random.randint(5, 30), random.randint(3, 15)


def inputs_text(servant_count, week_count):
    """Describes the simulated inputs for failure messages."""
    return f'Eingaben: {servant_count} Diener, {week_count} Wochen'


def fail(servant_count, week_count, expected, actual, label='Output'):
    """Fails the test with a short message containing the inputs."""
    pytest.fail(
        f"{inputs_text(servant_count, week_count)} / "
        f"Expected {label}: '{expected}' / Actual {label}: '{actual}'",
        pytrace=False
    )


def check_list(result, servant_count, week_count):
    """Checks that the result is a list with one entry (0..3 coins) per servant."""
    if not isinstance(result, list):
        fail(servant_count, week_count, 'list', type(result).__name__, 'type')
    if len(result) != servant_count:
        fail(servant_count, week_count, servant_count, len(result), 'list length')
    if not all(isinstance(coins, int) and 0 <= coins <= 3 for coins in result):
        fail(servant_count, week_count, 'nur int-Werte von 0 bis 3', result, 'list')


def check_weeks(output, servant_count, week_count):
    """Checks that every week is printed as 'Woche:n'."""
    expected = [f'Woche:{week}' for week in range(1, week_count + 1)]
    found = [line for line in output.splitlines() if line.startswith('Woche:')]
    if found != expected:
        fail(servant_count, week_count, ', '.join(expected), ', '.join(found))


def check_numbers(output, servant_count, week_count):
    """Checks that all numbers are printed as 'Nummer:n' in the correct order."""
    expected = expected_numbers(servant_count, week_count)
    found = [int(line.split(':')[1]) for line in output.splitlines() if line.startswith('Nummer:')]
    if found != expected:
        fail(servant_count, week_count, expected, found, 'numbers')


def check_coins(result, servant_count, week_count):
    """Checks the coins of every servant."""
    expected = expected_servants(servant_count, week_count)
    if result != expected:
        fail(servant_count, week_count, expected, result, 'list')


def check_count(output, servant_count, week_count):
    """Checks the line with the number of servants having 1 or 2 coins."""
    expected = f'{expected_count(servant_count, week_count)} Diener'
    if expected not in output:
        actual = next(line for line in output.splitlines() if 'Diener' in line)
        fail(servant_count, week_count, expected, actual)
