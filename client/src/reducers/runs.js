import * as types from "../actions/actionTypes";

const initialState = {};

export function runs(state = initialState, action = {}) {
  switch (action.type) {
    case types.CREATE_RUN:
      return { ...state, [action.id]: { params: action.params } };
    case types.RUN_ALGORITHM:
      return Object.keys(state).includes(`${action.id}`)
        ? {
            ...state,
            [action.id]: { ...state[action.id], result: action.result }
          }
        : state;
    default:
      return state;
  }
}
