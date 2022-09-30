import smtplib
import os
import logging
import time
import urllib.parse
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from helpers import aws

log = logging.getLogger(__name__)


# Email the test report
# send_from: source email address, for example platformbot@hallmarklabs.com
# email_password: SMTP server password for the send_from email address
# send_to: list of email address to send to
# report_location: file location of html report, for example: report/report.html


def upload_report_s3(report_location, bucket_name, aws_region):
    if not bucket_name:
        log.error("failed uploading report to S3, bucket name is empty")
        return

    # Just in case the report doens't exist yet, wait up to 3 seconds
    counter = 0
    while not os.path.isfile(report_location) and counter < 4:
        if counter == 4:
            log.error("failed uploading report to S3, report doesn't exist: " + report_location)
            return
        log.info("waiting for report to exist...")
        time.sleep(1)
        counter += 1

    # Example directory: core-services/2020-09-22_20:04:36.361027/report.html
    date_now = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S.%f")
    object_name = "core-services/" + date_now + "/report.html"

    # Upload the file
    err = aws.upload_file_s3(report_location, bucket_name, object_name)
    if err:
        log.error("failed uploading file to s3: " + str(err))
        return

    # Build url using f-strings
    encoded_object_name = urllib.parse.quote(object_name)
    file_url = f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{encoded_object_name}"
    log.info("successfully uploaded file to s3 at: " + file_url)

    # This is intended to be used by gitlab to retrieve the
    # S3 object and upload as artifact directly in the job.
    s3_uri = f"s3://{bucket_name}/{object_name}"
    log.info("S3_OBJECT_URI=" + s3_uri)

