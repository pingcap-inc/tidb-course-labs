#!/bin/bash

# Run ./playground-clean-classroom.sh

./playground-clean-classroom.sh

tiup playground v8.5.0 --tag classroom --db 3 --pd 3 --kv 3 --tiflash 1
