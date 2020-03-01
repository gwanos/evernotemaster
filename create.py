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

    def create_from_chat(self, notebook_name, chat, users):
        messages = kakaochat.extractor.extract_message_from_csv_group_by_date(chat, users)

        notebooks = self.note_coordinator.get_notebooks()
        notebook = list(filter(lambda x: x.name == notebook_name, notebooks))

        contents = evernotecore.contents.make_contents_from_message(messages)
        for content in contents:
            self.note_coordinator.create_note(content, notebook[0])


if __name__ == '__main__':
    main = Main()
    main.create_from_chat("", "", "")