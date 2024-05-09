from unittest.mock import patch

from authx import AuthX
from core.auth_config import get_authx_security


@patch('core.auth_config.settings')
def test_get_authx_security(mock_settings):
    mock_settings.SECRET_KEY = 'test_secret'

    security = get_authx_security()

    assert isinstance(security, AuthX)
    assert security.config.JWT_SECRET_KEY == 'test_secret'
