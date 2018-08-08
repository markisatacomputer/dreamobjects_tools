#!/usr/local/bin/python
import drob
from pick import pick

parser = drob.getArgParser('Count all objects from a bucket.')
args = parser.parse_args()

# get user region choice
resource = drob.getS3Resource(args.region)

# get user bucket choice
if args.bucket is not None:
  bucket = args.bucket
else:
  options = drob.getBuckets(resource)
  bucket, index_from = pick(options, 'Which Bucket?')

all_objects = drob.getObjectKeys(resource, bucket)

print(region + ' bucket ' + bucket + ': ' + str(len(all_objects)) + ' objects')
