#!/bin/bash

# Start server
echo "Starting server"

uvicorn main:app --reload --port 8001

exec "$@"
