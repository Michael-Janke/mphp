import * as types from "../../actions/actionTypes";

const initialState = [];

export function tissueTypes(state = initialState, action = {}) {
  switch (action.type) {
    case types.LOAD_STATISTICS:
      return action.tissueTypes;
    default:
      return state;
  }
}
