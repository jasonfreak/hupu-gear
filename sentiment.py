# -*- coding: cp936
from sqlite3 import connect
from snownlp import SnowNLP

db = connect('hupu-gear.db')
cs1 = db.cursor()
cs2 = db.cursor()

lining = (u'����', u'ĳ��', u'Lining', u'lining', u'LINING', u'LN', u'Τ��', u'Wow', u'wow', u'WOW', u'����', u'��Ϯ', u'����', u'����', u'������')
other = (u'�Ϳ�', u'Nike', u'nike', u'NIKE', u'NK', u'Jordan', u'jordan', u'JORDAN', u'Air', u'air', u'AIR', u'�Ʊ�', u'Kobe', u'kobe', u'KOBE', u'zk', u'zoom', u'�ղ���', u'��ղ', u'ղ��', u'С�ʵ�', u'Lebron', u'lebron', u'LEBRON', u'James', u'james', u'JAMES', u'սʿ', u'ʹ��', u'������', u'ŷ��', u'��', u'��', u'foam', u'Foam', u'FOAM', u'Hyper', u'hyper', u'HYPER', u'Dunk', u'dunk', u'DUNK', u'����', u'���ϴ�˹', u'Adidas', u'adidas', u'ADIDAS', u'Boost', u'boost', u'BOOST', u'����', u'�Ǹ�', u'Harden', u'harden', u'HARDEN', u'�����', u'��˹', u'Rose', u'rose', u'ROSE', u'ά��˹', u'clb', u'CLB', u'Explosive', u'explosive', u'EXPLOSIVE', u'����', u'Converse', 'converse', 'CONVERSE', u'��̤', u'ĳ̤', u'Anta', u'anta', u'ANTA', u'����', u'��ķ˹', u'KT', u'kt', u'¡��', u'ƥ��', u'Peak', u'peak', u'PEAK', u'����', u'Park', u'park', u'PARK', u'tp')

sql1 = 'select mid, fid, content from message'
cs1.execute(sql1)

def isLining(last, sentence):
    ret = None
    for word in lining:
        if word in sentence:
            ret = True
            break
    for word in other:
        if word in sentence:
            ret = False
    if ret is not None:
        return ret
    else:
        return last

def getSentiment(content):
    try:
        s = SnowNLP(content)
    except:
        return 0.5
    n_sentences = len(s.sentences)
    s_sentiments = 0.0
    last = None
    n_valids = 0
    for sentence in s.sentences:
        flag = isLining(last, sentence)
        if flag:
            s_sentiments += SnowNLP(sentence).sentiments
            n_valids += 1
        last = flag
    if n_valids == 0:
        return 0.5
    else:
        return s_sentiments / n_valids

while True:
    try:
        mid, fid, content = cs1.fetchone()
    except TypeError, e:    
        break
    sentiment = getSentiment(content)
    sql2 = 'update message set sentiment = {sentiment} where mid = {mid} and fid = {fid}'.format(sentiment=sentiment, mid=mid, fid=fid)
    cs2.execute(sql2)

db.commit()
db.close()
    
