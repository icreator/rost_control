# -*- coding: utf-8 -*-

if request.ajax:
    pass
else:
    ## gift code?
    if session.gc:
        GIFT_CODE = session.gc
    elif request.cookies.has_key('gift_code'):
        GIFT_CODE = request.cookies['gift_code'].value
    else:
        GIFT_CODE = None
    
    var_gc = request.vars.gc

    if not GIFT_CODE and var_gc:
        from gifts_lib import store_in_cookies
        store_in_cookies(var_gc)
        session.gc=var_gc
        session.bonus_recalc = True
            
    if var_gc:
        request.vars.pop('gc')
        redirect(URL(args=request.args, vars=request.vars))

    # if set land in vars - store and redirect
    _ = request.vars.lang
    if _ and _ != session.lang:
        session.lang = _
        vars = request.vars
        vars.pop('lang')
        redirect(URL( args = request.args, vars = vars))

# set a localizations
if session.lang and T.accepted_language != session.lang:
    #print '0.py - forsed T.[%s]' % session.lang
    T.force(session.lang)
