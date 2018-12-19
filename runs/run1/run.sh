#!/usr/bin/env bash

cd /home/petibm-user/data
export CUDA_VISIBLE_DEVICES=0
mpiexec -np 2 petibm-flapping \
	-options_left \
	-log_view ascii:view.log

exit 0
