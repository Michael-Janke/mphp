import { combineReducers } from "redux";
import { context } from "./context";
import { experiment } from "./experiment";
import { runs } from "./runs";

export default combineReducers({
  context,
  experiment,
  runs
});
