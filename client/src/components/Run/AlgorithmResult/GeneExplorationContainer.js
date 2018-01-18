import { connect } from "react-redux";

import { testGenes } from "../../../actions/runActions";
import GeneExploration from "./GeneExploration";

const mapStateToProps = state => {
  return {
    runs: state.runs
  };
};

const mapDispatchToProps = dispatch => {
  return {
    testGenes: (runId, params) => {
      dispatch(testGenes(runId, params));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(GeneExploration);
