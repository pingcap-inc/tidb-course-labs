# TiDB Operator on AWS EKS Lab Setup

This setup folder contains the boot-time environment for the demo_010o lab (Deploy TiDB on AWS EKS using TiDB Operator).

**Important:** For the lab to work, the contents of this folder must be copied to the `tidb-course-labs` repository at:
`tidb-course-labs/labs/demo_010o/`

The CloudFormation User Data references `tidb-course-labs/labs/demo_010o/` when provisioning the bastion node.

## Contents

- `install-operator-env.sh` - Installs kubectl, Helm, AWS CLI (run during User Data; no k3s - uses EKS)
- `template-tidb-cluster.yaml` - TidbCluster CR: 2 TiDB, 3 PD, 3 TiKV, 1 TiFlash. TiDB service is NodePort for reusing an existing NLB.
- `template-targetgroupbinding.yaml` - Bind the TiDB service to an existing NLB target group (replace `<TG_ARN>` and `<NAMESPACE>`). Apply after the cluster is created. Requires AWS Load Balancer Controller.
- `solution-tidb-cluster.yaml` - TidbCluster CR with LoadBalancer service for EKS (if present)
