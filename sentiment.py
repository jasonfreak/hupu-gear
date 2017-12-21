# -*- coding: cp936
from sqlite3 import connect
from snownlp import SnowNLP

db = connect('hupu-gear.db')
cs1 = db.cursor()
cs2 = db.cursor()

lining = (u'李宁', u'某宁', u'Lining', u'lining', u'LINING', u'LN', u'韦德', u'Wow', u'wow', u'WOW', u'闪击', u'空袭', u'音速', u'孙悦', u'郭艾伦')
other = (u'耐克', u'Nike', u'nike', u'NIKE', u'NK', u'Jordan', u'jordan', u'JORDAN', u'Air', u'air', u'AIR', u'科比', u'Kobe', u'kobe', u'KOBE', u'zk', u'zoom', u'勒布朗', u'老詹', u'詹皇', u'小皇帝', u'Lebron', u'lebron', u'LEBRON', u'James', u'james', u'JAMES', u'战士', u'使节', u'安东尼', u'欧文', u'喷', u'泡', u'foam', u'Foam', u'FOAM', u'Hyper', u'hyper', u'HYPER', u'Dunk', u'dunk', u'DUNK', u'阿迪', u'阿迪达斯', u'Adidas', u'adidas', u'ADIDAS', u'Boost', u'boost', u'BOOST', u'哈登', u'登哥', u'Harden', u'harden', u'HARDEN', u'林书豪', u'罗斯', u'Rose', u'rose', u'ROSE', u'维金斯', u'clb', u'CLB', u'Explosive', u'explosive', u'EXPLOSIVE', u'匡威', u'Converse', 'converse', 'CONVERSE', u'安踏', u'某踏', u'Anta', u'anta', u'ANTA', u'克莱', u'汤姆斯', u'KT', u'kt', u'隆多', u'匹克', u'Peak', u'peak', u'PEAK', u'帕克', u'Park', u'park', u'PARK', u'tp')

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
    
