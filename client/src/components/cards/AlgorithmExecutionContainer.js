import { connect } from "react-redux";
import { load as loadStatistics } from "../../actions/statisticsActions";
import {
  loadAlgorithms,
  runAlgorithm
} from "../../actions/featureAnalysisActions";
import AlgorithmExecution from "./AlgorithmExecution";

const mapStateToProps = state => {
  return {
    algorithms: state.featureAnalysis.algorithms,
    runs: state.featureAnalysis.runs,
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
