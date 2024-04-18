#!/bin/bash

# Start server
echo "Starting server"

uvicorn main:app --reload --port 443

exec "$@"
