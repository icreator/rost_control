# -*- coding: utf-8 -*-



def index():
    hash = request.args(0)
    if hash == None:
        return dict()

    h = CAT()

    hash_rec = db(db.t_files.f_hash == hash).select().first()
    if hash_rec == None:
        h += H3(T('Такой отпечаток %s не найден') % hash)
        return dict(h=h)

    
    
    h += CAT(
        H2(T('Отпечаток файла')),
        H3(A(hash, _href='http://54.194.119.240:9180/index/blockexplorer.html?tx=%s' % hash_rec.f_rec, _target='blank')),
        
        IMG(_src=URL('static', 'hashes/%s' % (hash + '.' + hash_rec.f_ext)))
        )

    return dict(h = h)
