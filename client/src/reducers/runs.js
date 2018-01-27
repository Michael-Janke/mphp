import * as types from "../actions/actionTypes";

const emptyRun = {
  algorithm: { cancerTypes: ["THCA", "COAD"], healthyTissueTypes: ["NT"], sickTissueTypes: ["TP"] },
  dataset: "dataset5",
  isLoading: false,
  result: null,
  geneResults: null
};

const initialState = {
  [Date.now()]: { ...emptyRun }
};

export function runs(state = initialState, action = {}) {
  if(action.type !== types.CREATE_RUN && !state[action.id]) {return state}
  switch (action.type) {
    case types.CREATE_RUN:
      return { ...state, [action.id]: emptyRun };
    case types.UPDATE_RUN:
      return updateRun(state, action.id, action.updates);
    case types.DELETE_RUN:
      let newState = {...state};
      delete newState[action.id];
      return newState;
    case types.START_RUN:
      return updateRun(state, action.id, {
        result: null,
        isLoading: true
      });
    case types.FINISH_RUN:
      return updateRun(state, action.id, {
        isLoading: false,
        result: action.result
      });
    case types.GENE_RESULTS:
      return updateRun(state, action.id, {
        isLoading: false,
        geneResults: action.result
      });
    default:
      return state;
  }
}

function updateRun(state, runid, updates) {
  return {
        ...state,
        [runid]: {
          ...state[runid],
          ...updates
        }
      }
}
