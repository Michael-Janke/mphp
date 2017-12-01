import * as types from "./actionTypes";
import request from "./_request";

export function load() {
  return dispatch =>
    request("/plot").then(plot => {
      dispatch(_load(plot));
    });

  function _load(plot) {
    return {
      type: types.LOAD_PLOT,
      plot
    };
  }
}
