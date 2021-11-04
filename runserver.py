#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Author: Benjamin Nadon
#-----------------------------------------------------------------------

from sys import exit, stderr
import argparse
from mapfunctions import app

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
        system('gunicorn -b 0.0.0.0:' + str(port) + ' --access-logfile - mist-princeton:app')
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
