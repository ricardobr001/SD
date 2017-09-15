from subprocess import call

call(['gnome-terminal' , '-e' ,'bash','--command','python Process.py 25000 0'])
call(['gnome-terminal' , '-e' ,'bash','--command','python Process.py 25001 1'])
call(['gnome-terminal' , '-e' ,'bash','--command','python Process.py 25002 2'])
