#!/bin/bash
set -xe
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
kubectl delete ns hipster
kubectl delete clusterrolebinding hipster-ns-default-sa 
