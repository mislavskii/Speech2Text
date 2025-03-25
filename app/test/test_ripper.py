import os
import pytest
from app.src.ripper import *

def test_extract_subtitles_success():
    # Call the function
    video_url = 'https://www.youtube.com/watch?v=3QzvFvRsCMg'
    lang = 'th'
    output_path = 'app/test/files'
    result = extract_subtitles(video_url, lang, output_path)

    # Assertions
    assert result == "app\\test\\files\\ครั้งแรกของ 'สุจิตต์' บรรยายพิเศษที่สภาฯ ＂จากสยามถึงไทย ： เปลี่ยนชื่อ เปลี่ยนประเทศ？＂ ： Matichon TV_3QzvFvRsCMg.th.vtt"
    assert os.path.exists(result)
    