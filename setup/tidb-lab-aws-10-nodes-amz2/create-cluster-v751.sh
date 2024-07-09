#!/bin/bash
REGION_NAME=${1}

source ./cloud-env.sh

./create-cluster-vinput.sh 7.5.1 ${REGION_NAME}