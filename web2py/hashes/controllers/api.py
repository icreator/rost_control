# -*- coding: utf-8 -*-

response.generic_patterns = ['json', 'html']

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
        return {'error':'error'}
        
    if (request.vars.get('update')):
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


def set_txid1():
    from_rec = request.args(0) or 0
    limit_rec = request.args(1) or 100
    try:
        from_rec = int(from_rec)
        limit_rec = int(limit_rec)
    except:
        return {'error':'error'}
        
    if limit_rec and from_rec:
        recs = db().select(db.t_files.ALL, limitby=(from_rec, from_rec + limit_rec))
    else:
        recs = db(db.t_files).select(limitby=(0, limit_rec))

    for row in recs:
        #if row.f_txid1_datachain != None or len(row.f_txid1_datachain) > 60:
        #    continue
        row.update_record( f_txid1_datachain = request.args(2))

def index():
    return dict(message="hello from api.py")
