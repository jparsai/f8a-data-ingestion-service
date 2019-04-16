#!/usr/bin/bash

# Start API ingestion service with time out
gunicorn --pythonpath /src/ -b 0.0.0.0:5000 -t $API_INGESTION_SERVICE_TIMEOUT -k $CLASS_TYPE -w $WORKER_COUNT rest_api:app