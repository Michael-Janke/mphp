import React, { Component } from "react";
import { connect } from "react-redux";

import { load } from "../../actions/featureAnalysisActions";
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
      dispatch(load());
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(FeatureAnalysis);
