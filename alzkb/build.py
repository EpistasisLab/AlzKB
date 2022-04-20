#!/usr/bin/env python

from argparse import ArgumentError
import warnings
import os, sys

def confirm_y_n():
    while True:
        resp = str(input("Continue with operation? (Y/n): ")).lower().strip()
        if resp[0] == 'y':
            return True
        if resp[0] == 'n':
            print("Exiting application...")
            sys.exit(0)
        print("Please enter y or n.")


def bootstrap():
    """
    Retrieve data files needed to build AlzKB from scratch and organize them
    into the required directory structure.
    """
    pass

def build():
    """
    Populate the AlzKB ontology using the local copies of the source databases.
    """
    pass

def install():
    """
    Import the contents of the AlzKB populated ontology into Neoj4.
    """
    pass

def main():
    args = sys.argv

    try:
        assert len(args) > 1
    except AssertionError:
        raise ArgumentError("Error - must provide one of `bootstrap`, `build`, or `install` as an argument to `alzkb`. See the README for more information.")

    if len(args) > 2:
        warnings.warn("Multiple arguments provided - only the first will be used.")

    op_arg = args[1].lower()

    if op_arg == 'bootstrap':
        bootstrap()
    elif op_arg == 'build':
        build()
    elif op_arg == 'install':
        install()
    else:
        raise ArgumentError("Error - must provide one of `bootstrap`, `build`, or `install` as an argument to `alzkb`. See the README for more information.")
