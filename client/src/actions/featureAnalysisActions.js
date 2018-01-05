import * as types from "./actionTypes";
import request, { postRequest } from "./_request";

export function loadAlgorithms() {
  return dispatch =>
    request("/algorithms").then(algorithms => {
      dispatch(_load(algorithms));
    });

  function _load(data) {
    return {
      type: types.LOAD_ALGORITHMS,
      algorithms: data.isError ? data : data.algorithms
    };
  }
}

export function runAlgorithm(params) {
  return dispatch => {
    const id = Date.now();
    dispatch({ type: types.CREATE_RUN, id, params });
    postRequest("/runAlgorithm", {
      algorithm: params
    }).then(response => dispatch(_runAlgorithm(id, response)));

    function _runAlgorithm(id, result) {
      return {
        type: types.RUN_ALGORITHM,
        id,
        result
      };
    }
  };
}
