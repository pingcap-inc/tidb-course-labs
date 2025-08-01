#!/bin/bash
#VERSION=${1}
#REGION_NAME=${2}

#source ./cloud-env.sh

#~/.tiup/bin/tiup mirror set tidb-community-server-${VERSION}-linux-amd64
#./01-precheck-and-fix-nodes.sh ${REGION_NAME}

# Creating the TiDB cluster named tidb-test, version ${VERSION}
#~/.tiup/bin/tiup cluster deploy tidb-test ${VERSION} ./solution-topology-ten-nodes.yaml --user ec2-user -i /home/ec2-user/.ssh/pe-class-key-${REGION_NAME}.pem --yes
#sleep 3;

#~/.tiup/bin/tiup cluster start tidb-test

set -e

VERSION=${1}
REGION_NAME=${2}
TOPOLOGY_FILE=${3:-./solution-topology-ten-nodes.yaml}

source ./cloud-env.sh

~/.tiup/bin/tiup mirror set tidb-community-server-${VERSION}-linux-amd64
./01-precheck-307-and-fix-nodes.sh ${TOPOLOGY_FILE} ${REGION_NAME}

# Creating the TiDB cluster named tidb-test, version ${VERSION}
~/.tiup/bin/tiup cluster deploy tidb-test ${VERSION} ${TOPOLOGY_FILE} --user ec2-user -i /home/ec2-user/.ssh/pe-class-key-${REGION_NAME}.pem --yes >> /home/ec2-user/create-cluster-vinput.log 2>&1
sleep 3;

~/.tiup/bin/tiup cluster start tidb-test
