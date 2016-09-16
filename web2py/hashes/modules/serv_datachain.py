#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

URL_FILES_SITE = myconf.take('site.url')

URL_DATACHAIN_API = myconf.take('datachain.url_api')
CHAIN_DATA = myconf.take('datachain.data')
CHAIN_PASSWORD = myconf.take('datachain.password')
CHAIN_CREATOR = myconf.take('datachain.creator')
CHAIN_FEEPOW = myconf.take('datachain.feepow')

import os
import hashlib
import base58
import urllib

from time import sleep
from datetime import datetime

try:
    import json
except ImportError:
    from gluon.contrib import simplejson as json
from gluon.tools import fetch

Test = None

# запуск опроса бирж и получение от них цен

def log(db, l2, mess='>'):
    print mess
    db.logs.insert(label123456789='s_rates', label1234567890=l2, mess='%s' % mess)
def log_commit(db, l2, mess='>'):
    log(db, l2, mess)
    db.commit()



def make_record(db):

    t_values = db.t_values[1]
    from_rec = t_values.f_files_txid_1
    to_rec = from_rec + 200
    recs_to_chain = []
    hashes = []
    recs = db(db.t_files).select(limitby=(from_rec, to_rec))
    print 'ger records from - to:', from_rec, to_rec
    last_record_id = from_rec
    for rec in recs:
        print 'rec_id:', rec.id
        last_record_id = rec.id
        if rec.f_txid1_datachain != None and len(rec.f_txid1_datachain) > 30:
            print '   record already chained:', rec.f_txid1_datachain
            continue
        hashes.append(rec.f_hash)
        recs_to_chain.append(rec.id)

    if len(recs_to_chain) == 0:
        return None, None

    #print '-'.join(hashes) ## urllib.urlencode
    params = json.dumps({ 'password': CHAIN_PASSWORD, 'creator': CHAIN_CREATOR, 'feepow': CHAIN_FEEPOW,
              'url': URL_FILES_SITE, 'data': CHAIN_DATA, 'hashes': '-'.join(hashes) })
    #print params
    ## POST
    try:
        api_func = urllib.urlopen(URL_CHAIN_API, params)
        result = api_func.read()
    except Exception, e:
        return e, None

    print result
    if 'signature' in result:
        txid = result['signature']
        for rec in recs:
            if rec.f_txid1_datachain != None and len(rec.f_txid1_datachain) > 30:
                continue
            rec.update_record( f_txid1_datachain = txid)


        ###### COMMIT in ANY case
        t_values.update_record( f_files_txid_1 = last_record_id )
        db.commit()

    return None, result

def run(db, not_local, interval=None):
    interval = interval or 10
    print __name__, 'not_local:',not_local, ' interval:', interval
    not_local = not_local == 'True'

    i_p3 = period3 = interval * 10
    while True:

        print '\n', datetime.now()

        make_record(db)

        print 'sleep:', interval
        sleep(interval)

if Test:
    run(db)

# если делать вызов как модуля то нужно убрать это иначе неизвестный db
import sys
#print sys.argv
if len(sys.argv)>1:
    run(db, sys.argv[1], float(sys.argv[2]))
