
set prog=web2py.py
set app=hashes
set not_local=True
set interval=10


:rep
python ..\..\%prog% -S %app% -M -R applications/%app%/modules/serv_datachain.py -A %not_local% %interval%

timeout /t 10
goto rep

pause