#!/usr/local/bin/python
import argparse
import boto3
from pick import pick

def getArgParser(description):
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('--bucket', metavar='bucket', help='The bucket name.')
  parser.add_argument('--region', default='us-east-1', choices=['us-west-1', 'us-east-1'], metavar='region', help='The DreamObjects region. (default: us-east-1)')
  parser.add_argument('--profile', nargs='?', default='default', metavar='Profile', help='The AWS Profile name.  This determines what credentials are pulled from ~/.aws/credentials. (default: "default") See https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration.')
  return parser
def getArgs(parser, question='Which Bucket?'):
  # get args
  args = parser.parse_args()
  # get S3 resource
  connection = getS3Resource(args.region)
  # get user bucket choice
  if args.bucket is None:
    options = []
    for bucket in connection.buckets.all():
      options.append(bucket.name)
    args.bucket, index = pick(options, question)
  return args

def getBuckets(resource):
  buckets = []
  for bucket in resource.buckets.all():
    buckets.append(bucket.name)
  return buckets
def getS3Resource(region='us-east-1', profile_name='default'):
  endpoint_url = 'https://objects-'+region+'.dream.io'
  session = boto3.Session(profile_name=profile_name)
  return session.resource('s3', endpoint_url=endpoint_url)
def getS3Client(region='us-east-1', profile_name='default'):
  endpoint_url = 'https://objects-'+region+'.dream.io'
  session = boto3.Session(profile_name=profile_name)
  return session.client('s3', endpoint_url=endpoint_url)

def key(obj):
  return obj.key
def getObjectKeys(resource, bucket, limit=0):
  source = resource.Bucket(bucket)
  if limit == 0:
    return [key(i) for i in source.objects.all()]
  else:
    return [key(i) for i in source.objects.limit(limit)]
