import { combineReducers } from "redux";
import { statistics } from "./statistics";
import { dataSelection } from "./dataSelection";
import { experiment } from "./experiment";
import { featureAnalysis } from "./featureAnalysis";

export default combineReducers({
  statistics,
  dataSelection,
  experiment,
  featureAnalysis
});
