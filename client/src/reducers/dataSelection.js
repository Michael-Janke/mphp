import {
  TOGGLE_TOKEN,
  TOGGLE_TISSUE_TYPE,
  LOAD_STATISTICS
} from "../actions/actionTypes";

const initialState = { tcgaTokens: [], tissueTypes: [] };

export function dataSelection(state = initialState, action = {}) {
  switch (action.type) {
    case LOAD_STATISTICS:
      const tcgaTokens = Object.keys(action.statistics).map(token => ({
        name: token,
        selected: true
      }));

      const tissueTypes = Object.keys(
        action.statistics[tcgaTokens[0].name]
      ).map(tissueType => ({
        name: tissueType,
        selected: true
      }));
      tissueTypes.push({ name: "healthy", selected: true });
      tissueTypes.push({ name: "sick", selected: true });
      tissueTypes.push({ name: "all", selected: true });

      return {
        tcgaTokens,
        tissueTypes
      };

    case TOGGLE_TOKEN:
      const tcgaIndex = state.tcgaTokens.indexOf(action.token);
      const newTcgaTokens = state.tcgaTokens.map(token => {
        if (token === action.token) {
          return {
            name: token.name,
            selected: !state.tcgaTokens[tcgaIndex].selected
          };
        } else {
          return token;
        }
      });
      return {
        ...state,
        tcgaTokens: newTcgaTokens
      };

    case TOGGLE_TISSUE_TYPE:
      const tissueIndex = state.tissueTypes.indexOf(action.tissueType);
      const newTissueTypes = state.tissueTypes.map(tissueType => {
        if (tissueType === action.tissueType) {
          return {
            name: tissueType.name,
            selected: !state.tissueTypes[tissueIndex].selected
          };
        } else {
          return tissueType;
        }
      });
      return {
        ...state,
        tissueTypes: newTissueTypes
      };

    default:
      return state;
  }
}
