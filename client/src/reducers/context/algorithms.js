import * as types from "../../actions/actionTypes";

const initialState = null;

export function algorithms(state = initialState, action = {}) {
  switch (action.type) {
    case types.LOAD_ALGORITHMS:
      return action.algorithms;
    default:
      return state;
  }
}
