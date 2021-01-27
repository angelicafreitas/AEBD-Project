#!/bin/sh
while true
do
  echo "| New Iteration |"
  python3 agent.py 1521 orclpdb1 system Oradoc_db1
  sleep 10
done