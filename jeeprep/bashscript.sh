#!/bin/bash

echo "Killing all Django runserver processes..."

# Find and kill processes running "manage.py runserver"
pids=$(ps aux | grep "manage.py runserver" | grep -v grep | awk '{print $2}')

if [ -z "$pids" ]; then
    echo "No Django processes found."
else
    echo "Killing PIDs: $pids"
    kill -9 $pids
    echo "All Django processes killed."
fi
