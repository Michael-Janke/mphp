import * as types from "../../actions/actionTypes";

const initialState = [];

export function tcgaTokens(state = initialState, action = {}) {
  switch (action.type) {
    case types.LOAD_STATISTICS:
      return action.tcgaTokens;
    default:
      return state;
  }
}
