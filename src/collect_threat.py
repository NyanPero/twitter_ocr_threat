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

def check_phonenumber(text_list):
    results = []
    
    phone_pattern1 = re.compile("0\d{9,10}")
    phone_pattern2 = re.compile("0\d{2,3}-\d{1,4}-\d{4}")
    phone_pattern3 = re.compile("\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$")
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
            #phone_pattern1
            matched_results = phone_pattern1.search(target_text)
            if matched_results:
                results.append(matched_results.group())
            #phone_pattern2
            matched_results = phone_pattern2.search(target_text)
            if matched_results:
                results.append(matched_results.group())
            #phone_pattern3
            matched_results = phone_pattern3.search(target_text)
            if matched_results:
                results.append(matched_results.group())

    uniq_phone_list = (list(set(results)))

    return uniq_phone_list  

def check_emailaddress(text_list, tld_list):
    results = []
    
    email_pattern = re.compile("[-_a-zA-Z0-9\.+]+@[-a-zA-Z0-9\.]+")
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
            matched_results = email_pattern.search(target_text)
            if matched_results:
                results.append(matched_results.group())
    email_list = []
    for result in results:
        tld = result.split(".")[-1].lower()
        if tld in tld_list:
            email_list.append(result)
    
    uniq_email_list = (list(set(email_list)))

    return uniq_email_list  

def check_emailaddress(text_list, tld_list):
    results = []
    
    email_pattern = re.compile("[-_a-zA-Z0-9\.+]+@[-a-zA-Z0-9\.]+")
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
            matched_results = email_pattern.search(target_text)
            if matched_results:
                results.append(matched_results.group())
    email_list = []
    for result in results:
        tld = result.split(".")[-1].lower()
        if tld in tld_list:
            email_list.append(result)
    
    uniq_email_list = (list(set(email_list)))

    return uniq_email_list  

def check_domains(text_list, url_results, tld_list):
    results = []
    
    domain_pattern = re.compile('((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}')
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
            matched_results = domain_pattern.search(target_text)
            if matched_results:
                results.append(matched_results.group())
    domain_list = []
    for result in results:
        tld = result.split(".")[-1].lower()
        if tld in tld_list:
            domain_list.append(result)
    
    uniq_domain_list = (list(set(domain_list)))
    for uniq_d in uniq_domain_list:
        url = 'http://'+uniq_d
        url_results.append(url)
    uniq_url_results = list(set(url_results))
    return uniq_domain_list, uniq_url_results    

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
    url_list = []
    for result in results:
        tld = result.split("/")[2].split(".")[-1].lower()
        if tld in tld_list:
            url_list.append(result)
            top_url = '.'.join(result.split(".")[0:3])
            url_list.append(top_url)
    
    uniq_url_list = (list(set(url_list)))

    return uniq_url_list

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
    domain_list = []
    email_list = []
    phone_list = []
    tld_list = get_tld_list(tld_file)
    df = pd.read_json(StringIO(Path(input_file).read_text()), orient='records', lines=True)
    for index, row in df.iterrows():
        #check urls
        url_results = check_urls(row['ocr_text'], tld_list)
        #check domains
        domain_results, url_results_add = check_domains(row['ocr_text'], url_results, tld_list)
        domain_list.append(domain_results)
        url_list.append(url_results_add)
        #check emails
        email_results = check_emailaddress(row['ocr_text'], tld_list)
        email_list.append(email_results)
        #check phones
        phone_results = check_phonenumber(row['ocr_text'])
        phone_list.append(phone_results)
    
    url_series = pd.Series(url_list, index=df.index, name='extracted_url')
    domain_series = pd.Series(domain_list, index=df.index, name='extracted_domain')
    email_series = pd.Series(email_list, index=df.index, name='extracted_email')
    phone_series = pd.Series(phone_list, index=df.index, name='extracted_phone')

    new_df = pd.concat([df,url_series,domain_series,email_series,phone_series], axis=1)
    new_df_dropped = new_df[new_df.astype(str)['extracted_url'] != '[]' & new_df.astype(str)['extracted_domain'] != '[]' & new_df.astype(str)['extracted_email'] != '[]' & new_df.astype(str)['extracted_phone'] != '[]']
    file_name = input_file.replace('.jsonl','_threat.jsonl')
    save_datasets(new_df_dropped, Path(output_dir), file_name)


if __name__ == '__main__':
    collect_threats()