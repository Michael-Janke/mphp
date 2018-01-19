import * as types from "../actions/actionTypes";

const initialState = {};

export function context(state = initialState, action = {}) {
  switch (action.type) {
    case types.LOAD_CONTEXT:
      return action.context;
    default:
      return state;
  }
}
