#!/bin/bash
# Prerequisites and preparation before deploying TidbCluster and TargetGroupBinding
# (reuse existing NLB). Run this on the machine that has kubectl access to the EKS cluster.
set -e

echo ""
echo "=== Pre-flight done. Next steps (run manually) ==="
echo "1. Apply TidbCluster in namespace tidb-cluster:"
echo "   kubectl -n tidb-cluster apply -f solution-tidb-cluster.yaml"
echo "2. After the TiDB service tidb-demo-tidb exists, apply TargetGroupBinding:"
echo "   kubectl apply -f solution-targetgroupbinding.yaml"
echo "3. Ensure your existing NLB listener forwards to that target group (e.g. TCP 4000)."
echo "   Target group must be instance type and port 30400 (TiDB NodePort)."
