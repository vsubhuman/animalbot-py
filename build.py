import os
import sys
import zipfile

import boto3


ZIP = 'build/animalbot-py.zip'
LAMBDA_NAME = 'AnimalBotTest'
S3_KEY = 'AnimalBotTest_py.zip'
S3_BUCKET = 'com.vsubhuman.lambda'

if len(sys.argv) != 2:
    print("One argument <task> is expected!")
    exit(1)

task = sys.argv[1]


def zip_dir(zipfile, dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(root, file)
            arcname = path[len(dir) + 1:]
            zipfile.write(path, arcname)


def create_zip():
    print(":zip")
    with zipfile.ZipFile(ZIP, mode='w') as z:
        zip_dir(z, 'src')
        zip_dir(z, 'virtualenv/lib/python3.6/site-packages')


def upload_zip():
    print(":upload")
    s3 = boto3.client('s3')
    s3.upload_file(ZIP, S3_BUCKET, S3_KEY)


if task == 'zip':
    create_zip()
    exit(0)

if task == 'upload':
    create_zip()
    upload_zip()
    exit(0)

if task == 'deploy':
    create_zip()
    upload_zip()
    print(':deploy')
    lmbda=boto3.client('lambda')
    lmbda.update_function_code(
        FunctionName=LAMBDA_NAME,
        S3Bucket=S3_BUCKET,
        S3Key=S3_KEY
    )
    exit(0)

print("Unknown task: %s" % task)
