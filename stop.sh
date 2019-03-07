#!/bin/bash
process="run.py"
log="./$out.log"
echo "$process is stop" >> $log
`kill -9 $(ps -ef|grep $process|grep -v "grep"|awk '{print $2}')`
echo "stop success"