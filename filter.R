thresh <- 55542*0.3
badColumns = c()
i = 0

for (col in data[,1:55542]){
  i = i+1
  indices = which(is.nan(col))
  if (length(indices) > thresh){
    badColumns = c(badColumns, 1)
    print(length(indices))
  }
  if (length(indices) > 0){
    print(i) 
  }
}
