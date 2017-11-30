import * as types from "./actionTypes";
import request from "./_request";

export function load() {
  return dispatch =>
    request("/statistics").then(statistics => {
      dispatch(_load(statistics));
    });

  function _load(statistics) {
    return {
      type: types.LOAD_STATISTICS,
      statistics
    };
  }
}
