# CloudFormation Lab: REST API on AWS

This repository contains a **CloudFormation lab** for deploying a REST API on AWS, based on the guide ["Build and Deploy REST API on AWS" by Rino-Dev](https://rino-dev.com/build-and-deploy-rest-api-on-aws). The original example was replicated for learning purposes and subsequently enhanced to include improved functionality, better security, and automation practices.

---

## Repository Contents

| File/Script         | Description                                      |
|---------------------|--------------------------------------------------|
| `template.yaml`     | CloudFormation template (Lambda + API Gateway + DynamoDB) |
| `index.py`          | Lambda handler code                              |
| `deploy.sh`         | Packaging and deployment helper script           |
| `test.sh`           | Script to test POST and GET functionalities      |

### To Be Added
- `lab_report.docx` — Assignment report

---

## Deployment Instructions

1. **Create an S3 bucket** for deployment artifacts.
2. **Configure AWS CLI** (use region `eu-west-1`; if you change the region, update `deploy.sh` accordingly):
   ```bash
   aws configure
   ```
3. **Run the deployment script**:
   ```bash
   ./deploy.sh <your_bucket>
   ```

---

## Requirements

- **AWS CLI** (installation instructions for Linux x86_64):
  ```bash
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
  ```
- **Verify installation**:
  ```bash
  aws --version
  ```
- **Clean up** (optional):
  ```bash
  rm awscliv2.zip
  ```

- **boto3** (if you want to test the python script locally):
  ```bash
  pip install boto3
  ```
---

## Additional Resources

The following tutorials were referenced for project improvements:
- [Logging in Python](https://realpython.com/python-logging/)
- [Programming Amazon DynamoDB with Python and Boto3](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/programming-with-python.html)
