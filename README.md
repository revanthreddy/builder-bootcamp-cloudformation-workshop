# CloudFormation Workshop

This project contains source code and supporting files to do a workshop on Codepipeline.
The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Step.1 `CLONE THIS REPO`


## Step.2 Prerequisites 

* AWS CLI (with default profile has Admin access to the AWS account)
* IDE (Like Pycharm, VS Code or which ever floats your boat)
* Create an S3 bucket that we will use as part CloudFormation package and deploy commands and remember the name
```bash
$ aws s3 mb s3://{YOUR_TEMP_BUCKET_NAME}
```


## Step.3 Package and Deploy with the existing template.yaml

* In the current project root run the below commands

```bash
$ aws cloudformation package --template-file template.yaml --output-template-file template-output.yaml --s3-bucket {YOUR_TEMP_BUCKET_NAME}
$ aws cloudformation deploy --template-file template-output.yaml --stack-name cfn-workshop-stack --parameter-overrides S3BucketPrefix=workshop-bucket --capabilities CAPABILITY_NAMED_IAM
```

## Step.4 Create Lambda function and its role

Append the below CloudFormation code to template.yaml to create a lambda function and an IAM role for it 
```bash
  RandomBucketNameGeneratorLambda:
    Type: "AWS::Lambda::Function"
    Properties:
      Code: lambda_source/
      FunctionName: 'lambda-to-generate-bucket-name'
      Description: 'Lambda to generate a random bucket name'
      Handler: index.handler
      Role: !GetAtt RandomBucketNameGeneratorLambdaRole.Arn
      Runtime: python3.7
      Timeout: 180

  RandomBucketNameGeneratorLambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: 'lambda.amazonaws.com'
            Action:
              - 'sts:AssumeRole'
      Policies:
        - PolicyName: 'RandomBucketNameGeneratorLambdaLogPolicy'
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: 'Allow'
                Action:
                  - 'logs:CreateLogGroup'
                  - 'logs:CreateLogStream'
                  - 'logs:PutLogEvents'
                Resource: 'arn:aws:logs:*:*:*'
```

## Step.5 Package and Deploy
* In the current project root run the below commands

```bash
$ aws cloudformation package --template-file template.yaml --output-template-file template-output.yaml --s3-bucket {YOUR_TEMP_BUCKET_NAME}
$ aws cloudformation deploy --template-file template-output.yaml --stack-name cfn-workshop-stack --parameter-overrides S3BucketPrefix=workshop-bucket --capabilities CAPABILITY_NAMED_IAM
```


## Step.6 Create a custom resource

Append the below CloudFormation code to template.yaml to create a custom resouce that is implemented by the Lambda created in Step.4

```bash
  GenerateBucketName:
    Type: Custom::NameGenerator
    Properties:
      ServiceToken: !GetAtt RandomBucketNameGeneratorLambda.Arn
      bucket_prefix: !Ref S3BucketPrefix
```

### Your final code in template.yaml should look like this

```yaml
AWSTemplateFormatVersion: "2010-09-09"

Description: "This is template to create S3 bucket with a certain prefix and a name"

Parameters:

  S3BucketPrefix:
    Type: String


Resources:


  RandomBucketNameGeneratorLambda:
    Type: "AWS::Lambda::Function"
    Properties:
      Code: lambda_source/
      FunctionName: 'lambda-to-generate-bucket-name'
      Description: 'Lambda to generate a random bucket name'
      Handler: index.handler
      Role: !GetAtt RandomBucketNameGeneratorLambdaRole.Arn
      Runtime: python3.7
      Timeout: 180

  RandomBucketNameGeneratorLambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: 'lambda.amazonaws.com'
            Action:
              - 'sts:AssumeRole'
      Policies:
        - PolicyName: 'RandomBucketNameGeneratorLambdaLogPolicy'
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: 'Allow'
                Action:
                  - 'logs:CreateLogGroup'
                  - 'logs:CreateLogStream'
                  - 'logs:PutLogEvents'
                Resource: 'arn:aws:logs:*:*:*'


  GenerateBucketName:
    Type: Custom::NameGenerato
    Properties:
      ServiceToken: !GetAtt RandomBucketNameGeneratorLambda.Arn
      bucket_prefix: !Ref S3BucketPrefix



  WorkshopS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !GetAtt GenerateBucketName.bucket_name


```

## Step.7 Package and Deploy
* In the current project root run the below commands

```bash
$ aws cloudformation package --template-file template.yaml --output-template-file template-output.yaml --s3-bucket {YOUR_TEMP_BUCKET_NAME}
$ aws cloudformation deploy --template-file template-output.yaml --stack-name cfn-workshop-stack --parameter-overrides S3BucketPrefix=workshop-bucket --capabilities CAPABILITY_NAMED_IAM
```


## Step.8 CLEANUP

* Delete the `cfn-workshop-stack` first from the cloudformation console

## Resources

[AWS CloudFormation getting started](https://aws.amazon.com/cloudformation/getting-started/)