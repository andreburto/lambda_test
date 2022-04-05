#!/usr/bin/env bash

source ./.env

HOME_PATH=$(dirname $0)
OUT_TEMPLATE_FILE="${DIST_NAME}/${DIST_NAME}.yml"

cd $HOME_PATH

pip install -r requirements.txt

mkdir -p $DIST_NAME

juni build

aws cloudformation package  \
--template-file template.yml \
--s3-bucket jarod \
--output-template-file $OUT_TEMPLATE_FILE

aws cloudformation deploy \
--template-file $OUT_TEMPLATE_FILE \
--s3-bucket $S3_BUCKET \
--stack-name $STACK_NAME \
--capabilities CAPABILITY_NAMED_IAM
