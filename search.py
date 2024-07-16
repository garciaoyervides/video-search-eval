import clip
import torch
import numpy as np
from sklearn.preprocessing import normalize
from databasechroma import query_segments
import cv2
from PIL import Image
import os
from moviepy.editor import VideoFileClip
import data
import math

def h_seconds_to_timestamp(h_seconds):
    #converts hundredth of seconds to timestamp
    hours = h_seconds / 120000
    hours = math.floor(hours)
    min = h_seconds / 6000
    min = math.floor(min)
    sec = int((h_seconds / 100)) % 60
    mili = h_seconds % 100
    time = str(hours).zfill(2)+":"+str(min).zfill(2)+":"+str(sec).zfill(2)+","+str(mili).zfill(2)+"0"
    return time

def extract_features_from_text(search_text):
    text = clip.tokenize(search_text).to(data.device)
    txt_features = []
    with torch.no_grad():
        txt_features = data.model.encode_text(text)
        txt_features = torch.nn.functional.normalize(txt_features,dim=1)
    return txt_features.tolist()

def extract_features_from_image(search_image):
    image = cv2.imread(f'./tmp/{search_image}')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    with torch.no_grad():
        features = data.model.encode_image(data.preprocess(image).unsqueeze(0).to(data.device))
        features = torch.nn.functional.normalize(features,dim=1)
    return features.tolist()

def search_scene(input,k=10,input_type="Text"):
    if input_type == "Text":
        features = extract_features_from_text(input)[0]
    if input_type == "Image":
        features = extract_features_from_image(input)[0]
    results = query_segments(features,k=k)
    return results

def clip_video(video_name, time, file_name):
    start_time = time[0] / 100
    end_time = time[1] / 100
    if not os.path.exists("./tmp"):
        os.makedirs("./tmp")
    if not os.path.exists("./tmp/clips"):
        os.makedirs("./tmp/clips")
    video = VideoFileClip("./videos/" + video_name).resize(width=360)
    clip = video.subclip(start_time, end_time)
    clip.write_videofile(f"./tmp/clips/{file_name}.mp4")
    return f"./tmp/clips/{file_name}.mp4"