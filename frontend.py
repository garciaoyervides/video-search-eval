import streamlit as st
import pandas as pd
import requests
import base64
import io
import time
import os

API_ENDPOINT="http://127.0.0.1:5000"

st.set_page_config(
    page_title="Video Semantic Search Application",
    page_icon="🔍",
)


st.title('Semantic Search Application')

##VIDEO SEARCH

st.caption('Searches inside our database and finds the video(s) that are most similar to your search phrase or search image.')
search_type = st.radio("Search Type",('Text', 'Image'),
                        help="Text: Write down one sentence. Image: Upload one image",
                        key="search_type_radio")
if search_type == "Text":
    search_term = st.text_input('Search Phrase', help="Longer phrases offer better results")
if search_type == "Image":
    search_uploaded_file = st.file_uploader("Choose an image file", help="Use a high quality picture", key="Search Upload Image Button", type=['jpg','jpeg','png','bmp'])
    if search_uploaded_file:
        st.image(search_uploaded_file)
search_results = st.slider('Amount of results', 1, 10, 1)
#search_expand_treshold = st.slider('Expand Treshold', 0.0, 1.0, 0.05)
if st.button('Search', key="Search Video Button", disabled=
                ((search_type == "Text" and search_term == "") or
                (search_type == "Image" and search_uploaded_file is None))):
    with st.spinner('Searching...'):
        if search_type == "Text":
            response = requests.post(f"{API_ENDPOINT}/search",
                                    data={
                                        "text": search_term,
                                        "k": search_results,
                                        })
        if search_type == "Image":
            search_bytes_data = search_uploaded_file.getvalue()
            response = requests.post(f"{API_ENDPOINT}/search",
                                    files = {
                                        "file": (search_uploaded_file.name,search_bytes_data)
                                        },
                                    data={
                                        "k": search_results,
                                        })
    if response.status_code == 200:
        with st.spinner('Loading...'):
            data = response.json()
            if not os.path.exists("./tmp"):
                os.makedirs("./tmp")
            for i,d in enumerate(data):
                video_decode = base64.b64decode(d['video']) 
                video_write = open(f'./tmp/segment_{str(i).zfill(3)}.mp4', 'wb')
                video_write.write(video_decode)
                video_file = open(f'./tmp/segment_{str(i).zfill(3)}.mp4', 'rb')
                video_bytes = video_file.read()
                st.divider()
                st.write(f"segment_{str(i).zfill(3)}.mp4 Distance: {d['distance']}")
                if (d['video'] != ""):
                    st.video(video_bytes)
                if 'identifier' in d:
                    st.caption(f"{d['identifier']}")
    else:
        st.error("Error getting data: {}".format(response.status_code))