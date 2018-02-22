import { connect } from "react-redux";

import { testGenes, fullTestGenes } from "../../../actions/runActions";
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
    },
    fullTestGenes: (runId, params) => {
      dispatch(fullTestGenes(runId, params));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(GeneExploration);
