#!/bin/bash
process="run.py"
log="./$out.log"
echo "$process is restart" >> $log
`kill -9 $(ps -ef|grep $process|grep -v "grep"|awk '{print $2}')`
`nohup python -u $process >> $log 2>&1&`
echo "restart success"