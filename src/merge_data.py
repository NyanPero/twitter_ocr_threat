import pandas as pd
import click
import time
import datetime
from io import StringIO
from pathlib import Path

def save_datasets(df, output_dir, file_name):
    # jsonl paths and flag path
    out_path = output_dir / file_name
    print (str(out_path))
    df.to_json(str(out_path), orient='records', lines=True)

def merge_dataframe(jsonl_files):
    df_list = []
    
    for jsonl_file in jsonl_files:
        df = pd.read_json(StringIO(jsonl_file.read_text()), orient='records', lines=True)
        df_list.append(df)
    concatenated_df = pd.concat(df_list, axis=0)
    return concatenated_df.drop_duplicates(subset="url")

@click.command()
@click.option('--input-time')
@click.option('--output-dir')
def merge_datasets(input_time, output_dir):
    # extract jsonl files
    input_time_str = "_".join(input_time.split("/")[-1].split("_")[0:2])
    check_jsonl_list = Path(output_dir).glob('{}*.jsonl'.format(input_time_str))
    
    # merge dataframe
    df = merge_dataframe(check_jsonl_list)

    file_name = input_time_str+"_"+'merged.jsonl'
    save_datasets(df, Path(output_dir), file_name)

if __name__ == '__main__':
    merge_datasets()