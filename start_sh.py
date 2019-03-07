#!/root/anaconda2/bin/python
import os

process = "run.py"
log = "out.log"
os.system("nohup python -u " + process + " >> " + log + " 2>&1 &")
