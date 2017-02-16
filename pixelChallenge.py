import boto3
import os
import sys

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')

#boto3 v1.4.1 fails to create EC2 resource by default -- workaround as follows
ec2 = boto3.resource('ec2', region_name='us-east-1', api_version='2016-04-01')
ec2_client = boto3.client('ec2')

iam = boto3.resource('iam')
iam_client = boto3.client('iam')

#Create an S3 bucket (if not already created)
def createBucket(bucketName):
    response = s3_client.create_bucket(
        ACL='private',
        Bucket=bucketName
    )

    print('Using S3 Bucket: ' + bucketName)


#Upload files to S3 bucket via list of filenames
def uploadFiles(files, bucketName):
    for file in files:
    	s3.meta.client.upload_file(file, bucketName, file)

    print('Source code uploaded to S3.')


#Attempt to create new S3 Admin role then attaches AmazonS3FullAccess policy
def createS3AccessRole(name):
    trustPolicyDoc = '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Principal": {"Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}]}'
    
    try: 
        response = iam_client.create_role(
            RoleName=name,
            AssumeRolePolicyDocument=trustPolicyDoc
        )

        response = iam_client.create_instance_profile(
            InstanceProfileName=name
        )

        response = iam_client.add_role_to_instance_profile(
            InstanceProfileName=name,
            RoleName=name
        )
        
        print ("IAM Role and Instance Profile created.")
    except:
        print("IAM Role with same name already exists.")

    role = iam.Role(name)
    
    response = role.attach_policy(
        PolicyArn = 'arn:aws:iam::aws:policy/AmazonS3FullAccess'
    )

    print("S3 Admin Policy attached to role.")


#Creates Security Group w/ access to port 8080
def createSecurityGroup():
    try:
        response = ec2.create_security_group(
            GroupName='WebDMZ',
            Description='Opens TCP Port 8080'
        )

        response.authorize_ingress(
            IpProtocol='tcp',
            CidrIp='0.0.0.0/0',
            FromPort=8080,
            ToPort=8080
        )

        print ('Security Group "WebDMZ" created.')
    except:
        print ('Security Group with name "WebDMZ" already created.')


#Retrieves user data startup script from .txt file
def getUserData(scriptName):
    with open(scriptName, 'r') as myfile:
        script=myfile.read()    

    return script


#Create a new EC2 Instance with given name and IAM role 
def createEC2Instance(instanceProfileName):

    response = iam_client.get_instance_profile(
        InstanceProfileName=instanceProfileName
    )

    instance = ec2.create_instances(
        ImageId='ami-b73b63a0',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        IamInstanceProfile={
            'Arn' : response['InstanceProfile']['Arn']
        },
        UserData=getUserData('userdata-script.txt'),
        SecurityGroups=['WebDMZ']
    )

    print('EC2 Instance launched. Return response below:')
    print(instance)

    for i in instance:
        i.create_tags(
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'cbanisi-pixel'
                }
            ]
        )

    print()
    print('An EC2 Instance has been created and tagged as "cbanisi-pixel".')

