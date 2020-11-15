import os, nltk
from subprocess import *

if not os.path.isdir("output"):
    os.makedirs("output")
else:
    os.replace("output", "output")

try:
    nltk.data.find('tokenizer/punkt')
except:
    nltk.download('punkt')

Popen('python subproject1/subproject1.py --path "./data"', shell=True).wait()