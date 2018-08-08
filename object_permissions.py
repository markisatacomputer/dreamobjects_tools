#!/usr/local/bin/python
import sys
import drob

parser = drob.getArgParser('Update all the object ACL policies in a bucket.')
parser.add_argument('--ACL', default='public-read', choices=['private', 'public-read', 'public-read-write', 'authenticated-read', 'aws-exec-read', 'bucket-owner-read', 'bucket-owner-full-control'], help='The ACL policy to apply to all the objects in the bucket. (default: public-read)  Read more at ')
args = drob.getArgs(parser, 'Which bucket would you like to update?')

# get bucket
S3 = drob.getS3Resource()
bucket = S3.Bucket(args.bucket)

# make sure
sys.stdout.write('Are you sure you want to update object ACL to "' + args.ACL + '" in dreamhost bucket "' + args.bucket.upper() + '"? [No]\n')
choice = input('---> ').lower()

# UPDATE
if choice in ['yes', 'y']:
  for obj in bucket.objects.limit(3):
    print('updating ' + obj.key)
    obj.Acl().put(ACL=args.ACL)
