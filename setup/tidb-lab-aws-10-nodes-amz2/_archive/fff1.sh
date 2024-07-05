#!/bin/bash
REGION_NAME=${1}

# Fast forward E1
./destroy-all.sh
./create-cluster-v750.sh ${REGION_NAME}
