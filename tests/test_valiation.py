from app.validation import validate_user_input

def test_empty_input():
    ok, msg = validate_user_input("")
    assert ok is False

def test_too_short():
    ok, msg = validate_user_input("Too short")
    assert ok is False

def test_valid_text():
    ok, cleaned = validate_user_input("Please review the attached proposal and share your feedback.")
    assert ok is False
    assert isinstance(cleaned, str)