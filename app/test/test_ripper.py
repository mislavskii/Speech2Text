import os
import pytest
from app.src.ripper import *
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_yt_dlp():
    """Fixture to mock yt_dlp.YoutubeDL"""
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        yield mock_ydl


def test_extract_subtitles_success(mock_yt_dlp):
    """Test when subtitles exist."""
    mock_instance = mock_yt_dlp.return_value
    mock_instance.__enter__.return_value.extract_info.return_value = {
        'requested_subtitles': {
            'th': {'filepath': 'files/sample_video_th.vtt'}
        }
    }
    
    result = extract_subtitles("https://www.youtube.com/watch?v=example", lang='th')
    assert result == "files/sample_video_th.vtt"


def test_extract_subtitles_no_subs(mock_yt_dlp, capsys):
    """Test when subtitles are not available."""
    mock_instance = mock_yt_dlp.return_value
    mock_instance.__enter__.return_value.extract_info.return_value = {}

    result = extract_subtitles("https://www.youtube.com/watch?v=example", lang='th')
    assert result is None

    captured = capsys.readouterr()
    assert "No subtitles found for th language" in captured.out


def test_extract_subtitles_all_the_way_through():
    # Call the function
    video_url = 'https://www.youtube.com/watch?v=3QzvFvRsCMg'
    lang = 'th'
    output_path = 'app/test/files'
    result = extract_subtitles(video_url, lang=lang, output_path=output_path)

    # Assertions
    assert result == "app\\test\\files\\ครั้งแรกของ 'สุจิตต์' บรรยายพิเศษที่สภาฯ ＂จากสยามถึงไทย ： เปลี่ยนชื่อ เปลี่ยนประเทศ？＂ ： Matichon TV_3QzvFvRsCMg.th.vtt"
    assert os.path.exists(result)
    