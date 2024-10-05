"""
onc_download.py
"""
import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import json
from contextlib import closing
import errno
from copy import deepcopy


import shutil
import glob
import random
import time




# Function to download a file
def download_file(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(response.content)

# Function to recursively search and download ".mseed" files
def download_mseed_files(url, base_dir, searched=[], filters=None):
    if url in searched:
        return []
    response = requests.get(url)

    # also append the parents of the url
    searched.append('/'.join(url.split('/')[:-2])+'/')    
    searched.append(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in reversed(soup.find_all('a')):
            href = link.get('href')
            if href.endswith('.mseed'):
                # for example href is ./OO-HYEA2--YDH-2018-01-01T00:00:00.000000.mseed
                # and url is https://rawdata-west.oceanobservatories.org/files/CE02SHBP/LJ01D/11-HYDBBA106/2018/01/01/
                # we want to save the file to os.path.join(base_dir, 'CE02SHBP/LJ01D/11-HYDBBA106/2018/01/01/OO-HYEA2--YDH-2018-01-01T00:00:00.000000.mseed')
                absolute_url = urljoin(url, href)
                # all filters must be in the absolute_url
                if filters is not None:
                    if not(all([filt in absolute_url for filt in filters])):
                        continue

                d = requests.get(absolute_url)
                if int(d.headers['Content-Length'])<1000000:
                    continue
                print('absolute_url:',absolute_url)
                relative_path = os.path.relpath(absolute_url, "https://rawdata-west.oceanobservatories.org/files/")
                # relative_path = os.path.relpath(absolute_url, searched[0])
                print('relative_path:',relative_path)
                local_path = os.path.join(base_dir, relative_path).replace(':','')
                print('local_path:',local_path)

                
                
                

                # Ensure the directory structure exists
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                # Download the file
                if not(os.path.exists(local_path) or os.path.exists(local_path.replace('.mseed','.flac'))):
                    # use wget silently and non blocking
                    print(f'wget -q  {absolute_url} -O '+ local_path.replace(" ", "\ "))
                    os.system(f'wget -q  {absolute_url} -O '+local_path.replace(" ", "\ "))
                # download_file(urljoin(url, href), local_path)
                # print(urljoin(url, href))

                # raise

                # print(f"Downloaded: {local_path}")
            elif href.endswith('/'):
                print(urljoin(url, href))
                # if the url is the parent of the current url, skip it
                if urljoin(url, href) in searched:
                    continue
                # Recursively process subdirectories
                searched_ = download_mseed_files(urljoin(url, href), base_dir, filters=filters, searched=searched)
                # extend only if elements are not in searched, but preserve order
                searched.extend([s for s in searched_ if s not in searched])
        return searched
    return []

wget_list = []
def list_all_mseed_files(url, base_dir, searched=[], filters=None):
    """
    save all wget commands to a list (hopefully this is faster)
    """
    global wget_list
    if url in searched:
        return []
    response = requests.get(url)

    # also append the parents of the url
    searched.append('/'.join(url.split('/')[:-2])+'/')    
    searched.append(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a').reverse():
            href = link.get('href')
            if href.endswith('.mseed'):
                # for example href is ./OO-HYEA2--YDH-2018-01-01T00:00:00.000000.mseed
                # and url is https://rawdata-west.oceanobservatories.org/files/CE02SHBP/LJ01D/11-HYDBBA106/2018/01/01/
                # we want to save the file to os.path.join(base_dir, 'CE02SHBP/LJ01D/11-HYDBBA106/2018/01/01/OO-HYEA2--YDH-2018-01-01T00:00:00.000000.mseed')
                absolute_url = urljoin(url, href)
                # all filters must be in the absolute_url
                if filters is not None:
                    if not(all([filt in absolute_url for filt in filters])):
                        continue

                # make sure the file is long enough
                d = requests.get(absolute_url)
                if int(d.headers['Content-Length'])<1000000:
                    continue
                relative_path = os.path.relpath(absolute_url, "https://rawdata-west.oceanobservatories.org/files/")
                local_path = os.path.join(base_dir, relative_path).replace(':','-')


                # # Download the file
                # if not(os.path.exists(local_path) or os.path.exists(local_path.replace('.mseed','.flac'))):
                #     # use wget silently and non blocking
                print(f'wget -q  {absolute_url} -O '+ local_path.replace(" ", "\ "))
                wget_list.append(f'wget -q  {absolute_url} -O '+local_path.replace(" ", "\ "))
                # download_file(urljoin(url, href), local_path)
                # print(urljoin(url, href))

                # raise

                # print
            elif href.endswith('/'):
                print(urljoin(url, href))
                # if the url is the parent of the current url, skip it
                if urljoin(url, href) in searched:
                    continue
                # Recursively process subdirectories
                searched_ = list_all_mseed_files(urljoin(url, href), base_dir, filters=filters, searched=searched)
                # extend only if elements are not in searched, but preserve order
                searched.extend([s for s in searched_ if s not in searched])
        return searched
    return []


if __name__=="__main__":
    # get_ooi_data(filters='2017',no_download=False)
    # Replace with the URL of the raw data directory
    # url_to_raw_data = "https://rawdata-west.oceanobservatories.org/files/CE02SHBP/"
    url_to_raw_data = "https://rawdata-west.oceanobservatories.org/files/CE02SHBP/LJ01D/11-HYDBBA106/2023/"
    # Replace with the local base directory where you want to save the files
    local_base_dir = "/media/bnestor/One Touch/ocean_observatories_initiative/"

    download_mseed_files(url_to_raw_data, local_base_dir, filters=['2023'])
    # list_all_mseed_files(url_to_raw_data, local_base_dir, filters=['2017'])

    # save wget_list to a file
    with open('wget_list.txt', 'w+') as f:
        f.write('\n'.join(wget_list))


 
