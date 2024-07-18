#!/bin/bash
SIZE=${1}

vgextend rocky /dev/xvda6
lvextend -L ${SIZE}G /dev/rocky/root
xfs_growfs /
