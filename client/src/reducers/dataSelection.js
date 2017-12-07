import { TOGGLE_TOKEN, TOGGLE_TISSUE_TYPE } from "../actions/actionTypes";

const initialState = { tcgaTokens: [], tissueTypes: [] };

export function dataSelection(state = initialState, action = {}) {
  switch (action.type) {
    case TOGGLE_TOKEN:
      if (state.tcgaTokens.includes(action.token)) {
        const index = state.tcgaTokens.indexOf(action.token);
        return {
          ...state,
          tcgaTokens: [
            ...state.tcgaTokens.slice(0, index),
            ...state.tcgaTokens.slice(index + 1)
          ]
        };
      } else {
        return {
          ...state,
          tcgaTokens: [...state.tcgaTokens, action.token]
        };
      }

    case TOGGLE_TISSUE_TYPE:
      if (state.tissueTypes.includes(action.tissueType)) {
        const index = state.tissueTypes.indexOf(action.tissueType);
        return {
          ...state,
          tissueTypes: [
            ...state.tissueTypes.slice(0, index),
            ...state.tissueTypes.slice(index + 1)
          ]
        };
      } else {
        return {
          ...state,
          tissueTypes: [...state.tissueTypes, action.tissueType]
        };
      }

    default:
      return state;
  }
}
