#!/usr/local/bin/python
import argparse
import boto3

def init():
  parser = argparse.ArgumentParser(description='Delete all data from Dreamhost dreamobjects bucket.')
  parser.add_argument('profile_name', nargs='?', default='dreamhost', choices=['dreamhost', 'dreamhost-old'], metavar='P', help='The AWS Profile name (eg. dreamhost, dreamhost-old)')

  args = parser.parse_args()
  #  generate url from profile name
  endpoint_url='https://objects-us-east-1.dream.io'
  if args.profile_name is 'dreamhost-old':
    endpoint_url='https://objects-us-west-1.dream.io'

  session = boto3.Session(profile_name=args.profile_name)
  s3 = session.resource('s3', endpoint_url=endpoint_url)

  return s3