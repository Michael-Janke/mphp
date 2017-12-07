import * as types from "./actionTypes";

export function updateName(experimentName) {
  return dispatch =>
    dispatch({
      type: types.UPDATE_EXPERIMENT_NAME,
      experimentName
    });
}
