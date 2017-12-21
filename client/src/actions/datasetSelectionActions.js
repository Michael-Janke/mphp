import { TOGGLE_TOKEN, TOGGLE_TISSUE_TYPE } from "./actionTypes";

export function toggleTcgaToken(token) {
  return {
    type: TOGGLE_TOKEN,
    token
  };
}

export function toggleTissueType(tissueType) {
  return {
    type: TOGGLE_TISSUE_TYPE,
    tissueType
  };
}
