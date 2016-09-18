### we prepend t_ to tablenames and f_ to fieldnames for disambiguity


########################################
db.define_table('t_hashes',
    Field('f_url', type='string',
          label=T('URL'),
          comment = T('Ссылка на хранилище файлов')),
    Field('f_descr', type='text',
          label=T('Описание'),
          comment = T('Описание файлов отпечатанных в этой записи летописи')),
    Field('f_hashes', type='text',
          label=T('Отпечатки'),
          comment = T('Отпечатки в формате Base58[32] разделённые пробелами')),
    Field('f_rec', type='string',
          label=T('ID записи'),
          readable=False, writable=False,
          comment = T('Отпечаток записи летописи в которой запечатлены эти отпечатки')),
    auth.signature,
    format='%(f_rec)s',
    migrate=settings.migrate)

db.define_table('t_hashes_archive',db.t_hashes,Field('current_record','reference t_hashes',readable=False,writable=False))

db.define_table('t_uik',
    Field('f_name', type='string',
          label=T('Название УИК'),
          comment = T('Наименование УИК и адрес')),
    Field('f_url', type='string',
          label=T('URL'),
          comment = T('ссылка для файлов')),
    Field('f_kod', type='integer',
          label=T('Код')),
    Field('f_tik', type='integer',
          label=T('Код ТИК')),
    format='%(f_name)s',
    #fake_migrate=True,
    migrate=settings.migrate)

########################################
## hash -> name_file as HASH + EXTENSION
db.define_table('t_files',
    Field('f_tik', type='integer',
          label=T('ТИК')),
    Field('f_uik', type='integer',
          label=T('УИК')),
    Field('f_user', type='string',
          label=T('ОПЕРАТОР')),
    Field('f_date', type='datetime',
          label=T('Время создания'),
          comment = T('')),
    Field('f_hash', type='string',
          label=T('ХЭШ')),
    Field('f_name', type='string',
          label=T('Имя файла'),
          comment = T('ТИК УИК ВРЕМЯ')),
    Field('f_ext', type='string', length=20,
          label=T('Расширение файла'),
          comment = T('.png .jpg .bmp')),
    Field('f_txid1_datachain', type='string', length = 100,
          # 4Pyob89gnoUGDtWMLf7d74JKJaWcYmiJZBWZxpSSaSEPKQRoKdV56KWxbrKaMCJpQBLxgAFnNPQwWEA3GgfQjR3v
          label=T('Хэш Записи в DATACJAINS.World'),
          comment = T('Хэш записи летописи в которой сохранён данный ХЭШ')),
    Field('f_txid2_emerchain', type='string', length = 100,
          label=T('Хэш Записи в Emercoin'),
          comment = T('Хэш записи летописи в которой сохранён данный ХЭШ')),
    format='%(f_hash)s',
    migrate=settings.migrate)

if db(db.t_files).isempty():
    db.t_files.truncate()
    #import serv_hashes
    #serv_hashes.ini_uiks(db)

    
db.define_table('t_folders',
    Field('f_folder',
          label=T('folder')),
    Field('f_counter', 'integer', default = 0,
          label=T('last file')),
    Field('f_last_file',
          label=T('last file')),
    format='%(f_folder)s',
    migrate=settings.migrate)


db.define_table('t_values',
    Field('f_files_count', type='integer',
          default = 0,
          comment = T('counter for T_FILES')),
    Field('f_files_txid_1', type='integer',
          default = 0,
          comment = T('counter for records in DATACHANS')),
    Field('f_files_txid_2', type='integer',
          default = 0,
          comment = T('counter for records in Emercoin')),
    Field('f_date', type='datetime',
          default = request.now,
          label=T('Время создания'),
          comment = T('')),
    format='%(f_hash)s',
    migrate=settings.migrate)

if db(db.t_values).isempty():
    db.t_values.insert()
