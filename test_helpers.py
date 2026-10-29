"""Shared helper functions for the servants.py test suite."""
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
