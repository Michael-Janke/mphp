import urllib.request
import os
import zipfile
import sys
import shutil
from parse_tcga_dataset import parse_tcga_dataset
from parse_gtex_dataset import parse_gtex_dataset
from merge_gtex_tcga import merge_gtex_tcga
from download_gene_names import download_gene_names
#sys.path.insert(0, './parse_data_scripts')

parseFunctionMap = {
    "tcga": parse_tcga_dataset,
    "gtex": parse_gtex_dataset,
    "merge": merge_gtex_tcga
}

urls = {
    "dataset1": {
        "parse": False,
    },
    "dataset2": {
        "url":
        "https://www.dropbox.com/sh/1v31yeu0zb4jcmm/AAAi5medvxa_kIbAEB7Edywua?dl=1&preview=LargeSets.zip",
        "parse": [],
    },
    "dataset3": {
        "url":
        "https://www.dropbox.com/s/0hqq2g2ipefy1u1/large_allSampleTypes.zip?dl=1",
        "parse": [],
    },
    "dataset4": {
        "url": "https://www.dropbox.com/s/l2bpf4lka8jxktg/LargeSet.zip?dl=1",
        "parse": ["tcga"],
        "version": "001"
    },
    "dataset5": {
        "url": "https://www.dropbox.com/s/xcrp4adwk6itwdi/GTEX_TCGA.zip?dl=1",
        "parse": ["tcga", "gtex", "merge"],
        "version": "001"
    },
    "gene_names": {
        "download_gene_names": True
    }
}

if not os.path.exists("data"):
    os.makedirs("data")

for dataset, url in urls.items():
    path = "data/" + dataset
    if "url" in url:
        if not os.path.exists(path):
            print("download " + dataset, flush=True)
            os.makedirs(path)
            urllib.request.urlretrieve(url["url"], path + "/download.zip")
            print("unzip " + dataset, flush=True)
            with zipfile.ZipFile(path + "/download.zip", "r") as zip_ref:
                zip_ref.extractall(path)
            os.remove(path + "/download.zip")
        else:
            print("skip already downloaded " + dataset, flush=True)
    
    
    if "parse" in url:
        version = ""
        if "version" in url:
            version = url["version"]
        try:
            file = open(path+"/version", "r")
            lastVersion = file.read()
            file.close()
        except:
            lastVersion = ""

        if version != lastVersion:
            if os.path.exists(path + "/subsets"):
                shutil.rmtree(path + "/subsets")
            
            for parseFunction in url["parse"]:
                print("parse {0}/{1}/{2}".format(dataset, version, parseFunction), flush=True)
                parseFunctionMap[parseFunction](dataset)
                file = open(path+"/version", "w")
                file.write(version)
                file.close()
        
        if version == lastVersion:
            print("already parsed {0}/{1}".format(dataset, version), flush=True)

    if "download_gene_names" in url and url["download_gene_names"] and not os.path.exists(
            path):
        os.makedirs(path)
        download_gene_names(path)
        print("downloaded genes names", flush=True)

    print("finished " + dataset, flush=True)
