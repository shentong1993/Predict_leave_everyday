#!/usr/bin/env bash
docker run \
    -e e=pull \
    -it \
    --rm \
    --name "predict_leave_everyday" \
    registry.cn-beijing.aliyuncs.com/fittime/predict_leave_everyday


docker run \
    -e e=predict \
    -it \
    --rm \
    --name "predict_leave_everyday" \
    registry.cn-beijing.aliyuncs.com/fittime/predict_leave_everyday

