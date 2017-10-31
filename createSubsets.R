# write data on disk

for (type in cancerTypes){
  selectedIndices = which(metaData[1,] == type)
  selectedMetaData = metaData[,min(selectedIndices):max(selectedIndices)]
  selectedData <- data[min(selectedIndices):max(selectedIndices),] # data has sample name in first column
  
  dataName = paste("data/subsets/",type,"-Data.csv",sep = "")
  metaDataName = paste("data/subsets/",type,"-MetaData.csv",sep = "")
  
  fwrite(selectedData,dataName)
  fwrite(selectedMetaData,metaDataName)
}


####### CLEAN UP #######
rm(type)
rm(selectedIndices)
rm(selectedMetaData)
rm(selectedData)
rm(dataName)
rm(metaDataName)