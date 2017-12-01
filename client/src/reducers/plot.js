import * as types from "../actions/actionTypes";

const initialState = null;

export function plot(state = initialState, action = {}) {
  switch (action.type) {
    case types.LOAD_PLOT:
      console.log(action);

      return action.plot;
    default:
      return state;
  }
}
