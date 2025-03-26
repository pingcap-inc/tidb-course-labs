#!/bin/bash
~/.tiup/bin/tiup cluster start tidb-demo
sleep 30;
./check-cluster.sh