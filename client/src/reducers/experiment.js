import * as types from "../actions/actionTypes";

const initialState = {
  name: "Epic Experiment",
  dataset: "TCGA Dataset 4"
};

export function experiment(state = initialState, action = {}) {
  switch (action.type) {
    case types.UPDATE_EXPERIMENT_NAME:
      return { ...state, name: action.experimentName };
    default:
      return state;
  }
}
