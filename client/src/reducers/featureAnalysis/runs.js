import * as types from "../../actions/actionTypes";

const initialState = [];

export function runs(state = initialState, action = {}) {
  switch (action.type) {
    case types.CREATE_RUN:
      return state;
    default:
      return state;
  }
}
