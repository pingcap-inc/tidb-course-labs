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
helm repo add eks https://aws.github.io/eks-charts
helm repo add pingcap https://charts.pingcap.com/
helm repo update eks pingcap

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

# Install PingCAP and AWS Load Balancer Controller CRDs
kubectl get crd | grep pingcap.com; kubectl get crd | grep elbv2.k8s.aws

kubectl create -f https://raw.githubusercontent.com/pingcap/tidb-operator/v1.6.5/manifests/crd.yaml
kubectl create -f https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.7.0/v2_7_0_full.yaml

kubectl get crd | grep pingcap.com; kubectl get crd | grep elbv2.k8s.aws

# Create tidb-cluster namespace and deploy TidbCluster
kubectl create namespace tidb-cluster

# Use TIDB_VERSION from lab if set, otherwise default
cp ./template-tidb-cluster.yaml ./solution-tidb-cluster.yaml

sed -i'' -e "s|<TIDB_VERSION>|${TIDB_VERSION}|g" \
         ./solution-tidb-cluster.yaml

cp ./template-targetgroupbinding.yaml ./solution-targetgroupbinding.yaml

sed -i'' -e "s|<TG_ARN>|${TG_ARN}|g" \
         ./solution-targetgroupbinding.yaml

kubectl -n tidb-cluster apply -f ./solution-tidb-cluster.yaml

# Wait for TiDB cluster to be ready
watch -n 1 kubectl get pods --namespace tidb-cluster
# kubectl wait --for=condition=Ready tidbcluster/tidb-demo -n tidb-cluster --timeout=900s

# Check the TiDB service
kubectl describe svc tidb-demo-tidb -n tidb-cluster

# Register EKS Nodes to the existing target group

# Get the real IP address of the node(s) labeled with "dedicated=tidb"
NODE_TIDB_IPS=($(kubectl get nodes -l dedicated=tidb -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}'))
for ip in "${NODE_TIDB_IPS[@]}"; do
  echo "Node with dedicated=tidb has IP: $ip"
  echo "Registering node $ip to existing target group $TG_ARN with port 4000"
  aws elbv2 register-targets \
    --target-group-arn ${TG_ARN} \
    --targets "Id=${ip},Port=4000"\
    --region ${REGION_CODE}
done


# ============== EXPERIMENTAL ==============

# Create IAM service account for AWS Load Balancer Controller
# eksctl get iamserviceaccount --cluster=${EKS_CLUSTER_NAME} --namespace=kube-system --region ${REGION_CODE}

eksctl create iamserviceaccount \
    --cluster=${EKS_CLUSTER_NAME} \
    --namespace=kube-system \
    --name=aws-load-balancer-controller \
    --attach-role-arn=${LBC_ROLE_ARN} \
    --override-existing-serviceaccounts \
    --approve \
    --region ${REGION_CODE}

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=${EKS_CLUSTER_NAME} \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --region ${REGION_CODE}

# Register the TiDB service to the existing target group
kubectl -n tidb-cluster apply -f solution-targetgroupbinding.yaml

# Check the target group binding
kubectl get targetgroupbinding -n tidb-cluster

