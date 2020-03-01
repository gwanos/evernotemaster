from kakaochat import extractor
import unittest


class TestExtract(unittest.TestCase):

    def setUp(self) -> None:
        self.chat = './sample_chat/KakaoTalk_Chat_09 소그룹_2020-03-01-10-16-45.csv'
        self.users = ['이관호']

    def tearDown(self) -> None:
        pass

    @unittest.skip
    def test_extract_message_from_csv(self):
        try:
            result = extractor.extract_message_from_csv(self.chat, self.users)
            pass
        except Exception as ex:
            print(ex)

    #@unittest.skip
    def test_extract_message_from_csv_group_by_date(self):
        try:
            result = extractor.extract_message_from_csv_group_by_date(self.chat, self.users)
            pass
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    unittest.main()
