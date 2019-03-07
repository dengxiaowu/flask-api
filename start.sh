#!/bin/bash
process="run.py"
log="./$out.log"
echo "$process is start" >> $log
`nohup python -u $process >> $log 2>&1 &`
echo "start success"