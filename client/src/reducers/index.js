import { combineReducers } from "redux";
import { statistics } from "./statistics";
import { plot } from "./plot";
import { dataSelection } from "./dataSelection";
import { experiment } from "./experiment";
import { featureAnalysis } from "./featureAnalysis";

export default combineReducers({
  statistics,
  plot,
  dataSelection,
  experiment,
  featureAnalysis
});
