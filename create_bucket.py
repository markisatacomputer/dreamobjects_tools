#!/usr/local/bin/python
import sys
import re
import drob

parser = drob.getArgParser('Create a new bucket and then delete the bucket itself.')
args = parser.parse_args()

# get user region choice
connection = drob.getS3Resource(args.region)

# get user bucket choice
if args.bucket is not None:
  bucket_name = args.bucket
else:
  # make sure
  sys.stdout.write('What do you want to name your new bucket? [a-z_]\n')
  bucket_name = input('---> ').lower()

# test format
pattern = re.compile("^[a-z0-9_\.]+$")
if pattern.match(bucket_name) == None:
  print('Your bucket name doesn\'t match the acceptable pattern.')
  sys.exit(0)

# test if exists
for bucket in connection.buckets.all():
  if bucket.name == bucket_name:
    print('That bucket already exists.')
    sys.exit(0)

#  CREATE
connection.Bucket(bucket_name).create()
