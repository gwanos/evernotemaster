import unittest
import json
import warnings
import dateutil.parser as dparser
from kakaochat import extractor
from evernotecore.coordinator import NoteCoordinator
from evernotecore.coordinator import UserCoordinator
from evernotecore.contents import Content
from evernotecore.error.errors import *
from datetime import datetime
import evernotecore.contents


class TestEvernote(unittest.TestCase):
    def setUp(self) -> None:
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.file = open('../evernotecore/config.json')
        self.config = json.loads(self.file.read())
        self.user_coordinator = UserCoordinator(self.config['Token'], False)
        self.note_coordinator = NoteCoordinator(self.config['Token'], False)

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

    #@unittest.skip
    def test_create_note_with_file_on_notebook(self):
        # 파일
        chat = './sample_chat/KakaoTalk_Chat_09 소그룹_2020-03-01-10-16-45.csv'
        users = ['이관호']
        messages = extractor.extract_message_from_csv_group_by_date(chat, users)
        chatroom_name = extractor.get_room_name(chat)

        # 에버노트 컨텐츠
        contents = evernotecore.contents.make_contents_from_message(messages, chatroom_name)

        try:
            # 노트북
            notebook_name = '[Default] InBox'
            notebook = self.note_coordinator.get_notebook(notebook_name)
            latest = self.note_coordinator.get_latest_note_on_notebook(notebook)
            last_update = None if latest is None else dparser.parse(latest.title, fuzzy=True)

            # 노트 생성
            results = []
            for content in contents:
                current_date = dparser.parse(content.title, fuzzy=True)
                if current_date <= last_update:
                    continue
                ret = self.note_coordinator.create_note(content, notebook)
                results.append(ret)

            print(f'Done. Total {len(results)} notes created.')
            for ret in results:
                print(f'Title: {ret.title}. Active: {ret.active}')
        except EvernoteMasterError as ex:
            print(ex.message)
        except Exception as ex:
            print(ex)


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
        try:
            metadata = self.note_coordinator.find_notes_metadata()
            for note in metadata.notes:
                print(note.title)
        except Exception as ex:
            print(ex)

    @unittest.skip
    def test_find_note_counts(self):
        try:
            count = self.note_coordinator.find_note_counts('이관호')
            print(count)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    unittest.main()
