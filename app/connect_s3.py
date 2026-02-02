import boto3

# 填入剛才 IAM 得到的金鑰
s3 = boto3.client(
    's3',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='ap-east-2'
)

bucket_name = 'linkuankuan-training-project-bucket'
file_path = '/Users/linkuanyu/Downloads/IMG_7855.jpeg' # 你電腦裡的圖片路徑
object_name = 'uploaded_test.jpg' # 傳到 S3 後的名字

try:
    s3.upload_file(file_path, bucket_name, object_name) # 移除 ExtraArgs
    print(f"上傳成功！圖片網址: https://{bucket_name}.s3.ap-east-2.amazonaws.com/{object_name}")
except Exception as e:
    print(f"上傳失敗: {e}")