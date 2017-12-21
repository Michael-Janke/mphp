import * as types from "../../actions/actionTypes";

const initialState = {};

export function runs(state = initialState, action = {}) {
  switch (action.type) {
    case types.CREATE_RUN:
      return { ...state, [action.id]: { params: action.params } };
    case types.RUN_ALGORITHM:
      const currentRun = state[action.id];
      return {
        ...state,
        [action.id]: { ...currentRun, result: action.result }
      };
    default:
      return state;
  }
}
