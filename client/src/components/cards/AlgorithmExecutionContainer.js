import { connect } from "react-redux";
import { load as loadStatistics } from "../../actions/statisticsActions";
import { loadAlgorithms, runAlgorithm } from "../../actions/algorithmActions";
import AlgorithmExecution from "./AlgorithmExecution";

const mapStateToProps = state => {
  return {
    algorithms: state.algorithms,
    runs: state.runs,
    statistics: state.statistics,
    tcgaTokens: state.dataSelection.tcgaTokens,
    tissueTypes: state.dataSelection.tissueTypes
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadAlgorithms: () => {
      dispatch(loadAlgorithms());
    },
    runAlgorithm: params => {
      dispatch(runAlgorithm(params));
    },
    loadStatistics: () => {
      dispatch(loadStatistics());
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(AlgorithmExecution);
