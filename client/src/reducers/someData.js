import * as types from "../actions/actionTypes";

const initialState = null;

export function someData(state = initialState, action = {}) {
  switch (action.type) {
    case types.LOAD_SOME_DATA:
      return action.someData;
    default:
      return state;
  }
}
