# CloudFormation_Lab_Rossolini
Cloud Formation example in AWS


This lab is initially based on the guide “Build and Deploy REST API on AWS” by Rino-Dev (https://rino-dev.com/build-and-deploy-rest-api-on-aws). The original example was replicated for learning purposes and subsequently enhanced to include improved functionality, better security, and automation practices.


## Requirements
aws cli 
`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && sudo ./aws/install`
verify installation with 
`aws --version`
Eventually
`rm awscliv2.zip`


## How to run 
```bash
aws cloudformation deploy \
  --template template.yml \
  --stack-name restapi-cloudformation --capabilities CAPABILITY_IAM
```
