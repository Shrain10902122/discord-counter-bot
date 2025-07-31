#!/bin/bash
kill -9 $(lsof -ti:10000) 2>/dev/null || true
python UOcounter.py