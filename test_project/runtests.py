#!/usr/bin/env python
import os
import sys


test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)


def runtests():
    from django.core.management import execute_from_command_line
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    runtests()
