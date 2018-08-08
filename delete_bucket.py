#!/usr/local/bin/python
import sys
import drob
from pick import pick

parser = drob.getArgParser('Delete all objects from a bucket and then delete the bucket itself.')
args = drob.getArgs(parser, 'Which Bucket do you want to delete?')

# make sure
sys.stdout.write('Are you sure you want to delete dreamhost bucket "' + args.bucket.upper() + '"? [No]\n')
choice = input('---> ').lower()

#  DELETE
if choice in ['yes', 'y']:
  connection = drob.getS3Resource(args.region)
  connection.Bucket(bucket_name).objects.delete()
  connection.Bucket(bucket_name).delete()
