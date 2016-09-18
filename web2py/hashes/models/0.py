from gluon.storage import Storage
settings = Storage()

#settings.migrate = True
settings.title = 'hashes of voting'
settings.subtitle = 'blockchain hashes'
settings.author = 'icreator'
settings.author_email = 'icreator@mail.ru'
settings.keywords = 'blockchain'
settings.description = 'blockchain startup hash'
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = '3fa7b7d5-e936-496f-90a8-34f8f4edd672'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []

from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

DEVELOP = myconf.take('app.develop', cast=bool)
APP_NAME = myconf.take('app.name')

if request.ajax:
    ##session.forget(response)
    pass
else:
    from gluon import current
    current.IS_LOCAL = IS_LOCAL = request.is_local
    current.IS_MOBILE = IS_MOBILE = request.user_agent().is_mobile
    current.IS_TABLET = IS_TABLET = request.user_agent().is_tablet
    current.ADMIN = ADMIN = request.controller == 'appadmin'
    
    SKIN = myconf['skin']

    LANGS = {
        'ru': ['Русский', 'ru.png'],
        'en': ['English', 'gb.png'],
        'de': ['Deutsche ', 'de.png'],
        'tr': ['Türkçe', 'tr.png'],
    }

if DEVELOP:
    print 'in 0', request.ajax and 'AJAX' or '', request.url, request.env.REMOTE_ADDR, request.now
