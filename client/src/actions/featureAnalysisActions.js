import * as types from "./actionTypes";
import request from "./_request";

export function load() {
  return dispatch =>
    request("/algorithms").then(algorithms => {
      dispatch(_load(algorithms));
    });

  function _load(algorithms) {
    return {
      type: types.LOAD_ALGORITHMS,
      algorithms
    };
  }
}
