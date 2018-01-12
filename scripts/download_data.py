import urllib.request
import os
import zipfile
import sys
from parse_tcga_dataset import parse_tcga_dataset
from parse_gtex_dataset import parse_gtex_dataset
from merge_gtex_tcga import merge_gtex_tcga
from download_gene_names import download_gene_names
from create_statistics import create_statistics
#sys.path.insert(0, './parse_data_scripts')

parseFunctionMap = {
	"tcga": parse_tcga_dataset,
	"gtex": parse_gtex_dataset,
	"merge": merge_gtex_tcga
}

urls = {
	"dataset1": {
		"parse": False,
		"create_statistics": False,
	},
	"dataset2": {
		"url":"https://www.dropbox.com/sh/1v31yeu0zb4jcmm/AAAi5medvxa_kIbAEB7Edywua?dl=1&preview=LargeSets.zip",
		"parse": [],
		"create_statistics": False,
	},
	"dataset3":	{
		"url":"https://www.dropbox.com/s/0hqq2g2ipefy1u1/large_allSampleTypes.zip?dl=1",
		"parse": [],
		"create_statistics": True,
	},
	"dataset4":	{
		"url":"https://www.dropbox.com/s/l2bpf4lka8jxktg/LargeSet.zip?dl=1",
		"parse": ["tcga"],
		"create_statistics": True,
	},
	"dataset5":	{
		"url":"https://www.dropbox.com/s/xcrp4adwk6itwdi/GTEX_TCGA.zip?dl=1",
		"parse": ["tcga","gtex", "merge"],
		#"create_statistics": True,
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
			with zipfile.ZipFile(path + "/download.zip","r") as zip_ref:
				zip_ref.extractall(path)
			os.remove(path + "/download.zip")
		else:
			print("skip already downloaded " + dataset, flush=True)

	if not os.path.exists(path + "/subsets") and "parse" in url:
		if url["parse"]:
			for parseFunction in url["parse"]:
				print("parse " + dataset + "/" + parseFunction, flush=True)
				parseFunctionMap[parseFunction](dataset)
		else:
			print("parser for " + dataset + " not implemented yet. Stay tuned!", flush=True)
	else:
		print("already parsed " + dataset, flush=True)

	if not os.path.exists(path + "/statistics") and "create_statistics" in url:
		if url["create_statistics"]:
			print("creating statistics for " + dataset, flush=True)
			create_statistics(dataset)
		else:
			print("skipping statistics for " + dataset, flush=True)
	else:
		print("already created statistics for " + dataset, flush=True)

	if "download_gene_names" in url and url["download_gene_names"] and not os.path.exists(path):
		os.makedirs(path)
		download_gene_names(path)
		print("downloaded genes names", flush=True)

	print("finished " + dataset, flush=True)
