# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()

import os
import hashlib
import base58
import datetime

#filename = u'Снимок экрана (4).png'
#in_folder = u'C:/Users/adm/Pictures/Screenshots/'
#out_folder = u'C:/rost/3456/'
def hash_file(in_folder, out_folder, basename, extension):
    path_filename = in_folder + basename + extension
    # m = hashlib.md5()
    h = hashlib.new('sha256') # выбор алгоритма
    fd = open(path_filename, 'rb')
    fd_read = fd.read()
    h.update(fd_read)
    fd.close()
    hash58 = base58.b58encode(h.digest())
    if False:
        if False:
            new_name = out_folder + hash58
        else:
            new_name = out_folder + basename
        try:
            os.rename(path_filename, new_name + extension)
        except:
            os.mkdir(out_folder)
            os.rename(path_filename, new_name + extension)
    else:
        new_name = basename
        
    #print hash58, new_name
    return hash58, new_name, fd_read


def dir_hash():
    
    response.no_function = True
    ##fname = os.path.join(dirname, filename).replace('\\', '/')
    #in_folder = u'C:/Users/adm/Pictures/Screenshots/'.replace('\\', '/')
    in_folder = u'C:/uik_test/'.replace('\\', '/')
    out_folder = u'C:/uik_test_hashes/'.replace('\\', '/')
    used_extensions = ['.jpg', '.png', '.gif']
    output = {}

    rename = []
    for name in os.listdir(in_folder):
            
        if os.path.isdir(os.path.join(in_folder, name)):
            continue
        
        basename, extension = os.path.splitext(name)
        print basename, extension
        name_items = basename.split(' ')
        if len(name_items) < 2:
            # it is not screenshoot
            continue
            
        print 'name_items:', name_items
        
        if used_extensions:
            if extension not in used_extensions:
                print 'not ext:', extension
                continue
        
        hash58, new_file_name, fd_read = hash_file(in_folder, out_folder, basename, extension)
        
        print hash58, new_file_name
        
        is_exist = db(db.t_files.f_hash == hash58).select().first()
        if is_exist != None:
            # already exist
            continue
        
        date_time = datetime.datetime.now()
            
        print date_time
        db.t_files.insert(f_tik = name_items[0], f_uik = name_items[1],
                         f_date = date_time, f_hash = hash58,
                         f_name = new_file_name, f_ext = extension,
                         f_file = fd_read, f_file_blob = fd_read)
        
        rename.append([in_folder + name, out_folder + new_file_name + extension])
        output[name] = dict( new_name = new_file_name, hash58 = hash58)
    
    db.commit()
    # if COMMIT is OK
    for item in rename:
        try:
            os.rename(item[0], item[1])
        except:
            os.mkdir(out_folder)
            os.rename(item[0], item[1])
    
    h_output = CAT()
    for k,v in output.iteritems():
        h_output += DIV(k, ' - ', v)
        
    h = CAT(
        H2('Hashes'),
        DIV('Input Folder: ', in_folder),
        DIV('Output Folder: ', out_folder),
        DIV('Used Extensions: ', used_extensions),
        DIV(H3('Output'),
            h_output),
        )
    
    return dict(h = h)
    
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
