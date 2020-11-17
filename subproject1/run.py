import os, nltk, shutil
from subprocess import *

if os.path.isdir("output"):
    shutil.rmtree("output")

os.makedirs("output")

try:
    nltk.data.find('tokenizer/punkt')
except:
    nltk.download('punkt')

Popen('python subproject1/subproject1.py --path "./data"', shell=True).wait()