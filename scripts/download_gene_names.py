import numpy as np
import urllib.parse
import urllib.request
import csv
import codecs
def download_gene_names(path):
	query = """<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE Query>
	<Query  virtualSchemaName = "default" formatter = "CSV" header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >

		<Dataset name = "hsapiens_gene_ensembl" interface = "default" >
			<Attribute name = "ensembl_gene_id" />
			<Attribute name = "external_gene_name" />
			<Attribute name = "entrezgene" />
		</Dataset>
	</Query>"""
	url="http://www.ensembl.org/biomart/martservice?query="

	f = urllib.request.urlopen(url+urllib.parse.quote_plus(query))
	reader = csv.reader(codecs.iterdecode(f, 'utf-8'))

	gene_map = {}
	entrez_map = {}
	for rows in reader:
		gene_map[int(rows[0][4:])] = rows[1]
		entrez_map[int(rows[0][4:])] = rows[2]

	np.save	(path + "/gene_names", gene_map)
	np.save	(path + "/entrez_names", entrez_map)
