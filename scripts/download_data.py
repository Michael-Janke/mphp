import urllib.request
import os
import zipfile
import sys
#sys.path.insert(0, './parse_data_scripts')

urls = {
	"dataset1": {
		"parse": False,
	},
	"dataset2": {
		"url":"https://www.dropbox.com/sh/1v31yeu0zb4jcmm/AAAi5medvxa_kIbAEB7Edywua?dl=1&preview=LargeSets.zip",
		"parse": False,
	},
	"dataset3":	{
		"url":"https://www.dropbox.com/s/0hqq2g2ipefy1u1/large_allSampleTypes.zip?dl=1",
		"parse": True,
	}
}

if not os.path.exists("data"):
	os.makedirs("data")

for dataset, url in urls.items():
	path = "data/" + dataset
	if "url" in url:
		if not os.path.exists(path):
			print("download " + dataset)
			os.makedirs(path)
			urllib.request.urlretrieve(url["url"], path + "/download.zip")
			print("unzip " + dataset)
			with zipfile.ZipFile(path + "/download.zip","r") as zip_ref:
				zip_ref.extractall(path)
			os.remove(path + "/download.zip")
		else:
			print("skip already downloaded " + dataset)

	if not os.path.exists(path + "/subsets"):
		if url["parse"]:
			print("parse " + dataset)
			__import__("parse_" + dataset)
		else:
			print("parser for " + dataset + " not implemented yet. Stay tuned!")
	else:
		print("already parsed " + dataset)

	print("finished " + dataset)
