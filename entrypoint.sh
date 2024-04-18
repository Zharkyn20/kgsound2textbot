#!/bin/bash

# Start server
echo "Starting server"

uvicorn main:app --reload --port 50

exec "$@"
