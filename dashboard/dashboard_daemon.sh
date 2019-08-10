#!/bin/bash
rm dashboard_log.txt
touch dashboard_log.txt
python3 $1 >> dashboard_log.txt &
echo "Use the first number(PID) to kill the process, using kill <PID>"
ps -u $USER -f|grep -m1 "python3"
