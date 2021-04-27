import pandas as pd
import click
import time
import datetime
from io import StringIO
from pathlib import Path
import json

def save_datasets_json(info_list, output_dir, file_name):
    out_path = output_dir / file_name
    print (str(file_name).split("/")[-1])
    result_dict = { "urls": info_list}
    out_file = open(str(out_path),"w")
    json.dump(result_dict, out_file, ensure_ascii=False)
    out_file.close()

@click.command()
@click.option('--input-file')
@click.option('--output-dir')
def create_urls_datasets(input_file, output_dir):
    url_list = []
    info_list = []
    df = pd.read_json(StringIO(Path(input_file).read_text()), orient='records', lines=True)
    
    for index, row in df.iterrows():
        if row['extracted_url'] not in url_list:
            url_list.append(row['extracted_url'])
            info_list.append({"phish_url":row['extracted_url'], "post_id":str(row['id'])})
    file_name = input_file.replace('.jsonl','_urls.json')
    save_datasets_json(info_list, Path(output_dir), file_name)

if __name__ == '__main__':
    create_urls_datasets()
    
