#!/root/anaconda2/bin/python
import os

process = "run.py"
log = "out.log"
os.system("kill -9 $(ps -ef|grep " + process + '|grep -v "grep"|awk ' + "'{print $2}')")
os.system("nohup python -u " + process + " >> " + log + " 2>&1 &")
