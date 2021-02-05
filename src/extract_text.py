import pandas as pd
import numpy as np
import click
import time
import datetime
from io import StringIO
from pathlib import Path
import io
from PIL import Image
import requests
import cv2
import glob
import pyocr
import pyocr.builders

IMG_SIZE = (200, 200)
SIM_THRESHOLD = 140

def save_datasets(df, output_dir, file_name):
    # jsonl paths and flag path
    out_path = output_dir / file_name
    print (str(out_path))
    df.to_json(str(out_path), orient='records', lines=True)

def apply_ocr(target_image_list):
    results_target = []
    tool = pyocr.get_available_tools()[0]
    for target_pil in target_image_list:
        #pil -> opencv
        #target_opencv = np.array(target_pil, dtype=np.uint8)
        ocr_text = tool.image_to_string(
            target_pil,
            lang="jpn+eng",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )
        results_target.append(ocr_text.replace('\n','[new_line]'))
    return results_target

def matching_features(source_list, target_list):
    results_target = []
    for index, target_pil in enumerate(target_list):
        #pil -> opencv
        target_opencv = np.array(target_pil, dtype=np.uint8)
        target_image = cv2.resize(target_opencv, IMG_SIZE)
        #create detector
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        # detector = cv2.ORB_create()
        detector = cv2.AKAZE_create()
        (target_kp, target_des) = detector.detectAndCompute(target_image, None)
        results_score = []
        for source in source_list:
            try:
                source_image = cv2.imread(source, cv2.IMREAD_GRAYSCALE)
                source_image = cv2.resize(source_image, IMG_SIZE)
                (source_kp, source_des) = detector.detectAndCompute(source_image, None)
                matches = bf.match(target_des, source_des)
                dist = [m.distance for m in matches]
                score = sum(dist) / len(dist)
                results_score.append(score)
            except:
                continue
        results_score.sort()
        if not results_score:
            continue
        if results_score[0] <= SIM_THRESHOLD:
            results_target.append(target_pil)
    return results_target

def download_image(dict_list):
    image_list = []
    for media_dict in dict_list:
        try:
            if 'fullUrl' not in media_dict:
                continue 
            image_url = media_dict['fullUrl']
            image = Image.open(io.BytesIO(requests.get(image_url).content))
            image_list.append(image)
        except:
            continue
    return image_list

@click.command()
@click.option('--input-file')
@click.option('--output-dir')
@click.option('--source-dir')
def extract_texts(input_file, output_dir, source_dir):
    df = pd.read_json(StringIO(Path(input_file).read_text()), orient='records', lines=True)
    text_list = []
    for index, row in df.iterrows():
        # get image list
        image_list = download_image(row['media'])
        if not image_list:
            text_list.append([])
            continue

        # compare src image and target image
        target_image_list = matching_features(glob.glob(source_dir+'*'), image_list)
        if not target_image_list:
            text_list.append([])
            continue

        extracted_texts = apply_ocr(target_image_list)
        
        #list
        text_list.append(extracted_texts)
    ocr_series = pd.Series(text_list, index=df.index, name='ocr_text')
    new_df = pd.concat([df,ocr_series], axis=1)
    new_df_dropped = new_df[new_df.astype(str)['ocr_text'] != '[]']
    file_name = input_file.replace('.jsonl','_orc.jsonl')
    save_datasets(new_df_dropped, Path(output_dir), file_name)


if __name__ == '__main__':
    extract_texts()