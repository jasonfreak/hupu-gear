from sqlite3 import connect

def setSpc(userPost, spc, sp_messages):
    n_messages = len(sp_messages)
    for i in range(n_messages):
        uid_i = sp_messages[i][1]
        userPost[uid_i] = userPost.get(uid_i, 0) + 1
        for j in range(i+1, n_messages):
            uid_j = sp_messages[j][1]
            spc[(uid_i, uid_j)] = spc.get((uid_i, uid_j), 0) + 1
            spc[(uid_j, uid_i)] = spc.get((uid_j, uid_i), 0) + 1

db = connect('hupu-gear.db')
cs = db.cursor()

sql = 'select uid from user'
cs.execute(sql)

users = cs.fetchall()
n_users = len(users)

userPost = {}
spc = {}

sql = 'select mid, uid from message group by mid, uid'
cs.execute(sql)
lastMid = None
while True:
    try:
        mid, uid = cs.fetchone()
    except TypeError, e:
        break
    if mid != lastMid:
        if lastMid is not None:
            setSpc(userPost, spc, sp_messages)
        sp_messages = []
        lastMid = mid
    sp_messages.append((mid, uid))
setSpc(userPost, spc, sp_messages)

f = open('graph_spr.txt', 'w')
for i in range(n_users):
    uid_i = users[i][0]
    for j in range(i+1, n_users):
        uid_j = users[j][0]
        spc_i_j = spc.get((uid_i, uid_j), 0)
        apc_i_j = userPost[uid_i] + userPost[uid_j] - spc_i_j
        if spc_i_j > 0 and apc_i_j > 6:
            spr =  spc_i_j * 1.0 / apc_i_j
            if spr > 0.3:
                f.write('{uid_i}, {uid_j}, {weight}\n'.format(uid_i=uid_i, uid_j=uid_j, weight=spr))
f.close()
