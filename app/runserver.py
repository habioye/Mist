#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Author: Benjamin Nadon
#-----------------------------------------------------------------------

from sys import exit, stderr
from app import app
from os import system, environ



def main():

    try:
        port = int(environ.get("PORT", 33507))
        system('gunicorn -b 0.0.0.0:' + port + ' --access-logfile - mist-princeton:app')
        #app.run(host = "0.0.0.0", port = port, debug = True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
