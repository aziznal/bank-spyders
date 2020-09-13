import boto3
from boto3.s3.transfer import S3Transfer
import numpy as np
import pandas as pd
import os
import sys

from datetime import datetime
from time import sleep

from global_init import get_paths
from extract_results import run_script as extract_results


class DataCleaner:

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def _check_duplicates(self, data):

        prev_val = None
        duplicate_counter = 0

        for index, row in data.iterrows():

            # Skip 1st iteration to set prev_val
            if index == 0:
                prev_val = row
                continue

            # Actual Loop
            if prev_val[0] == row[0]:
                duplicate_counter += 1

            prev_val = row

        return duplicate_counter > 0

    def _new_time_val(self, datetime_, flag=False):

        date, hour = datetime_.split('_')

        if not flag:
            hour += ":30"
        else:
            hour += ":00"

        fixed_datetime = "_".join([date, hour])

        return fixed_datetime

    def _fix_duplicates(self, data):
        """
        This method does NOT delete duplicate time values, but instaed
        appends seconds (as :00 or :30) to the end of each entry.

        Note that foreach entry in the column, at most there will be 
        two values that are the same.
        """

        prev_val = None

        for index, row in data.iterrows():

            # Skip 1st iteration to set prev_val
            if index == 0:
                prev_val = row
                new_val = self._new_time_val(row[0], True)
                data.at[index, 'time'] = new_val
                continue

            # Actual Loop
            if prev_val[0] == row[0]:
                new_val = self._new_time_val(row[0])
                data.at[index, 'time'] = new_val

            else:
                new_val = self._new_time_val(row[0], flag=True)
                data.at[index, 'time'] = new_val

            prev_val = row

    def _repair_time_column(self, data):
        """
        Time column has rows that refer to different rates but have the
        same value. This method fixes that by appending a ':00' or ':30' to the
        hour:minute section of the date
        """
        has_duplicates = self._check_duplicates(data)

        if has_duplicates:
            self._fix_duplicates(data)

        else:
            return

    def _create_date_column(self, data):
        date_column = []

        for val in data['time']:
            date_val = val.split('_')[0]
            date_column.append(date_val)

        data['date'] = np.array(date_column)

    def _create_hour_column(self, data):
        hourminute_column = []

        for val in data['time']:
            hourminute_val = val.split('_')[1]
            hourminute_column.append(hourminute_val)

        data['hour_minute'] = np.array(hourminute_column)

    def _remove_data_spikes(self, data):
        print("Getting all data spikes: ")

        data_spikes = data[data['buying'] / data['selling'] > 1.015]

        before = len(data)

        cond = data['buying'].isin(data_spikes['buying'])
        data.drop(data[cond].index, inplace = True)

        after = len(data)

        print(f"Removed {before - after} spikes in data")

    def clean(self):
        """
        This method does the following:

        :fixes duplicates in time column

        :creates date column

        :creates hour column

        :removes dataspikes
        """

        self._repair_time_column(self.data)

        self._create_date_column(self.data)

        self._create_hour_column(self.data)

        self._remove_data_spikes(self.data)

    def save(self, path):
        try:
            self.data.to_csv(path)

        except FileNotFoundError:

            dirname = path.split('/')[0]
            os.mkdir(dirname)

            self.data.to_csv(path)


def get_keys(filename='rootkey.csv'):

    if not os.path.isfile('rootkey.csv'):
        raise FileNotFoundError("Did you forget to include your AWS Access Key? (rootkey.csv)")

    with open(filename, 'r') as file:
        lines = file.readlines()
    
    access_id = lines[0].split('=')[-1].strip('\n').strip()
    access_secret = lines[1].split('=')[-1].strip('\n').strip()

    return access_id, access_secret


ACCESS_KEY, SECRET_KEY = get_keys()


def get_client():

    client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)    
    return client


def download_file(bucket_name, s3_filename, save_as=None):
    if save_as is None:
        save_as = s3_filename.split('/')[-1]

    s3 = get_client()
    s3.download_file(bucket_name, s3_filename, save_as)


def upload_file(local_filename, inbucket_filename, bucket_name, path_in_bucket=''):

    client = get_client()

    transfer = S3Transfer(client)

    transfer.upload_file(local_filename, bucket_name,
                         path_in_bucket + inbucket_filename)


def upload_multiple_files(client, local_filename, inbucket_filename, bucket_name, path_in_bucket=''):
    transfer = S3Transfer(client)

    transfer.upload_file(local_filename, bucket_name,
                         path_in_bucket + inbucket_filename)


def load_results(path):
    data = pd.read_csv(path)

    return data


def clean_results(data):
    cleaner = DataCleaner(data)
    cleaner.clean()

    return cleaner.data


def save_data(data, path):

    try:
        data.to_csv(path, index=False)

    except FileNotFoundError:
        os.mkdir(path.split('/')[0])
        data.to_csv(path, index=False)


def load_and_clean_data():

    # Get latest results to "results/" folder
    extract_results()
    
    # Load, clean, then save for each result in results folder
    for path, clean_path in zip(paths, clean_paths):

        data = load_results(path)
        data = clean_results(data)
        save_data(data, clean_path)


def sameline_print(output):
    sys.stdout.write('\r' + output)


def send_to_bucket():
    
    bucket_name = 'spider-results-bucket'
    client = get_client()
    
    inbucket_filenames = [
        "isbank-spyder",
        "kuveyt-spyder",
        "vakif-spyder",
        "yapikredi-spyder",
        "ziraat-spyder"
    ]

    for path, filename in zip(clean_paths, inbucket_filenames):
        print("Uploading " + filename)

        upload_multiple_files(
            client=client,
            local_filename=path,
            inbucket_filename=filename + ".csv",
            bucket_name=bucket_name,
            path_in_bucket="clean_data/"
        )


if __name__ == "__main__":

    paths = ["results/" + path + "_results.csv" for path in get_paths()]

    clean_paths = ["clean_results/" + path + ".csv" for path in get_paths()]
    

    # New data will be uploaded every 5 minutes

    wait_time = 10     # 10 minutes

    print(f"Data will uploaded to S3 every {wait_time / 60} minutes")
    while True:
        
        load_and_clean_data()
        send_to_bucket()

        timer = wait_time

        while timer > 0:
            sleep(1)
            timer -= 1
            sameline_print(f"Next upload is in {timer} seconds")

        print("\n")
