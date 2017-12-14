import * as types from "./actionTypes";
import { postRequest } from "./_request";

export function load(route, params) {
  return dispatch =>
    postRequest(route, {
      algorithm: params
    }).then(response => dispatch(_load(response)));

  function _load(plot) {
    return {
      type: types.LOAD_PLOT,
      plot
    };
  }
}
