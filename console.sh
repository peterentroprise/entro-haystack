#!/bin/sh

set -e

# Start hasura console once Graphql server is up
wait-for -t 999999 localhost:8080 -- \
  sleep 5 && hasura-cli console \
    --endpoint http://localhost:8080 \
    --address 0.0.0.0 \
    --no-browser \
    --skip-update-check &
