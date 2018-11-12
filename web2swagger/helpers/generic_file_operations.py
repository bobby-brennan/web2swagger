# -*- coding: utf-8 -*-
import os
import codecs
import hashlib
import logging
import shutil
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

try:
    from urllib import quote
except:
    from urllib.parse import quote
import zipfile
import json

def create_directory_path(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        raise Exception('Error when creating directory: ' + str(e))

def save_file(directory_path, filename, content):
    filename = os.path.join(directory_path, filename)

    logging.info("saving to " + filename)
    with open(filename, 'wb') as f:
        f.write(content)

def save_case_html(response, ident, data_type='start'):
    output_directory = os.path.abspath("test")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    file_data = generate_friendly_file_path(response.url, output_directory)
    storage_path = os.path.join(output_directory, data_type + '_' + file_data['filename'])
    try:
        with codecs.open(storage_path, 'w', "utf-8") as file_:
            file_.write(response.text)
    except:
        with codecs.open(storage_path, 'w', "utf-8") as file_:
            file_.write(response.body)

    return storage_path

def unzip_file(zip_file_path, directory_to_extract_to):
    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()

def get_files_from_path(directory): 
    file_paths = []
 
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append({'full_path': filepath, 'filename': filename})
 
    return file_paths

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def read_json_file(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(str(e))
    return {}

def delete_path(path):
    try:
        shutil.rmtree(path)
    except:
        logging.info("Failed to delete path: " + path)

def generate_friendly_file_path(url, output_directory):
    elements = urlparse(url)
    splitted_filepath = _split_element_path(elements)

    filename = 'index.html'
    if len(splitted_filepath) > 0:
        filename = splitted_filepath.pop()

        # check if we're looking at a directory, not a file here ...
        if "." not in filename[-5:] or elements.path.endswith('/'):
            splitted_filepath.append(filename)
            filename = 'index.html'

    filename = _add_url_element_to_filename(elements, filename)
    filename = _sanitize_filename(url, filename)
    splitted_filepath = [elements.netloc] + [p for p in splitted_filepath if len(p) > 0]

    web_part_of_path = os.path.join('', *splitted_filepath)
    return {'filename': filename,
            'file_directory': os.path.join(output_directory, web_part_of_path),
            'web_part_of_path': web_part_of_path}

def _add_url_element_to_filename(elements, filename):
    if elements.query:
        filename += ('?' + elements.query)

    if elements.fragment:
        filename += ('#' + elements.fragment)
    return filename

def _split_element_path(elements):
    splitted_filepath = elements.path.split('/')
    return [p for p in splitted_filepath if len(p) > 0]

def _sanitize_filename(url, filename):
    sanitized = quote(filename).replace("/", "_")
    if len(sanitized) < 70:
        return sanitized
    else:
        hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        return "%s_%s...%s" % (hash[:10], sanitized[:50], sanitized[-10:])
