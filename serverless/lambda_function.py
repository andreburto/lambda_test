import os
from datetime import datetime

import boto3


def lambda_handler(event, context):
    print(f"event: {event}")
    print(f"context: {context}")

    cw_client = boto3.client("cloudwatch")
    cw_client.put_metric_data(
        Namespace="test",
        MetricData=[
            {
                'MetricName': 'logcount',
                'Dimensions': [
                    {
                        'Name': 'MyMetrics',
                        'Value': 'Test'
                    },
                ],
                'Timestamp': datetime.now(),
                'Value': float(os.getenv("METRIC_COUNT")),
                'Unit': "Count",
            },
        ]
    )
