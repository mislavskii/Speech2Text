from app.src.processor import *
import unittest
import os
# from src.processor import match_timestamps_wth_texts

class TestProcessor(unittest.TestCase):

    def setUp(self):
        self.vtt_file = 'app/test/files/test.vtt'
        if os.path.exists(self.vtt_file.replace('.vtt', '.tsv')):
            os.remove(self.vtt_file.replace('.vtt', '.tsv'))
        if os.path.exists(self.vtt_file.replace('.vtt', '.txt')):
            os.remove(self.vtt_file.replace('.vtt', '.txt'))

    def test_match_timestamps_wth_auto_subs(self):
        result = match_timestamps_wth_auto_subs(self.vtt_file)
        expected = [
            (('00:00:00.160', '00:00:04.510'), 'ถามว่ามันเกิดอะไรขึ้นประเทศสยามถึงถูก'),
            (('00:00:04.520', '00:00:08.150'), 'เปลี่ยนเป็นประเทศไทยตอบว่าการเมืองชาติ'),
            (('00:00:08.160', '00:00:11.749'), 'นิยมช่วงเวลาตึงเครียดก่อนประกาศสงคราม')
        ]
        self.assertEqual(result, expected)

    def test_tsv_file_creation(self):
        match_timestamps_wth_auto_subs(self.vtt_file)
        self.assertTrue(os.path.exists('app/test/files/test.tsv'))
        with open('app/test/files/test.tsv', 'r', encoding='utf-8') as f:
            content = f.read()
        expected_content = "start_time\tend_time\ttext\n" \
            "00:00:00.160\t00:00:04.510\tถามว่ามันเกิดอะไรขึ้นประเทศสยามถึงถูก\n" \
            "00:00:04.520\t00:00:08.150\tเปลี่ยนเป็นประเทศไทยตอบว่าการเมืองชาติ\n" \
            "00:00:08.160\t00:00:11.749\tนิยมช่วงเวลาตึงเครียดก่อนประกาศสงคราม\n"
        self.assertEqual(content, expected_content)

    def test_txt_file_creation(self):
        match_timestamps_wth_auto_subs(self.vtt_file)
        self.assertTrue(os.path.exists('app/test/files/test.txt'))
        with open('app/test/files/test.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        expected_content = "ถามว่ามันเกิดอะไรขึ้นประเทศสยามถึงถูก\nเปลี่ยนเป็นประเทศไทยตอบว่าการเมืองชาติ\nนิยมช่วงเวลาตึงเครียดก่อนประกาศสงคราม\n"
        self.assertEqual(content, expected_content)

if __name__ == '__main__':
    unittest.main()
