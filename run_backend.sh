#!/bin/bash
CWD=$(pwd)
$CWD/venv/bin/python -m flask run --no-debugger --no-reload  --host="0.0.0.0" -p 5000