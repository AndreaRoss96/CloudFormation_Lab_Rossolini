# CloudFormation_Lab_Rossolini
Cloud Formation example in AWS


This lab is initially based on the guide “Build and Deploy REST API on AWS” by Rino-Dev (https://rino-dev.com/build-and-deploy-rest-api-on-aws). The original example was replicated for learning purposes and subsequently enhanced to include improved functionality, better security, and automation practices.

## What this repo contains
- template.yaml — CloudFormation template (Lambda + API Gateway + DynamoDB)
- index.py - Lambda handler code.
- deploy.sh - packaging & deploy helper.
- test.sh - script to test POST and GET functionalities.

# To be added
- lab_report.docx - Report of this assignment

# How to deploy
1. Create a S3 bucket
2. Set up you `aws configure` (region eu-west-1, if you want to change region, you need to modify the deploy.sh script)
3. Run `./deploy.sh <your_bucket>` (with your parameters)

## Requirements
- aws cli 
`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && sudo ./aws/install`
- verify installation with 
`aws --version`
- Eventually
`rm awscliv2.zip`


## Additional tutorials followed for porject improvement
##### [Logging in Python](https://realpython.com/python-logging/)
##### [Programming Amazon DynamoDB with Python and Boto3](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/programming-with-python.html)