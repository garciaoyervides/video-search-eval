#!/bin/bash
CWD=$(pwd)
$CWD/venv/bin/python -m streamlit run frontend.py --server.maxUploadSize=4000 --server.fileWatcherType none