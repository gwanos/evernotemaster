# evernotemaster
카카오톡 채팅 중 원하는 사람의 메세지만 선별하여 에버노트에 기록.

## Prerequisites
* 카카오톡 채팅 파일(.csv)
  + '채팅방 - 대화 내용 저장'으로 생성된 파일
* 에버노트 노트북
  + 노트가 생성될 위치

## Usage
```
python create.py --file={채팅 파일 경로} --user={선별 대상} --notebook={에버노트 노트북 이름}
```
사용예
```
python create.py --file=./Document/KakaoChat_채팅방_2020-03-04.csv --user=이관호 --notebook=Inbox
```

## References
* https://github.com/evernote/evernote-sdk-python3
* https://dev.evernote.com/doc
