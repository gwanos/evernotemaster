import os.path
import pandas as pd
import re


def get_room_name(chat):
    verify_chat_file(chat)
    regex = re.compile(r'(?<=KakaoTalk_Chat_)(.*)(?=_\d{4})')
    return regex.findall(chat)[0]


def extract_message_from_csv(chat, users):
    verify_chat_file(chat)

    result = {}
    for user in users:
        result[user] = []

    special_chars = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        '\'': '&apos;'
    }
    data = pd.read_csv(chat)
    for user in users:
        for index, row in data.iterrows():
            if user == row['User']:
                date = row['Date']
                message = row['Message']
                if is_invalid(message):
                    continue
                result[user].append((date, replace_xml_special_chracters(message, special_chars)))

    return result


def extract_message_from_csv_group_by_date(chat, users):
    dic = extract_message_from_csv(chat, users)

    result = {}
    for lst in dic.values():
        for item in lst:
            date = item[0]
            message = item[1]
            splits = date.split(' ')
            key = splits[0]
            if key not in result:
                result[key] = []
            result[key].append(message)

    return result


def replace_xml_special_chracters(message, special_chars):
    for k, v in special_chars.items():
        message = message.replace(k, v)
    return message


def is_invalid(message):
    if message == '이모티콘' or message == '사진' or message == "동영상":
        return True
    else:
        return False


def verify_chat_file(chat=None):
    if not chat:
        raise ValueError('Please designate kakaochat.csv file.')
    if not os.path.isfile(chat):
        raise FileNotFoundError('Please check if the file exists.')
    if chat.endswith('.csv') is False:
        raise ValueError('Only .csv file is permitted.')