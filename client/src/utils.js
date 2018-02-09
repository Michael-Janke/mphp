export function isHealthy(tissueType) {
  return tissueType[0] === "N";
}

export function canRunOneAgainstAll(algorithm) {
  return algorithm.key !== "pca" && algorithm.cancerTypes.length >= 2;
}
