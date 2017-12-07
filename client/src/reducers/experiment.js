import * as types from "../actions/actionTypes";

const initialState = {
  name: "Epic Experiment"
};

export function experiment(state = initialState, action = {}) {
  switch (action.type) {
    case types.UPDATE_EXPERIMENT_NAME:
      return { name: action.experimentName };
    default:
      return state;
  }
}
