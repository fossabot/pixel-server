import boto3
import time
import pixelChallenge

bucketName = 'cbanisi-pixel-challenge'
instanceProfileName = 'S3-Admin-Access'
files = ['pixel-server.tar']
scriptName = 'userdata-script.txt'

pixelChallenge.createBucket(bucketName)
time.sleep(2)
pixelChallenge.uploadFiles(files, bucketName)
time.sleep(2)
pixelChallenge.createS3AccessRole(instanceProfileName)
time.sleep(2)
pixelChallenge.createSecurityGroup()
time.sleep(2)
pixelChallenge.createEC2Instance(instanceProfileName)