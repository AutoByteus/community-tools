import pytest
import platform

from autobyteus_community_tools.social_media_poster.weibo.window_utils import find_window_by_name

pytestmark = pytest.mark.skipif(platform.system() != "Darwin", reason="macOS-specific tests")

def test_find_existing_window():
    # Test finding a window that should always exist on macOS
    result = find_window_by_name("Finder")
    assert result is not None

def test_find_non_existing_window():
    # Test finding a window that should not exist
    result = find_window_by_name("NonExistentWindowName12345")
    assert result is None