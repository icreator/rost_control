# -*- coding: utf-8 -*-
response.generic_patterns = ['json', 'html']

def get():
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
        recs = db().select(db.t_files.ALL, limitby=(from_rec))
    rows = {}
    for row in recs:
        row.pop('delete_record')
        row.pop('update_record')
        rows[row.id] = row
    
    #8 926 530 7393 Андрей
    return {'rows': rows, 'count': db(db.t_files.id > 0).count()}

def index():
    return dict(message="hello from api.py")
