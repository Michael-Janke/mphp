import * as types from "../actions/actionTypes";

const initialState = {
  name: "Epic Experiment",
  dataset: "",
  datasets: {}
};

export function experiment(state = initialState, action = {}) {
  switch (action.type) {
    case types.UPDATE_EXPERIMENT_NAME:
      return { ...state, name: action.experimentName };
    case types.LOAD_CONTEXT:
      return { ...state, datasets: action.context.datasets, dataset: "dataset5"};
    default:
      return state;
  }
}
