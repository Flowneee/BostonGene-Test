import urllib.request
import shutil
import hashlib

from web.celery import app

CHUNK_SIZE = 4096


@app.task
def download_file_from_url(url, path):
    with urllib.request.urlopen(url) as response, open(path, "wb") as f:
        shutil.copyfileobj(response, f)
        f.close()
    return path


@app.task
def calculate_md5sum(path):
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if chunk == b"":
                break
            hasher.update(chunk)
    return hasher.hexdigest()
