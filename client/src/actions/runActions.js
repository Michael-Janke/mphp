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

export function createRun() {
  return dispatch => {
    const id = Date.now();
    dispatch({ type: types.CREATE_RUN, id });
  };
}

export function updateRun(id, algorithm) {
  return dispatch => {
    dispatch({ type: types.UPDATE_RUN, id, algorithm });
  };
}

export function runAlgorithm(id, algorithm) {
  return dispatch => {
    dispatch({ type: types.START_ALGORITHM, id, algorithm });
    postRequest("/runAlgorithm", { algorithm }).then(response =>
      dispatch(_runAlgorithm(id, response))
    );

    function _runAlgorithm(id, result) {
      return {
        type: types.ALGORITHM_DONE,
        id,
        result
      };
    }
  };
}
