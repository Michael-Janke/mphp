#install.packages("data.table")
#install.packages("bit64")
require(data.table)
require(bit64)

start = Sys.time()
# read first metadata part
metaDataFilename = "data/TCGA-GBM_TCGA-THCA_TCGA-LAML_TCGA-HNSC_TCGA-LUAD_TCGA-UCEC_TCGA-KIRC_TCGA-SARC__GeneExpressionQuantification_TP_TB_HTSeq-Counts_metadata.csv"
metaData <- fread(metaDataFilename, header = T, sep = ',')
metaData[,1:=NULL]

# read and combine rest of metadata part
metaDataFilename = "data/TCGA-PRAD_TCGA-OV_TCGA-COAD_TCGA-LUSC_TCGA-BRCA_TCGA-PAAD_TCGA-STAD_TCGA-CESC__GeneExpressionQuantification_TP_HTSeq-Counts_metadata.csv"
metaData2 <- fread(metaDataFilename, header = T, sep = ',')
metaData2[,1:=NULL]

metaData = do.call(cbind, list(metaData, metaData2))
rm(metaData2)

# read first data part
dataFilename = "data/TCGA-GBM_TCGA-THCA_TCGA-LAML_TCGA-HNSC_TCGA-LUAD_TCGA-UCEC_TCGA-KIRC_TCGA-SARC__GeneExpressionQuantification_TP_TB_HTSeq-Counts.csv"
data <- fread(dataFilename, header = T, sep = ',')

# read and combine rest of metadata part
dataFilename = "data/TCGA-PRAD_TCGA-OV_TCGA-COAD_TCGA-LUSC_TCGA-BRCA_TCGA-PAAD_TCGA-STAD_TCGA-CESC__GeneExpressionQuantification_TP_HTSeq-Counts.csv"
data2 <- fread(dataFilename, header = T, sep = ',')

genes1 = colnames(data)
genes2 = colnames(data2)

missing_genes = setdiff(genes1,genes2)
data[,(missing_genes):=NULL]
missing_genes = setdiff(genes2,genes1)
data2[,(missing_genes):=NULL]


data = do.call(rbind, list(data, data2))
rm(data2)

# get cancer types
cancerTypes <- as.vector(unique(unlist(metaData[1,])))
remove = c(NA,"project_id")
cancerTypes = cancerTypes[! cancerTypes %in% remove]

end = Sys.time()
print(end-start)





####### CLEAN UP #######
rm(start)
rm(end)
rm(dataFilename)
rm(metaDataFilename)
rm(remove)
rm(genes1)
rm(genes2)
rm(missing_genes)