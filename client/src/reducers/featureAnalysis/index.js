import { combineReducers } from "redux";
import { algorithms } from "./algorithms";
import { runs } from "./runs";

export const featureAnalysis = combineReducers({ algorithms, runs });
