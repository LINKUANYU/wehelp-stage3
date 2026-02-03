import boto3
import os
import sys

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = 'linkuankuan-training-project-bucket'
REGION = 'ap-east-2'
MY_DOMAIN = 'cdn.linkuankuan.com'


if not AWS_SECRET_ACCESS_KEY or not AWS_ACCESS_KEY_ID:
    sys.exit("Critical Error: S3 connect fail, missing access keys in environment variables.")

# 填入剛才 IAM 得到的金鑰
s3 = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = REGION
)

def upload_s3(file_obj, object_name):
    try:
        s3.upload_fileobj(file_obj, BUCKET_NAME, object_name)
        img_url = (f"https://{MY_DOMAIN}/{object_name}")
        return img_url
    except Exception as e:
        print(f"上傳失敗: {e}")
        return None