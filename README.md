# API: A FastAPI CRUD todo App on AWS lambda
How to run: 
1. cd into the api folder
2. run the ./package_for_lambda.sh command this packages all the requirements up in a .zip file for Lambda
3. cd into the crud-infra folder and run: cdk deploy

You may need to use NPM install to install packages or run cdk bootstrap in order to get the environment set up. The installation also assumes you already are logged into the AWS CLI. In case you cannot redeploy check for S3 buckets with config files stored. 

## API Folder

The `/api` folder contains the Python FastAPI code. Run this shell script to build the code into
a zip (required for CDK to upload to Lambda):

```bash
# Only work on UNIX (Mac/Linux) systems!
./package_for_lambda.sh
```

This should generate a `lambda_function.zip`.

## Infrastructure Folder

The `/crud-infra` folder contains the CDK code to deploy all the infrastructure 
(Lambda function and DynamoDB table) to your AWS account.

You must have [AWS CLI](https://aws.amazon.com/cli/) configured, and 
[AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) installed on your machine.

First, install the node modules.

```bash
npm install
```

Then run bootstrap if you never used CDK with your account before.

```bash
cdk bootstrap
```

Now you can use this to deploy.

```bash
cdk deploy
```

## Test Folder

This contains the Pytest integration tests you can use to test your endpoint directly. Don't 
forget to change your `ENDPOINT` to the one you want to use (in `api_integration_test.py`).

You can run the test like this (but you have to have `pytest` installed):

```bash
pytest
```


