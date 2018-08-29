#!/usr/bin/env bash
docker run \
    -e e=pull \
    -it \
    -v /Users/shen/docker/predict_leave/data:/workspace/data \
    --rm \
    --name "predict_leave_everyday" \
    registry.cn-beijing.aliyuncs.com/fittime/predict_leave_everyday


docker run \
    -e e=predict \
    -it \
    -v /Users/shen/docker/predict_leave/data:/workspace/data \
    --rm \
    --name "predict_leave_everyday" \
    registry.cn-beijing.aliyuncs.com/fittime/predict_leave_everyday

