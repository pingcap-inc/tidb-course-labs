#!/bin/bash

source ./hosts-env.sh

# For cluster
export MYSQL_PS1="tidb:tiproxy> "
mysql -h ${HOST_MONITOR1_PRIVATE_IP} -P 6000 -u root
