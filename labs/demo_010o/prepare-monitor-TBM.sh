#!/bin/bash
set -e

## START of EKS and TiDB Operator setup (Lab Steps Candidates)

# Install kubectl, Helm, and AWS CLI for TiDB Operator on EKS
sudo bash ~/install-operator-env.sh

# =============================================================================
# Phase 2: EKS and TiDB Operator setup
# =============================================================================

# Setup ENV
source ~/cloud-env.sh
source ~/hosts-env.sh

# Configure kubectl for EKS cluster

aws eks update-kubeconfig --region "${REGION_CODE}" --name "${EKS_CLUSTER_NAME}"

# Helm Update
export KUBECONFIG=$HOME/.kube/config
helm repo add pingcap https://charts.pingcap.com/
helm repo update

# Check EKS nodes
kubectl get nodes \
    -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints,AZ:.metadata.labels.az,DEDICATED:.metadata.labels.dedicated

# Create K8S namespace
kubectl create namespace tidb-admin

# Install TiDB Operator - pull image - "pingcap/tidb-operator:v1.6.5"
helm install --namespace tidb-admin tidb-operator pingcap/tidb-operator --version v1.6.5

#helm upgrade --install tidb-operator pingcap/tidb-operator \
#  --namespace tidb-admin \
#  --set operatorImage=pingcap/tidb-operator \
#  --wait

# Verify the TiDB Operator installation
kubectl get pods --namespace tidb-admin -l app.kubernetes.io/instance=tidb-operator

# Check the node where the TiDB Operator is running, shoud on the node labeled with "admin"
kubectl describe pod --namespace tidb-admin \
    $(kubectl get pods --namespace tidb-admin -l app.kubernetes.io/instance=tidb-operator | awk 'NR==2 {print $1}') \
    | grep 'Node:'

# Install CRD
kubectl create -f https://raw.githubusercontent.com/pingcap/tidb-operator/v1.6.5/manifests/crd.yaml

kubectl get crd | grep pingcap.com

# Create tidb-cluster namespace and deploy TidbCluster
kubectl create namespace tidb-cluster

# Use TIDB_VERSION from lab if set, otherwise default
sed "s|<TIDB_VERSION>|${TIDB_VERSION}|" ./template-tidb-cluster.yaml > ./solution-tidb-cluster.yaml
kubectl -n tidb-cluster apply -f ./solution-tidb-cluster.yaml

# Wait for TiDB cluster to be ready
watch -n 1 kubectl get pods --namespace tidb-cluster
kubectl wait --for=condition=Ready tidbcluster/tidb-demo -n tidb-cluster --timeout=900s
