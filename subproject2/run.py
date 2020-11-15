from subprocess import *

Popen('python subproject2/subproject2.py --path "./data"', shell=True).wait()