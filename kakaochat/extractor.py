import pandas as pd


def extract_message_from_csv(chat, users):
    if chat.endswith('.csv') is False:
        raise ValueError('Only .csv kakaochat is permitted.')

    result = {}
    for user in users:
        result[user] = []

    data = pd.read_csv(chat)
    print(data.columns.values)
    for user in users:
        for index, row in data.iterrows():
            if user == row['User']:
                date = row['Date']
                message = row['Message']
                if message == '이모티콘' or message == '사진':
                    continue
                result[user].append((date, replace_ampersand(message)))

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


def replace_ampersand(message):
    return message.replace('&', '&amp;')
