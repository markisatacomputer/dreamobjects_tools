#!/usr/local/bin/python
import sys
import doto
from pick import pick

# get user FROM choices
cluster_options = ['objects-us-west-1', 'objects-us-east-1']
cluster_from, index_from = pick(cluster_options, 'Which Cluster are you migrating from?')
resource_from = doto.getResource(cluster_from)
options = doto.getBuckets(resource_from)
bucket_from, index_from = pick(options, 'Which Bucket are you migrating from?')
# get user TO choices
cluster_to, index_to = pick(cluster_options, 'Which Cluster are you migrating to?')
resource_to = doto.getResource(cluster_to)
options = doto.getBuckets(resource_to)
bucket_to, index_to = pick(options, 'Which Bucket are you migrating to?')

# get vars
destination = resource_to.Bucket(bucket_to)
all_source_objects = doto.getObjectKeys(resource_from, bucket_from)
all_dest_objects = doto.getObjectKeys(resource_to, bucket_to)
migrated_objects = []
skipped_objects = []
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
    destination.copy(copy_source, key)
    migrated_objects.append(key)
  else:
    print(' Skipping ' + key + '. (' + str(current_object) + ' of ' + total_objects +')', end="\r"),
    skipped_objects.append(key)
  current_object = current_object+1

# Give some feedback
print('')
print("Finished migration.")
print("Objects migrated: "+str(len(migrated_objects)))
print("Objects skipped: "+str(len(skipped_objects)))
