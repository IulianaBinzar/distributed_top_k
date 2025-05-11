import logging

import boto3
import io

s3_client = boto3.client('s3')
site_counts = {0: 0, 1: 0, 2: 0}


def process_log_file(bucket_name, file_key):
    global site_counts
    s3_object = s3_client.get_object(Bucket=bucket_name, Key=file_key)

    log_stream = io.StringIO(s3_object['Body'].read().decode('ISO-8859-1'))

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s",
        handlers = [
            logging.FileHandler("../../output/file_validation.log"),
            logging.StreamHandler()
        ]
    )

    logging.info(f"Processing file: {file_key}")

    for line in log_stream:
        site_code = int(line.split()[-1])  # last column is the site code
        if site_code in site_counts:
            site_counts[site_code] += 1

    logging.info(f"Logs received for each site: {site_counts}")

    counts = [site_counts[0], site_counts[1], site_counts[2]]
    max_count = max(counts)
    highest_delta = max_count - site_counts[0]
    delta_percentage = (highest_delta / site_counts[0]) * 100 if site_counts[0] > 0 else 1000
    logging.info(f"Highest delta for this file: {highest_delta} ({delta_percentage:.2f}% of site 0)")

    if delta_percentage >= 1000:
        logging.info(f"File is INVLID\n")
    else:
        logging.info(f"File is VALID\n")



def process_all_files(bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    for item in response.get('Contents', []):
        file_key = item['Key']
        process_log_file(bucket_name, file_key)

if __name__ == "__main__":
    bucket_name = 'fifa-access-logs-25'
    process_all_files(bucket_name)
