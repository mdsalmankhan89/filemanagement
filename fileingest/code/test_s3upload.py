import boto3
import boto.s3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIAJ2YIY2GG64RZMZOA' 
SECRET_KEY = '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'
local_file = "C:\\Users\\salman\\Desktop\\DjangoLearning\\projects\\DataIngestion\\filemanagement\\fileingest\\code\\Media\\QuarterlyFinance_Q12020.xlsx"
bucket_name = 'myawsgluesrcbucket'
s3_file_name = 'QuarterlyFinance_Q12020.xlsx'

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


uploaded = upload_to_aws(local_file, bucket_name, s3_file_name)