#!/usr/local/bin/python
import doto
from pick import pick

# get user FROM choices
cluster_options = ['objects-us-west-1', 'objects-us-east-1']
cluster, index = pick(cluster_options, 'Which Cluster?')
resource = doto.getResource(cluster)
options = doto.getBuckets(resource)
bucket, index_from = pick(options, 'Which Bucket?')

all_objects = doto.getObjectKeys(resource, bucket)

print(cluster + ' bucket ' + bucket + ': ' + len(all_objects) + ' objects')
