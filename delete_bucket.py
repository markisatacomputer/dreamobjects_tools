#!/usr/local/bin/python
import sys
from init import init
from pick import pick

connection = init()

# get user bucket choice
options = []
for bucket in connection.buckets.all():
  options.append(bucket.name)
bucket_name, index = pick(options, 'Which Bucket do you want to delete?')

# make sure
sys.stdout.write('Are you sure you want to delete dreamhost bucket "' + bucket_name.upper() + '"? [No]\n')
choice = input('---> ').lower()

#  DELETE
if choice in ['yes', 'y']:
  connection.Bucket(bucket_name).objects.delete()
  connection.Bucket(bucket_name).delete()
