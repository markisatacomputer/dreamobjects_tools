#!/usr/local/bin/python
import sys
import drob
from pick import pick

parser = drob.getArgParser('Delete all objects from a bucket and then delete the bucket itself.')
args = parser.parse_args()

# get user region choice
connection = drob.getResource(args.region)

# get user bucket choice
if args.bucket is not None:
  bucket_name = args.bucket
else:
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
