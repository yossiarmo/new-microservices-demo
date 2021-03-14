#!/bin/bash
set -xe
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
kubectl create ns hipster
kubectl apply -n hipster -f  $DIR/../release/kubernetes-manifests.yaml
kubectl create clusterrolebinding hipster-ns-default-sa --clusterrole=cluster-admin --serviceaccount=hipster:default