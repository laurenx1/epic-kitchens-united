import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
from datetime import datetime
import os
import math
from datetime import timedelta
import tqdm


def time_to_seconds(timestamp):
    """
    Returns a count of total seconds passed between 00:00:00.000 and the timestamp passed in.

    Args: 
        timestamp (datetime.strptime object or str): the timestamp that the count will be performed on 

    Returns:
        total_seconds (float): total seconds (to the millisecond) since 00:00:00.000
    """
    timestamp = str(timestamp)
    pt = datetime.strptime(timestamp, '%H:%M:%S.%f')
    total_seconds = pt.microsecond / 1e6 + pt.second + pt.minute * 60 + pt.hour * 3600
    return total_seconds



def dt_to_seconds(pt):
    """
    Counts the total number of seconds and returns the float.

    Args: 
        pt (datetime object): the timestamp for this count

    Returns:
        total_seconds (float): total seconds (to the millisecond) since 00:00:00.000
    """
    total_seconds = pt.microsecond / 1e6 + pt.second + pt.minute * 60 + pt.hour * 3600
    return total_seconds



def filter_csv_by_vid_id(df, vid_id): 
    
    """
    Filters a DataFrame by video_id, returns a dataframe of the csv with only rows of this video id.

    Args:
        df (DataFrame object): the dataframe to be filtered
        vid_id (str): the video id, ex. "P01_103"

    Returns: 
        (DataFrame): the original df filtered by vid_id
    """
    return df[df['video_id'] == vid_id]



def make_time_csv(df, dt, new_filepath, max_t):
    """
    Creates a csv of timestamp intervals for a specified time delta, filepath, and video, returns
    a DataFrame of this csv. 

    Args:
        df (DataFrame): dataframe of a csv already filtered by video id
        dt (int): time delta for intervals, or windows of time for each row
        new_filepath (str): filepath to where the new csv will be saved
        max_t (datetime object): datetime object that is the max timestamp of the specified video

    Returns:
        df (DataFrame): returns a dataframe of the timestamp oriented csv
    """
    with open(new_filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['start_timestamp_inclusive', 'stop_timestamp_exclusive'])
        dt_ = timedelta(milliseconds=dt)
        curr_time = '00:00:00.000'
        curr_time = datetime.strptime(curr_time, "%H:%M:%S.%f")
        for t in tqdm.tqdm(np.arange(dt_to_seconds(curr_time), dt_to_seconds(max_t), dt/1000), desc=f'{curr_time}/{max_t}'):
            writer.writerow([curr_time.strftime("%H:%M:%S.%f"), (curr_time + dt_).strftime("%H:%M:%S.%f")])
            curr_time += dt_

    df = pd.read_csv(new_filepath)
    df['start_timestamp_inclusive'] = pd.to_datetime(df['start_timestamp_inclusive'], format="%H:%M:%S.%f")
    return df



def check_overlap(start1, stop1, start2, stop2):
    """
    checks any overlaps between 2 sets of boundaries

    Args: 
        start1 (float): minimum bound 1
        stop1 (float): maximum bound 1
        start2 (float): minimum bound 2
        stop2 (float): maximum bound 2
    
    Returns: 
        (bool) : True if overlap is found, False if not
    """
    return (start1 <= start2 <= stop1) or (start2 <= start1 <= stop2)



def add_columns(df, dt, old_df, column_name_list):
    """
        Adds columns from column_name_list from one csv to a timestamp oriented one, placing data at the 
        correct timestamp

        Args:
            df (DataFrame): timestamp oriented dataframe, filtered by video id
            dt (int): time delta (milliseconds)
            old_df (DataFrame): old dataframe (with columns desired)
            column_name_list (lst):

        Returns:
            df (DataFrame): new timestamp oriented dataframe with added columns
    """
    dt_ = timedelta(milliseconds=dt)
    for c in column_name_list:
        df[c] = None

    times = df.start_timestamp_inclusive
    dictionary = {time: {c: [] for c in column_name_list} for time in df.start_timestamp_inclusive}

    for time in tqdm.tqdm(times):
        for index, row in old_df.iterrows():
            if check_overlap(dt_to_seconds(row.start_timestamp), dt_to_seconds(row.stop_timestamp), dt_to_seconds(time), dt_to_seconds(time + dt_)):
                for column_name in column_name_list:
                    dictionary[time][column_name].append(row[column_name])

    for i, row in df.iterrows():
        time_values = dictionary.get(row.start_timestamp_inclusive, {})
        for c in column_name_list:
            df.at[i, c] = time_values.get(c, None)
    return df



def merge_csv(dt, vid_id, new_filepath, ek_old_filepath, es_old_filepath, ek_column_name_list, es_column_name_list):
    """
    Adds columns from multiple csvs into one merged csv organized by timestamp, saves at new_filepath, returns a dataframe of this csv

    Args:
        dt (int): time delta (milliseconds) for new csv row intervals
        vid_i (str): the video id of the video for the desired new csv
        new_filepath (str): filepath to store the new (merged) csv
        ek_old_filepath (str): filepath of the EPIC KITCHENS csv
        es_old_filepath (str): filepath of the EPIC SOUNDS csv
        ek_column_name_list (lst, str): list of columns desired from EPIC KITCHENS
        es_column_name_list (lst, str): list of columns desired from EPIC SOUNDS

    Returns:
        (DataFrame): dataframe of new, merged csv
    """
    ek_df = pd.read_csv(ek_old_filepath)
    ek_filtered_df = ek_df[ek_df['video_id'] == vid_id].copy()
    ek_filtered_df['start_timestamp'] = pd.to_datetime(ek_filtered_df.start_timestamp, format="%H:%M:%S.%f")
    ek_filtered_df['stop_timestamp'] = pd.to_datetime(ek_filtered_df.stop_timestamp, format="%H:%M:%S.%f")

    es_df = pd.read_csv(es_old_filepath)
    es_filtered_df = es_df[es_df['video_id'] == vid_id].copy()
    es_filtered_df['start_timestamp'] = pd.to_datetime(es_filtered_df.start_timestamp)
    es_filtered_df['stop_timestamp'] = pd.to_datetime(es_filtered_df.stop_timestamp)
    
    max_t = max(ek_filtered_df.stop_timestamp.max(), es_filtered_df.stop_timestamp.max())

    df = make_time_csv(ek_filtered_df, dt, new_filepath, max_t) #ek_filtered_df can be replaced with es_filtered_df if so desired


    df = add_columns(df, dt, ek_filtered_df, ek_column_name_list)
    df = add_columns(df, dt, es_filtered_df, es_column_name_list)

    df['start_timestamp_inclusive'] = df.start_timestamp_inclusive.dt.strftime("%H:%M:%S.%f")
    df.to_csv(new_filepath, index=False)

    return df