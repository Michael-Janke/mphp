import { combineReducers } from "redux";
import { statistics } from "./statistics";
import { dataSelection } from "./dataSelection";
import { experiment } from "./experiment";
import { algorithms } from "./algorithms";
import { runs } from "./runs";

export default combineReducers({
  statistics,
  dataSelection,
  experiment,
  algorithms,
  runs
});
