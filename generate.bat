@echo off
set /a i = 30
set /a n = 3000
set python = "c:\Runtime_x86\Python\python.exe"

:while 
if %i% leq 100  (
	echo *************************
	echo %n%
	echo *************************
        %python% main.py %n% 10 > "out\\%i%.cnf"
        set /a n = n+100
        set /a i = i+1
	goto :while
)

