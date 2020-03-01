import unittest
import json
import warnings
from kakaochat import extractor
from evernotecore.coordinator import NoteCoordinator
from evernotecore.coordinator import UserCoordinator
from evernotecore.contents import Content


class TestEvernote(unittest.TestCase):
    def setUp(self) -> None:
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.file = open('../evernotecore/config.json')
        self.config = json.loads(self.file.read())
        self.user_coordinator = UserCoordinator(self.config['Token'])
        self.note_coordinator = NoteCoordinator(self.config['Token'])

    def tearDown(self) -> None:
        self.file.close()

    @unittest.skip
    def test_get_user(self):
        self.user_coordinator.get_user()

    @unittest.skip
    def test_create_note(self):
        content = Content("노트 생성 테스트_2020.03.01", "얘 이건 노트 생성 테스트란다!")
        result = self.note_coordinator.create_note(content)
        print(result)

    @unittest.skip
    def test_create_note_on_notebook(self):
        notebook_name = '강의'
        notebooks = self.note_coordinator.get_notebooks()
        notebook = list(filter(lambda x: x.name == notebook_name, notebooks))

        content = Content("노트 생성 테스트_2020.03.01", "얘 이건 노트 생성 테스트란다!")
        result = self.note_coordinator.create_note(content, notebook[0])
        print(result)

    def test_create_note_with_file_on_notebook(self):
        # 노트북
        notebook_name = '투자'
        notebooks = self.note_coordinator.get_notebooks()
        notebook = list(filter(lambda x: x.name == notebook_name, notebooks))

        # 파일
        #chat = './sample_chat/KakaoTalk_Chat_09 소그룹_2020-03-01-10-16-45.csv'
        chat = './sample_chat/KakaoTalk_Chat_이현석 유료리딩방_2020-02-27-14-02-14.csv'
        #users = ['이관호']
        users = ['이현석(로투스)']
        messages = extractor.extract_message_from_csv_group_by_date(chat, users)

        # 에버노트 컨텐츠
        contents = []
        for key in messages.keys():
            body = f"{key}<br/><br/>"
            for value in messages[key]:
                body += f"{value}<br/>"
            content = Content(f"{key}", body)
            contents.append(content)

        # 노트 생성
        try:
            for content in contents:
                result = self.note_coordinator.create_note(content, notebook[0])
            pass
        except Exception as ex:
            print(ex)
        pass

    @unittest.skip
    def test_get_notebooks(self):
        notebooks = self.note_coordinator.get_notebooks()
        for notebook in notebooks:
            print(notebook.name)

    @unittest.skip
    def test_find_notes(self):
        try:
            notes = self.note_coordinator.find_notes('이관호')
            print(notes)
        except Exception as ex:
            print(ex)

    @unittest.skip
    def test_find_notes_metadata(self):
        metadata = self.note_coordinator.find_notes_metadata()
        for note in metadata.notes:
            print(note.title)

    @unittest.skip
    def test_find_note_counts(self):
        try:
            count = self.note_coordinator.find_note_counts('이관호')
            print(count)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    unittest.main()
