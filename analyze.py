# -*- coding: cp936
from sys import argv
from sqlite3 import connect
from snownlp import SnowNLP

uid_i = int(argv[1])
uid_j = int(argv[2])

db = connect('hupu-gear.db')
cs = db.cursor()

sql = 'select mid, uid, content, sentiment from message where uid in ({uid_i}, {uid_j})'.format(uid_i=uid_i, uid_j=uid_j)
cs.execute(sql)
messages = cs.fetchall()
uid_contents = {}
mid_uid_contents = {}
mid_uid_sentiments = {}
mids = set()

for message in messages:
    mid, uid, content, sentiment = message
    mids.add(mid)
    uid_contents[uid] = uid_contents.get(uid, []) + [content]
    mid_uid_contents[(mid, uid)] = mid_uid_contents.get((mid, uid), []) + [content]
    mid_uid_sentiments[(mid, uid)] = mid_uid_sentiments.get((mid, uid), []) + [sentiment]

f = open('result.txt', 'w')
for word in SnowNLP(u'。'.join(uid_contents[uid_i])).keywords(5):
    f.write('{word}\t'.format(word=word.encode('cp936')))
f.write('\n')
for word in SnowNLP(u'。'.join(uid_contents[uid_j])).keywords(5):
    f.write('{word}\t'.format(word=word.encode('cp936')))
f.write('\n')

for mid in mids:
    keywords_i = []
    sentiment_i = 0.5
    if (mid, uid_i) in mid_uid_contents:
        keywords_i = SnowNLP(u'。'.join(mid_uid_contents[(mid, uid_i)])).keywords(5)
        sentiment_i = sum(mid_uid_sentiments[(mid, uid_i)]) * 1.0 / len(mid_uid_sentiments[(mid, uid_i)])
        
    keywords_j = []
    sentiment_j = 0.5
    if (mid, uid_j) in mid_uid_contents:
        keywords_j = SnowNLP(u'。'.join(mid_uid_contents[(mid, uid_j)])).keywords(5)
        sentiment_j = sum(mid_uid_sentiments[(mid, uid_j)]) * 1.0 / len(mid_uid_sentiments[(mid, uid_j)])

    for word in keywords_i:
        f.write('{word}|'.format(word=word.encode('cp936')))
    f.write('\t{sentiment}\t'.format(sentiment=sentiment_i))
    f.write('{mid}\t'.format(mid=mid))
    for word in keywords_j:
        f.write('{word}|'.format(word=word.encode('cp936')))
    f.write('\t{sentiment}\t'.format(sentiment=sentiment_j))
    f.write('\n')
f.close()
