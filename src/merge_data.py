import pandas as pd
import click
import time
import datetime
from io import StringIO
from pathlib import Path

def save_datasets(df, output_dir, file_name):
    # jsonl paths and flag path
    out_path = output_dir / file_name
    df.to_json(str(out_path), orient='records', lines=True)

def merge_dataframe(jsonl_files):
    df_list = []
    
    for jsonl_file in jsonl_files:
        df = pd.read_json(StringIO(jsonl_file.read_text()), orient='records', lines=True)
        df_list.append(df)
    concatenated_df = pd.concat(df_list, axis=0)
    return concatenated_df.drop_duplicates(subset="url")

def extract_jsonl_list(since_time, until_time, file_names):
    
    check_jsonl_list = []
    
    for file_name in file_names:
        str_collect_datetime = str(file_name).split("/")[-1].split("_")[0]
        dt_collect_datetime = datetime.datetime.strptime(str_collect_datetime, '%Y-%m-%dT%H:%M:%S')
        dt_since_datetime = datetime.datetime.strptime(since_time, '%Y-%m-%dT%H:%M:%S')
        dt_until_datetime = datetime.datetime.strptime(until_time, '%Y-%m-%dT%H:%M:%S')
        if dt_since_datetime <= dt_collect_datetime <= dt_until_datetime:
            check_jsonl_list.append(file_name)
    
    return check_jsonl_list


@click.command()
@click.option('--since-time')
@click.option('--until-time')
@click.option('--output-dir')
def merge_datasets(since_time, until_time, output_dir):
    # extract jsonl files
    file_names = Path(output_dir).glob('*.jsonl')
    check_jsonl_list = extract_jsonl_list(since_time, until_time, file_names)
    
    # merge dataframe
    df = merge_dataframe(check_jsonl_list)

    file_name = since_time+"_"+until_time+"_"+'merged.jsonl'
    print (file_name)
    save_datasets(df, Path(output_dir), file_name)

if __name__ == '__main__':
    merge_datasets()