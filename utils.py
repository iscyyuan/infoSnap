from urllib.parse import urlparse
import os

def get_valid_filename(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename.split('?')[0]