#!/bin/bash
kill -9 $(lsof -ti:8080) 2>/dev/null || true
python UOcounter.py