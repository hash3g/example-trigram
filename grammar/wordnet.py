import MySQLdb
import re
import json


def getwords(letters):
    sql = '''
    SELECT lexname.lexname, lemma FROM word
    INNER JOIN sense ON sense.wordno=word.wordno
    INNER JOIN synset ON synset.synsetno=sense.synsetno
    INNER JOIN lexname ON lexname.lexno=synset.lexno
    WHERE lemma REGEXP "^[adhes]{4,}$"
    GROUP BY lemma
    '''
    # lexname.lexname LIKE "adv.%" AND
    db = MySQLdb.connect(user='root', db="wordnet")
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def getlemmas(letters):
    result = {}

    pairs = getwords(letters)

    for pos, word in pairs:
        pos = re.sub('\..+$', '', pos)
        if pos not in result.keys():
            result[pos] = []
        result[pos].append(word)
    return json.dumps(result)
