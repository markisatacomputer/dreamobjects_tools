#!/usr/local/bin/python
import sys
import drob
from pick import pick

parser = drob.getArgParser('Migrate all objects from one bucket to another.')
parser.add_argument('--source-region', choices=['us-west-1', 'us-east-1'], metavar='src', help='The DreamObjects region to copy from.', dest='region_from')
parser.add_argument('--source-bucket', metavar='src-bckt', help='The bucket to copy from.', dest='bucket_from')
args = parser.parse_args()

# get user FROM choices
region_options = ['us-west-1', 'us-east-1']
if args.region_from is not None:
  region_from = args.region_from
else:
  region_from, index_from = pick(region_options, 'Which region are you migrating from?')
resource_from = drob.getResource(region_from)
if args.bucket_from is not None:
  bucket_from = args.bucket_from
else:
  options = drob.getBuckets(resource_from)
  bucket_from, index_from = pick(options, 'Which bucket are you migrating from?')

# get user TO choices
if args.region is not None:
  region_to = args.region
else:
  region_to, index_to = pick(region_options, 'Which region are you migrating to?')
if region_to is region_from:
  resource_to = resource_from
else:
  resource_to = drob.getResource(region_to)
if args.bucket is not None:
  bucket_to = args.bucket
else:
  options = drob.getBuckets(resource_to)
  bucket_to, index_to = pick(options, 'Which bucket are you migrating to?')

# get vars
destination = resource_to.Bucket(bucket_to)
all_source_objects = drob.getObjectKeys(resource_from, bucket_from)
all_dest_objects = drob.getObjectKeys(resource_to, bucket_to)
migrated_objects = []
skipped_objects = []
erred_objects = []
current_object = 1
total_objects = str(len(all_source_objects))

# COPY
for key in all_source_objects:
  if key not in all_dest_objects:
    copy_source = {
      'Bucket': bucket_from,
      'Key': key
    }
    print(' Copying ' + key + '. (' + str(current_object) + ' of ' + total_objects +')', end="\r"),
    try:
      destination.copy(copy_source, key)
      migrated_objects.append(key)
    except:
      erred_objects.append(key)
      pass
  else:
    print(' Skipping ' + key + '. (' + str(current_object) + ' of ' + total_objects +')', end="\r"),
    skipped_objects.append(key)
  current_object = current_object+1

# Give some feedback
print('')
print("Finished migration.")
print("Objects migrated: "+str(len(migrated_objects)))
print("Objects skipped: "+str(len(skipped_objects)))
print("Objects with errors: "+str(len(erred_objects)))
