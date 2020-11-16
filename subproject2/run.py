from subprocess import *
import time

Popen('python subproject2/subproject2.py --path "./data"', shell=True).wait()