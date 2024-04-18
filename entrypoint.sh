#!/bin/bash

# Start server
echo "Starting server"

uvicorn main:app --reload --port 5000

exec "$@"
