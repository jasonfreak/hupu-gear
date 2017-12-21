from datetime import datetime
from sqlite3 import connect

def setSoc(userPost, soc, co_messages):
    users = co_messages.keys()
    n_users = len(users)
    for i in range(n_users):
        uid_i = users[i]
        s_sentiment_i = sum(co_messages[uid_i]) * 1.0
        n_sentiment_i = len(co_messages[uid_i])
        avg_i =  s_sentiment_i / n_sentiment_i
        userPost[uid_i] = userPost.get(uid_i, 0) + 1
        for j in range(i+1, n_users):
            uid_j = users[j]
            s_sentiment_j = sum(co_messages[uid_j]) * 1.0
            n_sentiment_j = len(co_messages[uid_j])
            avg_j =  s_sentiment_j / n_sentiment_j
            soc[(uid_i, uid_j)] = soc.get((uid_i, uid_j), 0) + avg_i * avg_j
            soc[(uid_j, uid_i)] = soc.get((uid_j, uid_i), 0) + avg_i * avg_j

db = connect('hupu-gear.db')
cs = db.cursor()

sql = 'select uid from user'
cs.execute(sql)

users = cs.fetchall()
n_users = len(users)

userPost = {}
soc = {}

sql = 'select uid, stime, sentiment from message order by stime asc'
cs.execute(sql)

first = None
while True:
    try:
        uid, stime, sentiment = cs.fetchone()
    except TypeError, e:
        break
    t = datetime.strptime(stime, '%Y-%m-%d %H:%M')
    if first is None:
        first = t
        co_messages = {uid:[sentiment]}
        continue
    if (t-first).seconds > 3600:
        setSoc(userPost, soc, co_messages)
        first = t
        co_messages = {uid:[sentiment]}
        continue
    co_messages[uid] = co_messages.get(uid, []) + [sentiment]
setSoc(userPost, soc, co_messages)

f = open('graph_sor.txt', 'w')
for i in range(n_users):
    uid_i = users[i][0]
    for j in range(i+1, n_users):
        uid_j = users[j][0]
        soc_i_j = soc.get((uid_i, uid_j), 0)
        apc_i_j = userPost[uid_i] + userPost[uid_j] - soc_i_j
        if soc_i_j > 0 and apc_i_j > 6:
            sor = soc_i_j * 1.0 / apc_i_j
            if sor > 0.05:
                f.write('{uid_i}, {uid_j}, {weight}\n'.format(uid_i=uid_i, uid_j=uid_j, weight=sor))
#            f.write('{uid_i}, {uid_j}, {weight}\n'.format(uid_i=uid_i, uid_j=uid_j, weight=sor))
f.close()
