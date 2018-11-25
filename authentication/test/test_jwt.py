"""Authentication Integration tests."""

from faker import Faker

fake = Faker()


def test_login():
    """Login successfully with a username and password."""
    pass


def test_login_bad_password():
    """Fail login by supplying a wrong password."""
    pass


def test_login_bad_username():
    """Fail login by supplying a username not registered."""
    pass


def test_logout():
    """Logout from an authenticated state."""
    pass


def test_renew_token():
    """Renew JWT authentication token."""
    pass


def test_renew_token_expired():
    """Fail renewal of JWT token from an expired session."""
    pass


def test_renew_token_unknown():
    """Fail renewal of JWT token from an unknown token."""
    pass
