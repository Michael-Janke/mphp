import * as types from "./actionTypes";
import request from "./_request";

export function load() {
  return dispatch =>
    request("/statistics").then(statistics => {
      dispatch(_load(statistics));
    });

  function _load(statistics) {
    const tcgaTokens = Object.keys(statistics).map(token => token);
    const tissueTypes = Object.keys(statistics[tcgaTokens[0]]).map(
      tissueType => tissueType
    );
    return {
      type: types.LOAD_STATISTICS,
      statistics,
      tcgaTokens,
      tissueTypes
    };
  }
}
