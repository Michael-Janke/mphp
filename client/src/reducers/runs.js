import * as types from "../actions/actionTypes";
import { isHealthy } from "../utils";

const emptyRun = {
  algorithm: { cancerTypes: [], healthyTissueTypes: [], sickTissueTypes: [] },
  isLoading: false,
  result: null,
  isEvaluating: false,
  evaluation: null
};

const initialState = {
  [Date.now()]: { ...emptyRun }
};

export function runs(state = initialState, action = {}) {
  switch (action.type) {
    case types.LOAD_STATISTICS:
      return Object.keys(state).reduce((reducedState, runId) => {
        return {
          ...reducedState,
          [runId]: preselectData(state[runId], action)
        };
      }, {});
    case types.CREATE_RUN:
      return { ...state, [action.id]: preselectData(emptyRun, action) };
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
    case types.START_EVALUATION:
      return updateRun(state, action, {
        isEvaluating: true
      });
    case types.EVALUATION_DONE:
      return updateRun(state, action, {
        isEvaluating: false,
        evaluation: action.evaluation
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

function preselectData(run, { tcgaTokens, tissueTypes }) {
  const preselectedTokens = ["THCA", "LUAD"];
  const preselectedTissues = ["NT", "TP"];
  const healthyTissueTypes = tissueTypes.filter(
    tissueType =>
      isHealthy(tissueType) && preselectedTissues.includes(tissueType)
  );
  const sickTissueTypes = tissueTypes.filter(
    tissueType =>
      !isHealthy(tissueType) && preselectedTissues.includes(tissueType)
  );
  return {
    ...run,
    algorithm: {
      cancerTypes: tcgaTokens.filter(token =>
        preselectedTokens.includes(token)
      ),
      healthyTissueTypes,
      sickTissueTypes
    }
  };
}
