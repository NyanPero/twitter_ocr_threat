import pandas as pd
import click
import time
import datetime
from io import StringIO
from pathlib import Path
import re


def save_datasets(df, output_dir, file_name):
    # jsonl paths and flag path
    out_path = output_dir / file_name
    print (str(out_path))
    df.to_json(str(out_path), orient='records', lines=True)

def check_urls(text_list, tld_list):
    results = []
    
    url_pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    for text in text_list:
        
        text_pattern = []
        
        # raw pattern
        raw_text = text.replace('[new_line]','\n')
        text_pattern.append(raw_text)

        # delete space pattern
        delete_space = raw_text.replace(' ','')
        text_pattern.append(delete_space)

        # delete space and new line pattern
        delete_space_newline = delete_space.replace('\n','')
        text_pattern.append(delete_space_newline)

        # delete not ascii
        delete_not_ascii = ''.join(c if c.isascii() else ' ' for c in delete_space_newline)
        text_pattern.append(delete_not_ascii)
        for target_text in text_pattern:
            matched_results = url_pattern.search(target_text)
            if matched_results:
                results.append(matched_results.group())
    uniq_url_list = (list(set(results)))
    delete_not_tld = []
    for uniq_url in uniq_url_list:
        tld = uniq_url.split("/")[2].split(".")[-1].lower()
        if tld in tld_list:
            delete_not_tld.append(uniq_url)

    return delete_not_tld

def get_tld_list(tld_file_path):
    tld_list = []
    with open(tld_file_path, 'r') as f:
        for index, line in enumerate(f):
            if index <= 0:
                continue
            tld_list.append(line.strip().lower())
    return tld_list


@click.command()
@click.option('--input-file')
@click.option('--output-dir')
@click.option('--tld-file')
def collect_threats(input_file, output_dir, tld_file):
    url_list = []
    tld_list = get_tld_list(tld_file)
    df = pd.read_json(StringIO(Path(input_file).read_text()), orient='records', lines=True)
    for index, row in df.iterrows():
        url_results = check_urls(row['ocr_text'], tld_list)
        url_list.append(url_results)
    url_series = pd.Series(url_list, index=df.index, name='extracted_url')
    new_df = pd.concat([df,url_series], axis=1)
    new_df_dropped = new_df[new_df.astype(str)['extracted_url'] != '[]']
    file_name = input_file.replace('.jsonl','_threat.jsonl')
    save_datasets(new_df_dropped, Path(output_dir), file_name)


if __name__ == '__main__':
    collect_threats()