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

def create_dataframe(jsonl_files):

    df_list = []
    
    for jsonl_file in jsonl_files:
        df = pd.read_json(StringIO(jsonl_file.read_text()), orient='records', lines=True)
        df_list.append(df)
    
    return pd.concat(df_list, axis=0)

def clean_dataframe(df, keyword_list):
    df_list = []
    df_images = df[df['media'].str.len() > 0]

    for keyword in keyword_list:
        df_list.append(df_images[df_images['content'].str.contains(keyword, case=False)])
    concatenated_df = pd.concat(df_list, axis=0)
    return (concatenated_df.drop_duplicates(subset="url"))


@click.command()
@click.option('--since-time')
@click.option('--until-time')
@click.option('--target-dir')
@click.option('--output-dir')
@click.option('--keyword')
def clean_datasets(since_time, until_time, target_dir, output_dir, keyword):
    # extract jsonl files
    file_names = Path(target_dir).glob('*.jsonl')
    check_jsonl_list = extract_jsonl_list(since_time, until_time, file_names)
    
    # create dataframe
    df = create_dataframe(check_jsonl_list)
    df = df.head(10)
    
    # exclude not target tweet
    target_df = clean_dataframe(df,keyword.split("-"))

    file_name = since_time+"_"+until_time+"_"+keyword+'.jsonl'
    print (file_name)
    save_datasets(target_df, Path(output_dir), file_name)

if __name__ == '__main__':
    clean_datasets()
    