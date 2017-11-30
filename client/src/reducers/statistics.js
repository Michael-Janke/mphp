import * as types from "../actions/actionTypes";

const initialState = {
  statistics: null
};

export function statistics(state = initialState, action = {}) {
  switch (action.type) {
    case types.LOAD_STATISTICS:
      return action.statistics;
    default:
      return state;
  }
}
