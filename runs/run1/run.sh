#!/usr/bin/env bash

echo $PATH

cd /app
export CUDA_VISIBLE_DEVICES=0
mpiexec --allow-run-as-root -np 2 petibm-flapping \
	-options_left \
	-log_view ascii:view.log

exit 0
