import { connect } from "react-redux";

import Results from "./Results";

const mapStateToProps = state => {
  return {
    ...state.featureAnalysis,
    dataSelection: state.dataSelection
  };
};

const mapDispatchToProps = dispatch => {
  return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(Results);
