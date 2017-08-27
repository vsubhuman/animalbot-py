import os
import sys
import zipfile

import boto3

TARGETS = {
    'test': {
        'lambda_name': 'AnimalBotTest'
    },
    'production': {
        'lambda_name': 'AnimalBot'
    }
}

ZIP = 'build/animalbot-py.zip'
S3_BUCKET = 'com.vsubhuman.lambda'
S3_KEY = "%s_py.zip"


def zip_dir(zipfile, dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(root, file)
            arcname = path[len(dir) + 1:]
            zipfile.write(path, arcname)


def create_zip():
    print(":zip")
    dir, _ = os.path.split(ZIP)
    if dir and not os.path.exists(dir):
        os.makedirs(dir)
    with zipfile.ZipFile(ZIP, mode='w') as z:
        zip_dir(z, 'src')
        zip_dir(z, 'virtualenv/lib/python3.6/site-packages')


def upload_zip(lambda_name, s3_key):
    print(":upload")
    s3 = boto3.client('s3')
    s3.upload_file(ZIP, S3_BUCKET, s3_key)


def deploy_zip(lambda_name, s3_key):
    print(':deploy')
    lmbda = boto3.client('lambda')
    lmbda.update_function_code(
        FunctionName=lambda_name,
        S3Bucket=S3_BUCKET,
        S3Key=s3_key
    )


if len(sys.argv) != 2:
    print("One argument <target> is expected!")
    exit(1)

key = sys.argv[1]
target = TARGETS.get(key)
if not target:
    print("No target config found with name: %s!" % key)
    exit(1)

lambda_name = target['lambda_name']
if not lambda_name:
    print("No lambda name is found in the config: %s!" % key)

s3_key = S3_KEY % lambda_name

create_zip()
upload_zip(lambda_name, s3_key)
deploy_zip(lambda_name, s3_key)
