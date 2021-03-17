#!/bin/bash
curl -ik -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type: application/json" https://$API_SERVER_HOST:$API_SERVER_PORT/api/v1/namespaces/default/secrets
