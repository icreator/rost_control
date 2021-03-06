# -*- coding: utf-8 -*-

response.generic_patterns = ['json', 'html']


def proc():
    import os
    import base58
    import serv_hashes
    from datetime import datetime
    
    in_folder = myconf.take('files.in_folder').replace('\\', '/')
    used_extensions = None #['.jpg', '.png', '.gif']

    stop_counter = 200
    
    for f_user in os.listdir(in_folder):

        in_folder_user = os.path.join(in_folder, f_user)
        #print 'user folder:', in_folder_user
        if not os.path.isdir(in_folder_user):
            continue

        last_name = None
        folder_counter_rec = db(db.t_folder.f_folder == f_user).select().first()
        if folder_counter_rec == None:
            folder_counter_rec_id = db.t_folder.insert( f_folder = f_user)
            folder_counter_rec = db.t_folder[folder_counter_rec_id]
        
        folder_counter = folder_counter_rec.f_counter
        
        current_folder_counter = 0
        for name in os.listdir(in_folder_user):

            current_folder_counter += 1

            last_name = name

            if current_folder_counter <= folder_counter:
                continue

            in_folder_user_file = os.path.join(in_folder_user, name)
            if os.path.isdir(in_folder_user_file):
                continue

            basename, extension = os.path.splitext(name)
            #print 'basename, extension:', basename, extension
            #if True:
            try:
                name_items_2 = basename.split(' ')
                name_items = name_items_2[0].split('-')
                #print name_items
                name_items.append(name_items_2[1])
                #print name_items
                if len(name_items) < 3:
                    #print 'len < 3'
                    # it is not screenshoot
                    continue
            #else:
            except:
                continue

            if used_extensions:
                if extension not in used_extensions:
                    #print 'not ext:', extension
                    continue

            #print 'USER:', f_user, 'name_items:', name_items

            hash58 = serv_hashes.hash_file( in_folder_user, basename, extension)

            #print hash58

            f_tik = name_items[0]
            f_uik = name_items[1]
            f_name = name_items[2]
            try:
                int_probe = int(f_tik)
                int_probe = int(f_uik)
            except:
                print 'tik - uik not integer!'
                continue

            ##rename.append([os.path.join(in_folder_user, name), f_tik, f_uik, f_name + extension])

            is_exist = db(db.t_files.f_hash == hash58).select().first()
            if not is_exist:
                date_time = datetime.now()

                #print date_time
                db.t_files.insert(f_tik = f_tik, f_uik = f_uik, f_user = f_user,
                                 f_date = date_time, f_hash = hash58,
                                 f_name = f_name, f_ext = extension)
            
            stop_counter -= 1
            if stop_counter < 0:
                folder_counter_rec.update_record( f_counter = current_folder_counter, f_last_file = name)
                db.commit()
                return '%s %s %s' % (f_user, name, current_folder_counter)

        if current_folder_counter < folder_counter_rec.f_counter:
            folder_counter_rec.update_record( f_counter = current_folder_counter, f_last_file = last_name)
            db.commit()

# init folders
def ini_uiks():
    import os
    if db(db.t_uik).isempty():
        db.t_uik.truncate()
    else:
        return ' already initiated'
    
    IN_FOLDER = myconf.take('files.in_folder').replace('\\', '/')
    INI_UIKS = myconf.take('files.ini_uiks')
    f = open(os.path.join(request.folder, INI_UIKS))
    for line in f.readlines():
        fields = line.split(';')
        kod = fields[1].split('-')
        #print kod

        try:
            db.t_uik.insert(f_name = fields[0], f_kod = kod[0], f_tik = kod[1],
                        f_url = fields[2])
        except:
            continue

        try:
            os.mkdir(os.path.join(IN_FOLDER,fields[1]))
        except:
            pass
        
        
def get():
    from_rec = request.args(0) or 0
    limit_rec = request.args(1) or 100
    try:
        from_rec = int(from_rec)
        limit_rec = int(limit_rec)
    except:
        return {'error': 'error in args'}
        
    if False and request.vars.get('update'):
        import serv_hashes
        serv_hashes.dir_hash(db)

    if limit_rec and from_rec:
        recs = db().select(db.t_files.ALL, limitby=(from_rec, from_rec + limit_rec))
    else:
        recs = db(db.t_files).select(limitby=(0, limit_rec))
        
    rows = {}
    for row in recs:
        row.pop('delete_record')
        row.pop('update_record')
        rows[row.id] = row
    
    #8 926 530 7393 Андрей
    return {'rows': rows, 'count': db(db.t_files.id > 0).count()}

def get_uiks():
    from_rec = request.args(0) or 0
    limit_rec = request.args(1) or 100
    try:
        from_rec = int(from_rec)
        limit_rec = int(limit_rec)
    except:
        return {'error':'error'}

    if limit_rec and from_rec:
        recs = db().select(db.t_uik.ALL, limitby=(from_rec, from_rec + limit_rec))
    else:
        recs = db(db.t_uik).select(limitby=(0, limit_rec))
        
    rows = {}
    for row in recs:
        row.pop('delete_record')
        row.pop('update_record')
        rows[row.id] = row
    
    #8 926 530 7393 Андрей
    return {'rows': rows, 'count': db(db.t_uik.id > 0).count()}



def set_txid1():
    from_rec = request.args(0) or 0
    limit_rec = request.args(1) or 100
    try:
        from_rec = int(from_rec)
        limit_rec = int(limit_rec)
    except:
        return {'error':'error in args'}
        
    if limit_rec and from_rec:
        recs = db().select(db.t_files.ALL, limitby=(from_rec, from_rec + limit_rec))
    else:
        recs = db(db.t_files).select(limitby=(0, limit_rec))

    for row in recs:
        #if row.f_txid1_datachain != None or len(row.f_txid1_datachain) > 60:
        #    continue
        row.update_record( f_txid1_datachain = request.args(2))

def set_txid2():
    from_rec = request.args(0) or 0
    limit_rec = request.args(1) or 100
    try:
        from_rec = int(from_rec)
        limit_rec = int(limit_rec)
    except:
        return {'error':'error in args'}
        
    if limit_rec and from_rec:
        recs = db().select(db.t_files.ALL, limitby=(from_rec, from_rec + limit_rec))
    else:
        recs = db(db.t_files).select(limitby=(0, limit_rec))

    for row in recs:
        #if row.f_txid1_datachain != None or len(row.f_txid1_datachain) > 60:
        #    continue
        row.update_record( f_txid2_emerchain = request.args(2))

def index():
    return dict(message="hello from api.py")
