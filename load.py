import json
from sqlite3 import connect

with open('message.json') as f:
    messages = json.load(f)['data']

db = connect('hupu-gear.db')
cs = db.cursor()

cs.execute('delete from message')

for message in messages:
#    print message
    sql = u'insert into message values(?, ?, ?, ?, ?)'
    cs.execute(sql, (message['mid'], message['fid'], message['uid'], message['stime'], message['content']))

db.commit()
db.close()
