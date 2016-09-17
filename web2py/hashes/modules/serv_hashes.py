#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

#INI_UIKS = myconf.take('files.ini_uiks')
IN_FOLDER = myconf.take('files.in_folder')
OUT_FOLDER = myconf.take('files.out_folder')

#!/usr/bin/env python
# coding: utf8

import os
import hashlib
import base58

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

#filename = u'Снимок экрана (4).png'
#in_folder = u'C:/Users/adm/Pictures/Screenshots/'
#out_folder = u'C:/rost/3456/'
def hash_file(in_folder, out_folder, basename, extension):
    path_filename = os.path.join(in_folder, basename + extension)
    # m = hashlib.md5()
    h = hashlib.new('sha256') # выбор алгоритма
    fd = open(path_filename, 'rb')
    h.update(fd.read())
    fd.close()

    hash58 = base58.b58encode(h.digest())

    return hash58


def dir_hash(db):

    in_folder = IN_FOLDER.replace('\\', '/')
    out_folder = OUT_FOLDER.replace('\\', '/')
    used_extensions = ['.jpg', '.png', '.gif']

    rename = []
    for f_user in os.listdir(in_folder):

        in_folder_user = os.path.join(in_folder, f_user)
        print 'user folder:', in_folder_user
        if not os.path.isdir(in_folder_user):
            continue

        for name in os.listdir(in_folder_user):

            basename, extension = os.path.splitext(name)
            print 'basename, extension:', basename, extension
            name_items = basename.split(' ')
            if len(name_items) < 3:
                # it is not screenshoot
                continue

            if used_extensions:
                if extension not in used_extensions:
                    #print 'not ext:', extension
                    continue

            print 'USER:', f_user, 'name_items:', name_items

            hash58 = hash_file(in_folder_user, out_folder, basename, extension)

            print hash58

            f_tik = name_items[0]
            f_uik = name_items[1]
            f_name = name_items[2]
            try:
                int_probe = int(f_tik)
                int_probe = int(f_uik)
            except:
                print 'tik - uik not integer!'
                continue

            rename.append([os.path.join(in_folder_user, name), f_tik, f_uik, f_name + extension])

            is_exist = db(db.t_files.f_hash == hash58).select().first()
            if is_exist != None:
                print 'already exist'
                continue

            date_time = datetime.now()

            #print date_time
            db.t_files.insert(f_tik = f_tik, f_uik = f_uik, f_user = f_user,
                             f_date = date_time, f_hash = hash58,
                             f_name = f_name, f_ext = extension)

        db.commit()
        # if COMMIT is OK
        for item in rename:

            new_file_path_name = os.path.join(out_folder, item[1], item[2], f_user, item[3])
            if os.path.exists(new_file_path_name):
                os.remove(new_file_path_name)

            try:
                print item[0], '-->>', new_file_path_name
                os.rename(item[0], new_file_path_name)
            except:
                try:
                    os.mkdir(os.path.join(out_folder,item[1]))
                    os.mkdir(os.path.join(out_folder, item[1], item[2]))
                    os.mkdir(os.path.join(out_folder, item[1], item[2], f_user))
                    os.rename(item[0], new_file_path_name)
                except:
                    try:
                        os.mkdir(os.path.join(out_folder, item[1], item[2]))
                        os.mkdir(os.path.join(out_folder, item[1], item[2], f_user))
                        os.rename(item[0], new_file_path_name)
                    except:
                        try:
                            os.mkdir(os.path.join(out_folder, item[1], item[2], f_user))
                            os.rename(item[0], new_file_path_name)
                        except:
                            print 'error making path:', new_file_path_name
                            continue



    return

def get(db, not_local, interval=None):
    interval = interval or 55
    print __name__, 'not_local:',not_local, ' interval:', interval
    not_local = not_local == 'True'

    i_p3 = period3 = interval * 3
    while True:


        print '\n', datetime.now()

        dir_hash(db)
        db.commit()

        sleep(interval)

if Test: get(db)

# если делать вызов как модуля то нужно убрать это иначе неизвестный db
import sys
#print sys.argv
if len(sys.argv)>1:
    get(db, sys.argv[1], float(sys.argv[2]))
