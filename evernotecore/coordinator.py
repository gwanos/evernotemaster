from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as CommonTypes
import evernote.edam.notestore.ttypes as NoteStoreTypes
import evernote.edam.limits.constants as LimitConstants


class UserCoordinator:
    def __init__(self, auth_token):
        self.client = EvernoteClient(token=auth_token)

    def get_user(self):
        user_store = self.client.get_user_store()
        return user_store.getUser()


class NoteCoordinator:
    def __init__(self, auth_token):
        self.token = auth_token
        self.client = EvernoteClient(token=auth_token)
        self.note_store = self.client.get_note_store()

    def create_note(self, content, parent_notebook=None):
        note = CommonTypes.Note(title=content.title, content=content.body)
        if parent_notebook and hasattr(parent_notebook, 'guid'):
            note.notebookGuid = parent_notebook.guid
        return self.note_store.createNote(self.token, note)

    def get_notebooks(self):
        ret = self.note_store.listNotebooks()
        return ret

    def find_notes(self, word):
        note_filter = NoteStoreTypes.NoteFilter(ascending=True)
        notes = self.note_store.findNotes(self.token, note_filter, 0, 100)
        return notes
        #query = NoteStoreTypes.RelatedQuery(plainText=word)
        result_spec = NoteStoreTypes.RelatedResultSpec(maxNotes=LimitConstants.EDAM_RELATED_MAX_NOTES)
        #ret = self.note_store.findRelated(self.token, query, result_spec)

    def find_notes_metadata(self):
        note_filter = NoteStoreTypes.NoteFilter(ascending=False)
        spec = NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True)

        return self.note_store.findNotesMetadata(self.token, note_filter, 0, LimitConstants.EDAM_USER_NOTES_MAX, spec)

    def find_note_counts(self, word):
        note_filter = NoteStoreTypes.NoteFilter()
        note_filter.words = word
        note_filter.ascending = False

        ret = self.note_store.findNoteCounts(self.token, note_filter, False)
        return ret
