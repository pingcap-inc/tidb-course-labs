#!/bin/bash
REGION_NAME=${1}

source ./cloud-env.sh

./create-307-cluster-vinput.sh 7.5.4 ${REGION_NAME}