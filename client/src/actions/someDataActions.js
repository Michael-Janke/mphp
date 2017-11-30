import * as types from "./actionTypes";
import request from "../request";

export function load() {
  return dispatch =>
    request("/data").then(someData => {
      dispatch(_load(someData));
    });

  function _load(someData) {
    return {
      type: types.LOAD_SOME_DATA,
      someData
    };
  }
}
