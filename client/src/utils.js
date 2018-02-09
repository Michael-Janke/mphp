export function isHealthy(tissueType) {
  return tissueType[0] === "N";
}

export function canRunOneAgainstAll(algorithm) {
  return algorithm.cancerTypes.length >= 2;
}
