import { combineReducers } from "redux";
import { statistics } from "./statistics";
import { algorithms } from "./algorithms";
import { tcgaTokens } from "./tcgaTokens";
import { tissueTypes } from "./tissueTypes";

export const context = combineReducers({
  statistics,
  algorithms,
  tcgaTokens,
  tissueTypes
});
