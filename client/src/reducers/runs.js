import * as types from "../actions/actionTypes";

const emptyRun = {
  algorithm: { cancerTypes: ["THCA", "COAD"], healthyTissueTypes: ["NT"], sickTissueTypes: ["TP"] },
  isLoading: false,
  result: null
};

const initialState = {
  [Date.now()]: { ...emptyRun }
};

export function runs(state = initialState, action = {}) {
  switch (action.type) {
    case types.CREATE_RUN:
      return { ...state, [action.id]: emptyRun };
    case types.UPDATE_ALGORITHM:
      return updateRun(state, action, {
        algorithm: action.algorithm
      });
    case types.START_ALGORITHM:
      return updateRun(state, action, {
        algorithm: action.algorithm,
        isLoading: true
      });
    case types.ALGORITHM_DONE:
      return updateRun(state, action, {
        isLoading: false,
        result: action.result
      });
    default:
      return state;
  }
}

function updateRun(state, action, updates) {
  return Object.keys(state).includes(`${action.id}`)
    ? {
        ...state,
        [action.id]: {
          ...state[action.id],
          ...updates
        }
      }
    : state;
}
