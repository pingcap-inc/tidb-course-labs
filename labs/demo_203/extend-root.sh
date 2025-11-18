#!/bin/bash
SIZE=${1}
PART=${2}

vgextend rocky ${PART}
lvextend -L ${SIZE}G /dev/rocky/root
xfs_growfs /
