#!/bin/bash
# Install kubectl, Helm, and AWS CLI for TiDB Operator on EKS - run during EC2 User Data (Ubuntu)
set -e
LAB_USER="ubuntu"
LAB_HOME="/home/ubuntu"

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
mv kubectl /usr/local/bin/

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# AWS CLI v2 (if not present)
if ! command -v aws &> /dev/null; then
  apt-get install -y unzip 2>/dev/null || true
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip -q awscliv2.zip
  ./aws/install
  rm -rf aws awscliv2.zip
fi

# Create kube directory for lab user
mkdir -p "${LAB_HOME}/.kube"
chown -R "${LAB_USER}:${LAB_USER}" "${LAB_HOME}/.kube"
echo "export KUBECONFIG=${LAB_HOME}/.kube/config" >> "${LAB_HOME}/.bashrc"
chown "${LAB_USER}:${LAB_USER}" "${LAB_HOME}/.bashrc"
