import pytest
from unittest.mock import patch, MagicMock

from autobyteus_community_tools.social_media_poster.weibo.window_utils import find_window_by_name_mac

@pytest.fixture
def mock_workspace():
    with patch('autobyteus.utils.window_utils.NSWorkspace') as mock:
        yield mock

def test_find_existing_window(mock_workspace):
    # Set up mock
    mock_app = MagicMock()
    mock_app.localizedName.return_value = "TestApp"
    mock_app.activationPolicy.return_value = MagicMock()  # Assuming NSApplicationActivationPolicyRegular

    mock_workspace.sharedWorkspace.return_value.runningApplications.return_value = [mock_app]

    # Test
    result = find_window_by_name_mac("TestApp")
    assert result == mock_app

def test_find_non_existing_window(mock_workspace):
    # Set up mock
    mock_app = MagicMock()
    mock_app.localizedName.return_value = "OtherApp"
    mock_app.activationPolicy.return_value = MagicMock()  # Assuming NSApplicationActivationPolicyRegular

    mock_workspace.sharedWorkspace.return_value.runningApplications.return_value = [mock_app]

    # Test
    result = find_window_by_name_mac("TestApp")
    assert result is None

def test_empty_input(mock_workspace):
    # Set up mock
    mock_workspace.sharedWorkspace.return_value.runningApplications.return_value = []

    # Test
    result = find_window_by_name_mac("")
    assert result is None