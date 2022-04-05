#!/usr/bin/env python3
# Standard library...
import os
import json
from datetime import datetime, timedelta
from time import sleep

# Third-party...
import boto3
from pytz import timezone

CLOUDWATCH_EVENT_PAYLOAD = {
    "version": "0",
    "id": "fe8d3c65-xmpl-c5c3-2c87-81584709a377",
    "detail-type": "RDS DB Instance Event",
    "source": "aws.rds",
    "account": "123456789012",
    "time": "2020-04-28T07:20:20Z",
    "region": "us-east-2",
    "resources": [
        "arn:aws:rds:us-east-2:123456789012:db:rdz6xmpliljlb1"
    ],
    "detail": {
        "EventCategories": [
            "backup"
        ],
        "SourceType": "DB_INSTANCE",
        "SourceArn": "arn:aws:rds:us-east-2:123456789012:db:rdz6xmpliljlb1",
        "Date": "2020-04-28T07:20:20.112Z",
        "Message": "Finished DB Instance backup",
        "SourceIdentifier": "rdz6xmpliljlb1"
    }
}
DEFAULT_RESOURCE_NAME = "HelloWorldFunction"


def get_stack_resources(stack_name: str) -> dict:
    """
    Get the resources from the given stack.
    """
    stack_resources = {}
    cfn_client = boto3.client("cloudformation")
    for page in cfn_client.get_paginator('list_stack_resources').paginate(StackName=stack_name):
        for r in page["StackResourceSummaries"]:
            stack_resources[r["LogicalResourceId"]] = r["PhysicalResourceId"]
    return stack_resources


def invoke_lambda(lambda_arn: str, event_payload: dict) -> dict:
    """
    Execute the lambda synchronously.
    """
    lambda_client = boto3.client("lambda")
    lambda_response = lambda_client.invoke(
        FunctionName=lambda_arn, InvocationType='Event', Payload=event_payload)
    return lambda_response


def get_metrics_within_five_minutes():
    """
    Get the most recent metrics output by the Lambda.
    """
    cw_client = boto3.client("cloudwatch")
    cw_response = cw_client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "test_response",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "test",
                        "MetricName": "logcount",
                        "Dimensions": [
                            {
                                "Name": "MyMetrics",
                                "Value": "Test",
                            },
                        ],
                    },
                    "Period": 60,
                    "Stat": "Sum",
                },
                "ReturnData": True,
            },
        ],
        StartTime=(datetime.now(timezone('UTC')) - timedelta(minutes=5)),
        EndTime=(datetime.now(timezone('UTC')) + timedelta(minutes=5))
    )
    return cw_response


def main() -> None:
    stack_name = os.getenv("STACK_NAME")
    resources_by_name = get_stack_resources(stack_name)
    lambda_response = invoke_lambda(
        resources_by_name[DEFAULT_RESOURCE_NAME],
        json.dumps(CLOUDWATCH_EVENT_PAYLOAD, ensure_ascii=False).encode())
    print(lambda_response)
    sleep(10)
    cw_response = get_metrics_within_five_minutes()
    print(cw_response)


if __name__ == "__main__":
    main()
