import * as types from "../actions/actionTypes";

const initialState = { algorithms: null };

export function featureAnalysis(state = initialState, action = {}) {
  switch (action.type) {
    case types.LOAD_ALGORITHMS:
      return { ...state, ...action.algorithms };
    default:
      return state;
  }
}
