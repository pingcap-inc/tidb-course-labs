#!/bin/bash
REGION_NAME=${1}

source ./cloud-env.sh

./create-307-cluster-vinput.sh 7.5.1 ${REGION_NAME}