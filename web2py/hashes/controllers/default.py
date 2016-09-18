# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()

import os
import datetime

    
def call_datachain(pars):
    import gluon.contrib.simplejson as js
    pars = {
        'sender': '78JFPWVVAVP3WW7S8HPgSkt24QF2vsGiS5',
        'feePow': 0, 'password': '1',
        'url': pars.f_url,
        'data': pars.f_descr,
        'hashes': pars.f_hashes
        }
    pars = js.dumps(pars)
    import urllib
    if True:
    #try:
        encode_pars = urllib.unquote_plus(pars)
        print encode_pars
        page = urllib.urlopen('http://127.0.0.1:9085/rec_hashes', encode_pars)
        result = page.read()
    #except:
    else:
        pass
    #get_url = '=1&url=123'
    #fetch('
    return result

### end requires
def index():

    import os
    
    h = CAT(H1('ХЭШ SHA256 файла'),
            H2('ТИК - УИК - ВРЕМЯ - ОПЕРАТОРА - ИМЯ_ФАЙЛА'),
            H2('Ссылки на записи этого хэша файла в блокчейнах'))
    
    count = db(db.t_files.id > 0).count()
    if count < 100:
        count = 100

    
    for rec in db(db.t_files).select(limitby=(count - 100, count)):
        h += DIV(
            DIV(H3(rec.f_hash), 
                H4(rec.f_tik, ':', rec.f_uik, ' ', rec.f_date, ' ', rec.f_user, ' -', rec.f_name),
                H4(A(B('DATACHAINs.World explorer'), _href='#', _target='blank')),' ', H4(A(B('Emercoin explorer'), _href='#', _target='blank')),
               _class='col-sm-8'),
            DIV(IMG(_src=URL('static',os.path.join('hashes', '%s' % rec.f_tik, '%s' % rec.f_uik, '%s' % rec.f_user, rec.f_name + rec.f_ext),
                             ), _height=200),
               _class='col-sm-4'),
            _class='row')
    return dict(h = h)

def error():
    return dict()

@auth.requires_login()
def hashes_manage():
    form = SQLFORM.smartgrid(db.t_hashes,onupdate=auth.archive)
    return locals()
