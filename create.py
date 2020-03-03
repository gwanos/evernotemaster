import argparse
import json
import warnings
import kakaochat.extractor
from evernotecore.coordinator import NoteCoordinator
import evernotecore.contents


class Main:
    def __init__(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.file = open('./evernotecore/config.json')
        self.config = json.loads(self.file.read())
        self.note_coordinator = NoteCoordinator(self.config['Token'])

    def create_from_chat(self, chat, users, notebook_name):
        messages = kakaochat.extractor.extract_message_from_csv_group_by_date(chat, users)

        notebooks = self.note_coordinator.get_notebooks()
        notebook = list(filter(lambda x: x.name == notebook_name, notebooks))

        contents = evernotecore.contents.make_contents_from_message(messages)
        for content in contents:
            self.note_coordinator.create_note(content, notebook[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='카카오 채팅 중 원하는 상대의 메세지만 선택해 에버노트에 저장합니다.')
    parser.add_argument('--chat', required=True, help='카카오 채팅 csv 파일')
    parser.add_argument('--user', required=True, help='유저')
    parser.add_argument('--notebook', required=True, help='에버노트 노트북 이름')

    args = parser.parse_args()
    main = Main()
    main.create_from_chat(args.chat, args.user, args.notebook)