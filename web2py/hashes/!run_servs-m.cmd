rem start !clear_sessions.cmd
rem start !clear_errors.cmd


set prog=web2py.py
set app=hashes
set not_local=True
set interval=1


:rep
..\..\%prog% -S %app% -M -R applications/%app%/modules/serv_hashes.py -A %not_local% %interval%

timeout /t 4
goto rep

pause