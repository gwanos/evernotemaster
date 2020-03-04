import argparse
import dateutil.parser as dparser
import evernotecore.contents
import json
import warnings
import kakaochat.extractor
from evernotecore.error.errors import *
from evernotecore.coordinator import NoteCoordinator


class Main:
    def __init__(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.file = open('./evernotecore/config.json')
        self.config = json.loads(self.file.read())
        self.note_coordinator = NoteCoordinator(self.config['Token'], False)

    def create_from_chat(self, chat, users, notebook_name):
        messages = kakaochat.extractor.extract_message_from_csv_group_by_date(chat, users)
        chatroom_name = kakaochat.extractor.get_room_name(chat)
        print(f'There are messages over {len(messages)} days.')

        contents = evernotecore.contents.make_contents_from_message(messages, chatroom_name)

        notebook = self.note_coordinator.get_notebook(notebook_name)
        latest = self.note_coordinator.get_latest_note_on_notebook(notebook)
        last_update = None if latest is None else dparser.parse(latest.title, fuzzy=True)

        results = []
        for content in contents:
            if self.note_exists(last_update, content.title):
                continue
            ret = self.note_coordinator.create_note(content, notebook)
            results.append(ret)

        print(f'Done. Total {len(results)} notes created.')
        for ret in results:
            print(f'Title: {ret.title}. Active: {ret.active}')

    def note_exists(self, last_update, current):
        if not last_update:
            return False

        current_date = dparser.parse(current, fuzzy=True)
        if current_date <= last_update:
            return True
        else:
            return False


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='카카오 채팅 중 원하는 상대의 메세지만 선택해 에버노트에 저장합니다.')
        parser.add_argument('--file', required=True, help='카카오 채팅 csv 파일')
        parser.add_argument('--user', required=True, action='append', help='유저')
        parser.add_argument('--notebook', required=True, help='에버노트 노트북 이름')

        args = parser.parse_args()
        main = Main()
        main.create_from_chat(args.file, args.user, args.notebook)
    except EvernoteMasterError as ex:
        print('Error.')
        print(ex.message)
    except Exception as ex:
        print('Error.')
        print(ex)
