import boto3
import logging
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)

# Note:
# Boto3 looks at various configuration locations until it finds configuration values.
# Boto3 adheres to the following lookup order when searching through sources for configuration values:
# - A Config object that's created and passed as the config parameter when creating a client
# - Environment variables
# - The ~/.aws/config file


def upload_file_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        # TODO this follows a different pattern then above get_secrets()
        # In that function we raise the exception again and here we just return it.
        # Might want to update this so we follow the same pattern.
        return e
    except Exception as e:
        return e

    return None