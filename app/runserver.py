#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Author: Benjamin Nadon
#-----------------------------------------------------------------------

from sys import exit, stderr
import argparse
from app import app
import os

def make_parser():
    parser = argparse.ArgumentParser(description =
    'Server for the registrar application',
        allow_abbrev = False)
    parser.add_argument("port", type = int, help =
    "the port at which the server should listen")

    return parser

def main():
    try:
        parser = make_parser()
        args = parser.parse_args()
        port = args.port

    except Exception as ex:
        print(ex, file=stderr)
        exit(2)


    try:
        port = int(os.environ.get("PORT", 33507))
        system('gunicorn -b 0.0.0.0:' + port + ' --access-logfile - mist-princeton:app')
        #app.run(host = "0.0.0.0", port = port, debug = True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
