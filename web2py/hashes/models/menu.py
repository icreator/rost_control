if request.ajax:
    pass
else:
    response.title = settings.title
    response.subtitle = settings.subtitle
    response.meta.author = '%(author)s <%(author_email)s>' % settings
    response.meta.keywords = settings.keywords
    response.meta.description = settings.description
    response.menu = [
    (T('Index'),URL('default','index')==URL(),URL('default','index'),[]),
    (T('Hashes'),URL('default','hashes_manage')==URL(),URL('default','hashes_manage'),[]),
    ]
