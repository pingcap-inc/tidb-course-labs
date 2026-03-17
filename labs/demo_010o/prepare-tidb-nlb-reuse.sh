#!/bin/bash
# Prerequisites and preparation before deploying TidbCluster and TargetGroupBinding
# (reuse existing NLB). Run this on the machine that has kubectl access to the EKS cluster.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== TiDB on EKS (reuse existing NLB) - Pre-flight checks ==="

# 1. kubectl and cluster access
if ! command -v kubectl &>/dev/null; then
  echo "ERROR: kubectl not found. Install it (e.g. install-operator-env.sh) and retry."
  exit 1
fi
if ! kubectl cluster-info &>/dev/null; then
  echo "ERROR: Cannot reach cluster. Configure kubeconfig (e.g. aws eks update-kubeconfig --region <REGION> --name <EKS_CLUSTER_NAME>)."
  exit 1
fi
echo "[OK] kubectl and cluster access"

# 2. Source lab env (TIDB_VERSION, TG_ARN) and refresh kubeconfig
if [[ -f ~/cloud-env.sh ]]; then
  source ~/cloud-env.sh
  if [[ -n "${REGION_CODE:-}" && -n "${EKS_CLUSTER_NAME:-}" ]]; then
    aws eks update-kubeconfig --region "${REGION_CODE}" --name "${EKS_CLUSTER_NAME}" 2>/dev/null || true
  fi
fi
if [[ -z "${TIDB_VERSION:-}" ]]; then
  echo "ERROR: TIDB_VERSION is not set. Export it or set it in cloud-env.sh (e.g. 7.5.0)."
  exit 1
fi
if [[ -z "${TG_ARN:-}" ]]; then
  echo "ERROR: TG_ARN is not set. Export it or set it in cloud-env.sh (your existing NLB target group ARN)."
  exit 1
fi
echo "[OK] TIDB_VERSION=${TIDB_VERSION} TG_ARN set"

# 3. Namespace for TidbCluster and TargetGroupBinding
if kubectl get namespace tidb-cluster &>/dev/null; then
  echo "[OK] Namespace tidb-cluster exists"
else
  echo "Creating namespace tidb-cluster..."
  kubectl create namespace tidb-cluster
  echo "[OK] Namespace tidb-cluster created"
fi

# 4. TiDB Operator (TidbCluster CRD)
if kubectl get crd tidbclusters.pingcap.com &>/dev/null; then
  echo "[OK] TidbCluster CRD (TiDB Operator) present"
else
  echo "ERROR: TidbCluster CRD not found. Install TiDB Operator first (e.g. Helm install tidb-operator and apply CRD)."
  exit 1
fi

# 5. AWS Load Balancer Controller (TargetGroupBinding CRD)
if kubectl get crd targetgroupbindings.elbv2.k8s.aws &>/dev/null; then
  echo "[OK] TargetGroupBinding CRD (AWS Load Balancer Controller) present"
else
  echo "ERROR: TargetGroupBinding CRD not found. Install AWS Load Balancer Controller so TargetGroupBinding can be used."
  exit 1
fi

# 6. StorageClass (warning only)
if kubectl get storageclass gp2 &>/dev/null; then
  echo "[OK] StorageClass gp2 exists"
else
  echo "WARN: StorageClass gp2 not found. TidbCluster uses gp2 for PD/TiKV/TiFlash; create it or change template storageClassName."
fi

# 7. Node labels (warning only) – TiDB template expects dedicated=pd/tikv/tidb/tiflash
for role in pd tikv tidb tiflash; do
  count=$(kubectl get nodes -l "dedicated=${role}" --no-headers 2>/dev/null | wc -l)
  if [[ "$count" -eq 0 ]]; then
    echo "WARN: No nodes with label dedicated=${role}; schedule pods there or add the label to nodes."
  else
    echo "[OK] Nodes with dedicated=${role}: $count"
  fi
done

# 8. Generate solution manifests from templates using TIDB_VERSION and TG_ARN
echo ""
echo "Generating solution manifests (TIDB_VERSION=${TIDB_VERSION}, TG_ARN=***)..."
cp -f ./template-tidb-cluster.yaml ./solution-tidb-cluster.yaml
cp -f ./template-targetgroupbinding.yaml ./solution-targetgroupbinding.yaml
sed -i.bak -e "s|v<TIDB_VERSION>|v${TIDB_VERSION}|g" ./solution-tidb-cluster.yaml && rm -f ./solution-tidb-cluster.yaml.bak
sed -i.bak -e "s|\"<TG_ARN>\"|\"${TG_ARN}\"|g" ./solution-targetgroupbinding.yaml && rm -f ./solution-targetgroupbinding.yaml.bak
echo "[OK] solution-tidb-cluster.yaml and solution-targetgroupbinding.yaml created"

echo ""
echo "=== Pre-flight done. Next steps (run manually) ==="
echo "1. Apply TidbCluster in namespace tidb-cluster:"
echo "   kubectl -n tidb-cluster apply -f solution-tidb-cluster.yaml"
echo "2. After the TiDB service tidb-demo-tidb exists, apply TargetGroupBinding:"
echo "   kubectl apply -f solution-targetgroupbinding.yaml"
echo "3. Ensure your existing NLB listener forwards to that target group (e.g. TCP 4000)."
echo "   Target group must be instance type and port 30400 (TiDB NodePort)."
