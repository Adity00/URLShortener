from services.auth_service import login_user

def test_login_correct_password():
    result = login_user("adi@gamil.com", "12345678")
    assert result is not None

def test_login_incorrect_password():
    result = login_user("adi@gamil.com", "not")
    assert result is None

def test_login_nonexistent_user():
    result = login_user("false_user.com", "12345678")
    assert result is None
