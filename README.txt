README
----------------------
Pixel Server - Code Challenge
by Cyrus Banisi

This code is developed for Python 3.4 and requires a client machine configured with the following:
	1) boto3 Python SDK is installed
	2) The AWS CLI is installed and configured to connect to the us-east-1 region by default

	For guidance regarding the steps above, please refer to the following URL:
	http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation

To execute this code, copy all of the files in this .zip to the client machine and then run LaunchPixelServer.py.



----------------------
Suggested Next Steps:
	*Modify existing crontab and logrotate instead of replacing files
	*Clean up logs on S3 bucket and allow for different bucket names
	*Use AWS Elastic Beanstalk to deploy app + auto-scaling + elastic load balancing

For Even Further Improvements (choose one of the following):
	*Use AWS OpsWorks to manage config setup (i.e. Flask installation)
	*Use AWS CloudFormation to create template for entire application
	*Use AWS CodeCommit/CodeBuild/CodeDeploy to automate deployments of new versions