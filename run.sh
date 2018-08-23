#!/usr/bin/env bash

echo 'begin run!'
function pull(){
    python pull.py
}
function predict(){
    python get_data_and_predict.py
}
if [ "$e" = "" ];then
    e=$1
fi

if [ "$e" = 'pull' ];then
echo 'pull start'
    pull
echo 'pull end '
fi

if [ "$e" = 'predict' ]; then
echo 'predict begin'
    predict
echo 'predict over'
fi
echo 'end'
