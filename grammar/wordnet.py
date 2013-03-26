import json
import MySQLdb
import os
import re


def getwords(letters):
    if not letters.strip():
        return []

    sql = '''
    SELECT lexname.lexname, lemma FROM word
    INNER JOIN sense ON sense.wordno=word.wordno
    INNER JOIN synset ON synset.synsetno=sense.synsetno
    INNER JOIN lexname ON lexname.lexno=synset.lexno
    WHERE lemma REGEXP "^[%s]{4,}$"
    GROUP BY lemma
    '''
    # lexname.lexname LIKE "adv.%" AND
    db = MySQLdb.connect(host=os.environ.get('DB_HOST', 'localhost'),
                         user=os.environ.get('DB_USER', 'root'),
                         passwd=os.environ.get('DB_PASSWORD', ''),
                         db=os.environ.get('DB_NAME', 'wordnet'))
    cursor = db.cursor()
    cursor.execute(sql, [letters])
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
