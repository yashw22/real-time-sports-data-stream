#!/bin/bash

KAFKA_URL="http://broker:9092/health"
MAX_RETRIES=12
RETRY_INTERVAL=5

# Function to check Kafka server health
check_kafka_health() {
  response=$(curl --write-out "%{http_code}" --silent --output /dev/null "$KAFKA_URL")
  echo $response
  [[ "$response" -eq 200 ]]
}

# Wait for Kafka to be up
for ((attempt=1; attempt<=MAX_RETRIES; attempt++)); do
  if check_kafka_health; then
    echo "Kafka server is up and running!"
    exec "$@" # Execute any additional commands passed to the script
    exit 0
  fi
  echo "Kafka server is not available. Attempt $attempt/$MAX_RETRIES. Retrying in $RETRY_INTERVAL seconds..."
  sleep $RETRY_INTERVAL
done

echo "Kafka server is still not available after $MAX_RETRIES attempts. Exiting."
exit 1
