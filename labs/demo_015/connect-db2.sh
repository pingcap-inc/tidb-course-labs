#!/bin/bash

source ./hosts-env.sh

# For cluster
export MYSQL_PS1="tidb:db2> "
mysql -h ${HOST_R1DB1_PUBLIC_IP} -P 4000 -u root
