from evernote.api.client import EvernoteClient
from evernotecore.error.errors import *
import evernote.edam.type.ttypes as CommonTypes
import evernote.edam.notestore.ttypes as NoteStoreTypes
import evernote.edam.limits.constants as LimitConstants


class UserCoordinator:
    def __init__(self, auth_token, is_sandbox):
        self.client = EvernoteClient(token=auth_token, sandbox=is_sandbox)

    def get_user(self):
        user_store = self.client.get_user_store()
        return user_store.getUser()


class NoteCoordinator:
    def __init__(self, auth_token, is_sandbox):
        self.token = auth_token
        self.client = EvernoteClient(token=auth_token, sandbox=is_sandbox)
        self.note_store = self.client.get_note_store()

    def create_note(self, content, parent_notebook=None):
        note = CommonTypes.Note(title=content.title, content=content.body)
        if parent_notebook and hasattr(parent_notebook, 'guid'):
            note.notebookGuid = parent_notebook.guid
        return self.note_store.createNote(self.token, note)

    def get_notebook(self, name):
        notebooks = self.get_notebooks()
        found = list(filter(lambda x: x.name == name, notebooks))
        if not found:
            raise NotFoundNotebookError(name=name)
        else:
            return found[0]

    def get_notebooks(self):
        ret = self.note_store.listNotebooks()
        return ret

    def get_latest_note_on_notebook(self, notebook):
        note_metadata = self.find_notes_metadata(notebook)
        if not note_metadata.notes:
            return None
        return note_metadata.notes[0]

    def find_notes_metadata(self, notebook=None):
        note_filter = NoteStoreTypes.NoteFilter(order=CommonTypes.NoteSortOrder.TITLE, ascending=False)
        if notebook is not None:
            note_filter.notebookGuid = notebook.guid
        spec = NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True)

        return self.note_store.findNotesMetadata(self.token, note_filter, 0, LimitConstants.EDAM_USER_NOTES_MAX, spec)

    def find_note_counts(self, word):
        note_filter = NoteStoreTypes.NoteFilter()
        note_filter.words = word
        note_filter.ascending = False

        ret = self.note_store.findNoteCounts(self.token, note_filter, False)
        return ret
