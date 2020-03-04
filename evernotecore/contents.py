from string import Template


class Content:
    def __init__(self, title, body):
        self.title = title
        self.body = ContentBody().make(body)


class ContentBody:
    def __init__(self):
        self.__header = '<?xml version="1.0" encoding="UTF-8"?>' \
                        '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        self.__body_template = Template('<en-note>$body</en-note>')

    def make(self, body):
        return self.__header + self.__body_template.substitute(body=body)


def make_contents_from_message(messages, title_prefix=''):
    result = []
    for key in messages.keys():
        body = ''
        for value in messages[key]:
            body += f'{value}<br/>'
        content = Content(f'{title_prefix}_{key}', body)
        result.append(content)

    return result
