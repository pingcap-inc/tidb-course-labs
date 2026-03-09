#!/bin/bash
set -e

## START of EKS and TiDB Operator setup (Lab Steps Candidates)

# Install kubectl, Helm, AWS CLI
sudo bash ~/install-operator-env.sh || true

# =============================================================================
# Phase 2: EKS and TiDB Operator setup
# =============================================================================

# Setup ENV
source ~/cloud-env.sh
source ~/hosts-env.sh

# Configure kubectl for EKS cluster

aws eks update-kubeconfig --region "${REGION_CODE}" --name "${EKS_CLUSTER_NAME}"

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
