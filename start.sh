#!/bin/bash
redis-server --daemonize yes

sleep 3

uvicorn main:app --host 0.0.0.0 --port 8000