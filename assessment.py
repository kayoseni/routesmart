import boto3
import json


S3_BUCKET = "test_bucket"

#Create an s3 client
s3 = boto3.client('s3')
s3.create_bucket(Bucket=S3_BUCKET)

# Create a bucket policy
bucket_policy = {
    "Version": "2012-10-17",
    "Id": "S3PolicyIPRestrict",
    "Statement": [
        {
            "Sid": "IPAllow",
            "Effect": "Deny",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::bucket/*",
            "Condition" : {
                "IpAddress" : {
                    "aws:SourceIp": "192.168.143.0/24"
                }
            }
        }
    ]
}

# Convert the policy from JSON dict to string
bucket_policy = json.dumps(bucket_policy)

# Set the new policy
s3 = boto3.client('s3')
s3.put_bucket_policy(Bucket=S3_BUCKET, Policy=bucket_policy)

# Set lifecycle policy to delete objects after 14 days
response = s3.put_bucket_lifecycle_configuration(
    Bucket='bucket-sample',
    LifecycleConfiguration={
        'Rules': [
            {
                'Expiration': {
                    'Days': 14,
                },
                'Status': 'Enabled'
            },
        ],
    },
)
