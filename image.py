import requests
import shutil
import os
import hashlib
import base64
import streamlit as st
from urllib.parse import urljoin

def download_image(img_url, referer, img_path):
    headers = {'Referer': referer}
    try:
        img_response = requests.get(img_url, headers=headers, stream=True)
        img_response.raise_for_status()
        with open(img_path, 'wb') as out_file:
            shutil.copyfileobj(img_response.raw, out_file)
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"图片加载失败: {e}")
        return False

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def generate_unique_filename(url):
    hash_object = hashlib.sha1(url.encode())
    return hash_object.hexdigest()

def process_images(soup, url, image_dir):
    images = soup.find_all('img')
    os.makedirs(image_dir, exist_ok=True)
    for img in images:
        img_url = img.get('data-src') if 'data-src' in img.attrs else img.get('src')
        if img_url:
            img_url = urljoin(url, img_url)
            img_filename = generate_unique_filename(img_url) + os.path.splitext(img_url)[1]
            img_path = os.path.join(image_dir, img_filename)
            if download_image(img_url, url, img_path):
                bin_str = get_base64_of_bin_file(img_path)
                full_img_url = f"data:image/png;base64,{bin_str}"
                img['src'] = full_img_url
                if 'data-src' in img.attrs:
                    img['data-src'] = full_img_url