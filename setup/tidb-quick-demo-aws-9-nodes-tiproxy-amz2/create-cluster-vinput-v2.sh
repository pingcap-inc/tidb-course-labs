#!/bin/bash
VERSION=${1}
REGION_NAME=${2}

source ./cloud-env.sh
~/.tiup/bin/tiup mirror set https://tiup-mirrors.pingcap.com
~/.tiup/bin/tiup update --self
~/.tiup/bin/tiup update cluster
~/.tiup/bin/tiup mirror set tidb-community-server-${VERSION}-linux-amd64
./01-precheck-and-fix-nodes.sh ${REGION_NAME}

# Creating the TiDB cluster named tidb-demo, version ${VERSION}
~/.tiup/bin/tiup cluster deploy tidb-demo ${VERSION} ./eleven-nodes.yaml --user ec2-user -i /home/ec2-user/.ssh/pe-class-key-${REGION_NAME}.pem --yes

sleep 3;

./start-cluster.sh

ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/.ssh/pe-class-key-oregon.pem ec2-user@${HOST_TIPROXY1_PRIVATE_IP} << EOFX
~/.tiup/bin/tiup mirror set https://tiup-mirrors.pingcap.com
~/.tiup/bin/tiup update --self
~/.tiup/bin/tiup tiproxy --config ./tiproxy.toml
EOFX

ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/.ssh/pe-class-key-oregon.pem ec2-user@${HOST_TIPROXY2_PRIVATE_IP} << EOFX
~/.tiup/bin/tiup mirror set https://tiup-mirrors.pingcap.com
~/.tiup/bin/tiup update --self
~/.tiup/bin/tiup tiproxy --config ./tiproxy.toml
EOFX