#!/bin/bash
set -e

# =============================================================================
# Phase 1: Bootstrap environment (moved from CloudFormation User Data)
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(dirname "$SCRIPT_DIR")"
cd ~

# Install system packages (kubectl, helm, aws cli, mysql-client)
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -qq
sudo apt-get install -y unzip python3-pip mysql-client git

# Create cloud-env.sh with region
REGION_CODE=$(curl -s http://169.254.169.254/latest/meta-data/placement/region)
echo "export REGION_CODE=${REGION_CODE}" > ~/cloud-env.sh

# Copy setup files from lab's setup folder (or clone tidb-course-labs as fallback)
if [ -d "${LAB_ROOT}/setup" ] && [ -f "${LAB_ROOT}/setup/solution-tidb-cluster.yaml" ]; then
  cp -R "${LAB_ROOT}/setup/"* ~/
else
  echo "Cloning tidb-course-labs for setup files..."
  git clone -q https://github.com/pingcap-inc/tidb-course-labs.git /tmp/tidb-course-labs
  cp -R /tmp/tidb-course-labs/labs/demo_010o/* ~/
  cp /tmp/tidb-course-labs/setup/tidb-lab-mysql-init-amz2/show-mysql-password.sh ~/ 2>/dev/null || true
  rm -rf /tmp/tidb-course-labs
fi
chmod +x ~/*.sh 2>/dev/null || true

# Install kubectl, Helm, AWS CLI
sudo bash ~/install-operator-env.sh || true

# Add hosts-env.sh to bashrc
grep -q 'hosts-env.sh' ~/.bashrc 2>/dev/null || echo 'if [ -f ~/hosts-env.sh ]; then source ~/hosts-env.sh; fi' >> ~/.bashrc

# =============================================================================
# Phase 2: EKS and TiDB Operator setup
# =============================================================================

# Setup ENV
source ~/cloud-env.sh

# REGION_NAME may come from platform; fallback to REGION_CODE or instance metadata
REGION_NAME=${REGION_NAME:-${REGION_CODE:-$(curl -s http://169.254.169.254/latest/meta-data/placement/region)}}
echo export REGION_NAME=${REGION_NAME} >> ~/cloud-env.sh

# EKS lab: monitor-only topology - bastion connects to EKS
echo export HOST_MONITOR1_PRIVATE_IP=${HOST_MONITOR1_PRIVATE_IP} > ./hosts-env.sh
echo export HOST_MONITOR1_PUBLIC_IP=${HOST_MONITOR1_PUBLIC_IP} >> ./hosts-env.sh
echo export HOST_CM_PRIVATE_IP=${HOST_MONITOR1_PRIVATE_IP} >> ./hosts-env.sh
echo export HOST_CM_PUBLIC_IP=${HOST_MONITOR1_PUBLIC_IP} >> ./hosts-env.sh

# Configure kubectl for EKS cluster
EKS_CLUSTER_NAME=${EKS_CLUSTER_NAME:-tidb-demo-eks}
REGION=${REGION_NAME:-$(curl -s http://169.254.169.254/latest/meta-data/placement/region)}

aws eks update-kubeconfig --region "${REGION}" --name "${EKS_CLUSTER_NAME}"

echo export EKS_CLUSTER_NAME=${EKS_CLUSTER_NAME} >> ./hosts-env.sh
echo export TIDB_PORT=4000 >> ./hosts-env.sh

source ./hosts-env.sh

echo "ssh -i ~/.ssh/pe-class-key-${REGION_NAME}.pem ${HOST_CM_PRIVATE_IP}" > ./ssh-to-cm.sh
echo "ssh -i ~/.ssh/pe-class-key-${REGION_NAME}.pem ${HOST_MONITOR1_PRIVATE_IP}" > ./ssh-to-monitor1.sh
chmod +x ./*.sh

# Install TiDB Operator via Helm
export KUBECONFIG=$HOME/.kube/config
helm repo add pingcap https://charts.pingcap.org
helm repo update

# Create namespace and install TiDB Operator
kubectl create namespace tidb-admin 2>/dev/null || true
helm upgrade --install tidb-operator pingcap/tidb-operator \
  --namespace tidb-admin \
  --set operatorImage=pingcap/tidb-operator \
  --wait

# Create tidb-cluster namespace and deploy TidbCluster
kubectl create namespace tidb-cluster 2>/dev/null || true

# Use TIDB_VERSION from lab if set, otherwise default
TIDB_VER=${TIDB_VERSION:-v8.1.1}
sed "s|version:.*|version: ${TIDB_VER}|" ./solution-tidb-cluster.yaml > ./solution-tidb-cluster-deploy.yaml
kubectl apply -f ./solution-tidb-cluster-deploy.yaml

# Wait for TiDB cluster to be ready
echo "Waiting for TiDB cluster to be ready on EKS (this may take 5-10 minutes)..."
kubectl wait --for=condition=Ready tidbcluster/tidb-demo -n tidb-cluster --timeout=900s || true

# Get TiDB LoadBalancer hostname for connection (internal NLB, accessible from bastion in same VPC)
TIDB_LB=$(kubectl get svc -n tidb-cluster tidb-demo-tidb -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>/dev/null || true)
if [ -n "${TIDB_LB}" ]; then
  echo export TIDB_HOST=${TIDB_LB} >> ./hosts-env.sh
  TIDB_CONNECT_HOST=${TIDB_LB}
else
  # Fallback: use port-forward for connection
  echo export TIDB_HOST=127.0.0.1 >> ./hosts-env.sh
  echo export TIDB_PORT_FORWARD=4000 >> ./hosts-env.sh
  TIDB_CONNECT_HOST=127.0.0.1
  echo "Note: Run 'kubectl port-forward -n tidb-cluster svc/tidb-demo-tidb 4000:4000' to connect via mysql -h 127.0.0.1 -P 4000 -u root"
fi

# Setup Java (for compatibility with other labs)
if [ -f ./template-JdbcConnect.java ]; then
  cp ./template-JdbcConnect.java ./JdbcConnect.java
  sed -i'' -e "s/<HOST_DB1_PRIVATE_IP>/${TIDB_CONNECT_HOST}/g" -e "s/<HOST_DB2_PRIVATE_IP>/${TIDB_CONNECT_HOST}/g" -e "s/4000/4000/g" ./JdbcConnect.java 2>/dev/null || true
fi

# Setup Python (for compatibility with other labs)
if [ -f ./template-PythonConnect.py ]; then
  cp ./template-PythonConnect.py ./PythonConnect.py
  sed -i'' -e "s/<HOST_DB1_PRIVATE_IP>/${TIDB_CONNECT_HOST}/g" -e "s/<HOST_DB2_PRIVATE_IP>/${TIDB_CONNECT_HOST}/g" -e "s/4000/4000/g" ./PythonConnect.py 2>/dev/null || true
fi

echo "TiDB Operator on EKS lab environment prepared for user ${USER_UNIQUE_TAG}." > MONITOR_PREPARE_DONE
