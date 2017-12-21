import React, { Component } from "react";
import { connect } from "react-redux";

import { load } from "../../actions/statisticsActions";
import DataSelection from "./DataSelection";

const mapStateToProps = state => {
  return {
    statistics: state.statistics,
    tcgaTokens: state.dataSelection.tcgaTokens,
    tissueTypes: state.dataSelection.tissueTypes
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadStatistics: () => {
      dispatch(load());
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(DataSelection);
