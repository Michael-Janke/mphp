import * as types from "../actions/actionTypes";

const emptyRun = { params: {}, isLoading: false, result: null };

const initialState = {
  [Date.now()]: { ...emptyRun }
};

export function runs(state = initialState, action = {}) {
  switch (action.type) {
    case types.CREATE_RUN:
      return { ...state, [action.id]: { ...emptyRun } };
    case types.START_ALGORITHM:
      return Object.keys(state).includes(`${action.id}`)
        ? {
            ...state,
            [action.id]: {
              ...state[action.id],
              params: action.params,
              isLoading: true
            }
          }
        : state;
    case types.ALGORITHM_DONE:
      return Object.keys(state).includes(`${action.id}`)
        ? {
            ...state,
            [action.id]: {
              ...state[action.id],
              isLoading: false,
              result: action.result
            }
          }
        : state;
    default:
      return state;
  }
}
