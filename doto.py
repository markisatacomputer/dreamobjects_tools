#!/usr/local/bin/python
import argparse
import boto3

def getArgs(description):
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('profile_name', nargs='?', default='dreamhost', choices=['dreamhost', 'dreamhost-old'], metavar='P', help='The AWS Profile name (eg. dreamhost, dreamhost-old)')
  args = parser.parse_args()
  return args

def getBuckets(resource):
  buckets = []
  for bucket in resource.buckets.all():
    buckets.append(bucket.name)
  return buckets
def getResource(profile_name='objects-us-east-1'):
  endpoint_url = 'https://'+profile_name+'.dream.io'
  session = boto3.Session(profile_name=profile_name)
  return session.resource('s3', endpoint_url=endpoint_url)
def getClient(profile_name='objects-us-east-1'):
  endpoint_url = 'https://'+profile_name+'.dream.io'
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
