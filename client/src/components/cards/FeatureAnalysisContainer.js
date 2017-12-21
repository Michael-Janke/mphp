import { connect } from "react-redux";
import {
  loadAlgorithms,
  runAlgorithm
} from "../../actions/featureAnalysisActions";
import FeatureAnalysis from "./FeatureAnalysis";

const mapStateToProps = state => {
  return {
    ...state.featureAnalysis,
    dataSelection: state.dataSelection
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadAlgorithms: () => {
      dispatch(loadAlgorithms());
    },
    runAlgorithm: params => {
      dispatch(runAlgorithm(params));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(FeatureAnalysis);
