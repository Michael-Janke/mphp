import urllib.request
import os
import zipfile
import sys
sys.path.insert(0, './parse_data_scripts')

urls = {
	"dataset1": {},
	"dataset2": {
		#"url":"https://www.dropbox.com/sh/1v31yeu0zb4jcmm/AAAi5medvxa_kIbAEB7Edywua?dl=1&preview=LargeSets.zip",
		#"unzip": True
	},
	"dataset3":	{
		"url":"https://www.dropbox.com/s/0hqq2g2ipefy1u1/large_allSampleTypes.zip?dl=1",
		"unzip":True,
		"parse": True
	}
}

if not os.path.exists("data"):
	os.makedirs("data")

for dataset, url in urls.items():
	path = "data/" + dataset
	if not os.path.exists(path):
		os.makedirs(path)
	else:
		print("skip already downloaded " + dataset, flush=True)
		continue
	if "url" in url:
		print("download " + dataset, flush=True)
		if not os.path.exists(path):
			os.makedirs(path)
		urllib.request.urlretrieve(url["url"], path + "/download.zip")
	if "unzip" in url and url["unzip"]:
		print("unzip " + dataset, flush=True)
		with zipfile.ZipFile(path + "/download.zip","r") as zip_ref:
			zip_ref.extractall(path)
		os.remove(path + "/download.zip")
	if "parse" in url and url["parse"]:
		print("parse " + dataset, flush=True)
		__import__("parse_" + dataset)
	print("finsihed " + dataset, flush=True)