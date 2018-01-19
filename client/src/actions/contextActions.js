import * as types from "./actionTypes";
import request from "./_request";

export function loadContext() {
  return dispatch => {
    dispatch({
      type: types.LOAD_CONTEXT,
      context: {}
    });
    request("/context").then(context => {
      dispatch({
          type: types.LOAD_CONTEXT,
          context
      });
    });
  };
}