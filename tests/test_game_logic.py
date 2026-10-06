from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_too_high_hint_says_go_lower():
    # Regression: hints used to be backwards
    _, message = check_guess(60, 50)
    assert "LOWER" in message


def test_too_low_hint_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


def test_numeric_comparison_not_string():
    # Regression: str comparison made "9" > "50"; ints must compare numerically
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"


def test_parse_guess_valid_and_invalid():
    assert parse_guess("42") == (True, 42, None)
    assert parse_guess("  7 ") == (True, 7, None)
    assert parse_guess("") == (False, None, "Enter a guess.")
    assert parse_guess(None) == (False, None, "Enter a guess.")
    ok, value, err = parse_guess("abc")
    assert ok is False and value is None and err == "That is not a number."


def test_hard_range_is_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


def test_wrong_guess_never_increases_score():
    for attempt in range(1, 9):
        assert update_score(0, "Too High", attempt) == -5
        assert update_score(0, "Too Low", attempt) == -5


def test_win_score_has_floor():
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 20) == 10
